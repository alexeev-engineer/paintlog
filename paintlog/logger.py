#!venv/bin/python3
"""Paintlog Example File.

Copyright Alexeev Bronislav (C) 2024
BSD 3 Clause License
"""
from time import monotonic
import ast
import logging
import inspect
import pprint
import sys
import warnings
from datetime import datetime
import functools
from contextlib import contextmanager
from os.path import basename, realpath
from textwrap import dedent
import colorama
import executing
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer as PyLexer, Python3Lexer as Py3Lexer

from paintlog.paint import debug_message, info_message, warn_message, error_message, other_message, run_exception
from paintlog.color_highlight import CatppuccinMocha


PYTHON2 = (sys.version_info[0] == 2)

_absent = object()
DEFAULT_THEME = CatppuccinMocha


@contextmanager
def supportTerminalColorsInWindows():
	"""Support terminal colors in Windows OS with colorama."""
	colorama.init()
	yield
	colorama.deinit()


def stderrPrint(*args):
	"""Print to stderr."""
	print(*args)


def isLiteral(s):
	"""Check string if literal."""
	try:
		ast.literal_eval(s)
	except Exception:
		return False
	return True


def bindStaticVariable(name, value):
    def decorator(fn):
        setattr(fn, name, value)
        return fn
    return decorator


@bindStaticVariable('formatter', Terminal256Formatter(style=DEFAULT_THEME))
@bindStaticVariable(
	'lexer', PyLexer(ensurenl=False) if PYTHON2 else Py3Lexer(ensurenl=False))
def colorize(s):
	"""Colorize with pygments."""
	self = colorize
	return highlight(s, self.lexer, self.formatter)


def colorized_stderr_print(obj):
	"""Colorized stderr print."""
	for s in obj.split('; '):
		if not s.startswith('pydbg_obj |'):
			s = f'pydbg_obj | {s}'
		colored = colorize(s)

		with supportTerminalColorsInWindows():
			stderrPrint(colored)


DEFAULT_PREFIX = 'pydbg_obj | '
DEFAULT_LINE_WRAP_WIDTH = 80  # Characters.
DEFAULT_CONTEXT_DELIMITER = '~ '
DEFAULT_OUTPUT_FUNCTION = colorized_stderr_print
DEFAULT_ARG_TO_STRING_FUNCTION = pprint.pformat


NO_SOURCE_AVAILABLE_WARNING_MESSAGE = (
	'Failed to access the underlying source code for analysis. Was ic() '
	'invoked in a REPL (e.g. from the command line), a frozen application '
	'(e.g. packaged with PyInstaller), or did the underlying source code '
	'change during execution?')


def callOrValue(obj):
	"""Call or value."""
	return obj() if callable(obj) else obj


class Source(executing.Source):
	"""Source."""

	def get_text_with_indentation(self, node):
		"""Get text with indents."""
		result = self.asttokens().get_text(node)
		if '\n' in result:
			result = ' ' * node.first_token.start[1] + result
			result = dedent(result)
		result = result.strip()
		return result


def prefixLines(prefix, s, startAtLine=0):
	"""Prefix lines."""
	lines = s.splitlines()

	for i in range(startAtLine, len(lines)):
		lines[i] = prefix + lines[i]

	return lines


def prefixFirstLineIndentRemaining(prefix, s):
	"""First line indent remaining prefix."""
	indent = ' ' * len(prefix)
	lines = prefixLines(indent, s, startAtLine=1)
	lines[0] = prefix + lines[0]
	return lines


def formatPair(prefix, arg, value):
	"""Formatting pair."""
	if arg is _absent:
		argLines = []
		valuePrefix = prefix
	else:
		argLines = prefixFirstLineIndentRemaining(prefix, arg)
		valuePrefix = argLines[-1] + ': '

	looksLikeAString = (value[0] + value[-1]) in ["''", '""']
	if looksLikeAString:  # Align the start of multiline strings.
		valueLines = prefixLines(' ', value, startAtLine=1)
		value = '\n'.join(valueLines)

	valueLines = prefixFirstLineIndentRemaining(valuePrefix, value)
	lines = argLines[:-1] + valueLines
	return '\n'.join(lines)


def singledispatch(func):
	"""Single dispatch function."""
	if "singledispatch" not in dir(functools):
		def unsupport_py2(*args, **kwargs):
			raise NotImplementedError(
				"functools.singledispatch is missing in " + sys.version
			)
		func.register = func.unregister = unsupport_py2
		return func

	func = functools.singledispatch(func)

	# add unregister based on https://stackoverflow.com/a/25951784
	closure = dict(zip(func.register.__code__.co_freevars, 
					   func.register.__closure__))
	registry = closure['registry'].cell_contents
	dispatch_cache = closure['dispatch_cache'].cell_contents
	def unregister(cls):
		del registry[cls]
		dispatch_cache.clear()
	func.unregister = unregister
	return func


@singledispatch
def argumentToString(obj):
	"""Convert argument to string."""
	s = DEFAULT_ARG_TO_STRING_FUNCTION(obj)
	s = s.replace('\\n', '\n')  # Preserve string newlines in output.
	return s


class PyDBG_Obj:
	"""Advanced print for debuging.
	
	>>> pydbg_obj | num: 12
	            	float_int: 12.12
	            	string: 'Hello'
	            	boolean: True
	            	list_array: [1, 2, 3, 'Hi', True, 12.2]
	            	dictionary: {1: 'HELLO', 2: 'WORLD'}
	
	"""

	_pairDelimiter = '; '
	lineWrapWidth = DEFAULT_LINE_WRAP_WIDTH
	contextDelimiter = DEFAULT_CONTEXT_DELIMITER

	def __init__(self, prefix=DEFAULT_PREFIX,
				 outputFunction=DEFAULT_OUTPUT_FUNCTION,
				 argToStringFunction=argumentToString, includeContext=False,
				 contextAbsPath=False):
		"""Initialization."""
		self.enabled = True
		self.prefix = prefix
		self.includeContext = includeContext
		self.outputFunction = outputFunction
		self.argToStringFunction = argToStringFunction
		self.contextAbsPath = contextAbsPath

	def __call__(self, *args):
		"""Call magic method."""
		if self.enabled:
			callFrame = inspect.currentframe().f_back
			self.outputFunction(self._format(callFrame, *args))

		if not args:
			passthrough = None
		elif len(args) == 1:
			passthrough = args[0]
		else:
			passthrough = args

		return passthrough

	def format(self, *args):
		"""Format arguments."""
		callFrame = inspect.currentframe().f_back
		out = self._format(callFrame, *args)
		return out

	def _format(self, callFrame, *args):
		"""Format helper function."""
		prefix = callOrValue(self.prefix)

		context = self._formatContext(callFrame)
		if not args:
			time = self._formatTime()
			out = prefix + context + time
		else:
			if not self.includeContext:
				context = ''
			out = self._formatArgs(
				callFrame, prefix, context, args)

		return out

	def _formatArgs(self, callFrame, prefix, context, args):
		"""Format arguments."""
		callNode = Source.executing(callFrame).node
		if callNode is not None:
			source = Source.for_frame(callFrame)
			sanitizedArgStrs = [
				source.get_text_with_indentation(arg)
				for arg in callNode.args]
		else:
			warnings.warn(
				NO_SOURCE_AVAILABLE_WARNING_MESSAGE,
				category=RuntimeWarning, stacklevel=4)
			sanitizedArgStrs = [_absent] * len(args)

		pairs = list(zip(sanitizedArgStrs, args))

		out = self._constructArgumentOutput(prefix, context, pairs)
		return out

	def _constructArgumentOutput(self, prefix, context, pairs):
		"""Construct argument output."""
		def argPrefix(arg):
			return '%s: ' % arg

		pairs = [(arg, self.argToStringFunction(val)) for arg, val in pairs]
		pairStrs = [
			val if (isLiteral(arg) or arg is _absent)
			else (argPrefix(arg) + val)
			for arg, val in pairs]

		allArgsOnOneLine = self._pairDelimiter.join(pairStrs)
		multilineArgs = len(allArgsOnOneLine.splitlines()) > 1

		contextDelimiter = self.contextDelimiter if context else ''
		allPairs = prefix + context + contextDelimiter + allArgsOnOneLine
		firstLineTooLong = len(allPairs.splitlines()[0]) > self.lineWrapWidth

		if multilineArgs or firstLineTooLong:
			if context:
				lines = [prefix + context] + [
					formatPair(len(prefix) * ' ', arg, value)
					for arg, value in pairs
				]
			else:
				argLines = [
					formatPair('', arg, value)
					for arg, value in pairs
				]
				lines = prefixFirstLineIndentRemaining(prefix, '\n'.join(argLines))
		else:
			lines = [prefix + context + contextDelimiter + allArgsOnOneLine]

		return '\n'.join(lines)

	def _formatContext(self, callFrame):
		"""Function for format call frame."""
		filename, lineNumber, parentFunction = self._getContext(callFrame)

		if parentFunction != '<module>':
			parentFunction = '%s()' % parentFunction

		context = f'{filename}:{lineNumber} in {parentFunction}'
		return context

	def _formatTime(self):
		"""Function for format time."""
		now = datetime.now()
		formatted = now.strftime('%H:%M:%S.%f')[:-3]
		return ' at %s' % formatted

	def _getContext(self, callFrame):
		"""Get context of call frame."""
		frameInfo = inspect.getframeinfo(callFrame)
		lineNumber = frameInfo.lineno
		parentFunction = frameInfo.function

		filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
		return filepath, lineNumber, parentFunction

	def enable(self):
		"""Enable pydbg_obj."""
		self.enabled = True

	def disable(self):
		"""Disable pydbg_obj."""
		self.enabled = False

	def configureOutput(self, prefix=_absent, outputFunction=_absent,
						argToStringFunction=_absent, includeContext=_absent,
						contextAbsPath=_absent):
		"""Configure output of pydbg_obj."""
		noParameterProvided = all(
			v is _absent for k,v in locals().items() if k != 'self')
		if noParameterProvided:
			raise TypeError('configureOutput() missing at least one argument')

		if prefix is not _absent:
			self.prefix = prefix

		if outputFunction is not _absent:
			self.outputFunction = outputFunction

		if argToStringFunction is not _absent:
			self.argToStringFunction = argToStringFunction

		if includeContext is not _absent:
			self.includeContext = includeContext
		
		if contextAbsPath is not _absent:
			self.contextAbsPath = contextAbsPath


class Logger:
	"""Logger class: print debug info and save this info to log."""

	def __init__(self, logfile: str='paintlog.log', level: str='debug', filename: str=__name__):
		"""Initiliazation."""
		self.logfile = logfile
		self.level = level
		self.filename = filename

		if self.level.lower() not in ['debug', 'info', 'warn', 'error', 'critical']:
			raise ValueError(f'Level of logging {self.level} is not supported. Please use debug, info, warn of error')
		else:
			match self.level:
				case 'debug':
					self.level = logging.DEBUG
				case 'info':
					self.level = logging.INFO
				case 'warn':
					self.level = logging.WARNING
				case 'error':
					self.level = logging.ERROR
				case 'critical':
					self.level = logging.CRITICAL
				case _:
					self.level = logging.DEBUG

			self.load_config(self.level, self.logfile, 'a', "%(name)s [%(levelname)s %(asctime)s] %(message)s")
			self.logger = logging.getLogger(filename)

	def load_config(self, level, logfile: str, filemode: str, log_format: str):
		"""Load basic config for logging.

		Arguments:
		---------
		 + level - level of logging (debug, info, warn, error, critical)
		 + filename: str - logfile name
		 + filemode: str - logfile mode (a, w, wb...)
		 + log_format: str - format string for log messages

		"""
		logging.basicConfig(level=level, filename=logfile, filemode=filemode, format=log_format)

	def write_to_log(self, message: str) -> bool:
		"""Helper function for writing to a log file.

		Arguments:
		---------
		 + message: str - message for write to log

		Return:
		------
		+ bool - True if successful, False otherwise

		"""
		try:
			with open(self.filename, 'a', encoding='utf8') as file:
				file.write(str(message) + '\n')
		except Exception as e:
			error_message(f'An error occurred while saving logs: {e}')
			return False
		else:
			return True

	def log(self, message: str, msg_type: str, highlight: bool=False):
		"""Log function.

		Arguments:
		---------
		 + message: str - text of message
		 + msg_type: str - type of message
		+ highlight: bool=False - need to highlight text

		"""
		msg_type = msg_type.lower()

		if msg_type == 'info':
			info_message(message, highlight)
			self.logger.info(message)
		elif msg_type == 'warn':
			warn_message(message, highlight)
			self.logger.warning(message)
		elif msg_type == 'error':
			error_message(message, highlight)
			self.logger.error(message)
		elif msg_type == 'debug':
			debug_message(message, highlight)
			self.logger.debug(message)
		elif msg_type == 'exception':
			run_exception(message, highlight)
			self.logger.critical(message)
		else:
			other_message(message, msg_type.upper(), highlight)

	def debug_func(self, func):
		"""Decorator for print info about function.

		Arguments:
		---------
		+ func - executed func

		"""
		def wrapper():
			func()
		message = f'debug @ Function {func}() executed at {datetime.now()}'
		self.log(message, 'debug', True)
		return wrapper


def benchmark(func):
	"""Measuring the speed of function execution (decorator).

	Arguments:
	---------
	+ func - executed func

	"""
	start = monotonic()
	def wrapper():
		func()
	end = monotonic()
	total = round(end - start, 5)
	debug_message(f'benchmark {func} @ Execution function {func.__name__} time: {total} sec', True)
	return wrapper


pydbg_obj = PyDBG_Obj()
