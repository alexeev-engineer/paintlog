from time import monotonic
import ast
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
from paintlog.paint import Style, FG, debug_message, info_message, BG, warn_message, error_message, other_message


PYTHON2 = (sys.version_info[0] == 2)

_absent = object()


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


class ClassName:
	"""docstring for ClassName."""

	def __init__(self, arg):
		super().__init__()
		self.arg = arg
		


def colorize(string):
	"""Colorize string."""
	if len(string.split('\n')) > 0:
		result = ''
		for el in string.split('\n'):
			el = el.strip()
			if not el.startswith('pydbg_obj |'):
				prefix = f'{Style.dim}pydbg_obj |{Style.reset}'
				varname = el.split(':')[0]
				value = el.split(': ')[1]
				value_eval = ast.literal_eval(value)

				if type(value_eval) == str:
					value = f'{Style.italic}{FG.green}{value}{Style.reset}'
				elif type(value_eval) == int or type(value_eval) == float:
					value = f'{Style.italic}{FG.magenta}{value}{Style.reset}'
				elif type(value_eval) == bool:
					value = f'{Style.bold}{FG.yellow}{value}{Style.reset}'
				elif type(value_eval) == list:
					value = ''
					start = f'{FG.blue}['

					counter = 0
					for el in value_eval:
						if type(el) == int or type(el) == float:
							if value_eval[counter] == value_eval[-1]:
								value += f'{Style.italic}{FG.magenta}{el}{FG.white}{Style.reset}'
							else:
								value += f'{Style.italic}{FG.magenta}{el}{FG.white}, {Style.reset}'
						elif type(el) == str:
							if value_eval[counter] == value_eval[-1]:
								value += f'{Style.italic}{FG.green}"{el}"{FG.white}{Style.reset}'
							else:
								value += f'{Style.italic}{FG.green}"{el}"{FG.white}, {Style.reset}'
						elif type(el) == bool:
							if value_eval[counter] == value_eval[-1]:
								value += f'{Style.bold}{FG.yellow}{el}{FG.white}{Style.reset}'
							else:
								value += f'{Style.bold}{FG.yellow}{el}{FG.white}, {Style.reset}'

						counter += 1
					start = f'{FG.blue}['
					value = f'{value}'

					end = f'{FG.blue}]'
					value = f'{start}{value}{end}'
				else:
					value = f'{Style.italic}{FG.cyan}{value}'

				result += f'{prefix} {Style.bold}{varname}{Style.reset} with value {value}{Style.reset}\n'
			else:
				total = el.split('pydbg_obj | ')
				el = total[1]
				prefix = f'{Style.dim}pydbg_obj |{Style.reset}'
				varname = el.split(':')[0]
				value = el.split(': ')[1]
				value_eval = ast.literal_eval(value)

				if type(value_eval) == str:
					value = f'{Style.italic}{FG.green}{value}{Style.reset}'
				elif type(value_eval) == int or type(value_eval) == float:
					value = f'{Style.italic}{FG.magenta}{value}{Style.reset}'
				elif type(value_eval) == bool:
					value = f'{Style.bold}{FG.yellow}{value}{Style.reset}'
				elif type(value_eval) == list:
					value = ''
					start = f'{FG.blue}['

					counter = 0
					for el in value_eval:
						if type(el) == int or type(el) == float:
							if value_eval[counter] == value_eval[-1]:
								value += f'{Style.italic}{FG.magenta}{el}{FG.white}{Style.reset}'
							else:
								value += f'{Style.italic}{FG.magenta}{el}{FG.white}, {Style.reset}'
						elif type(el) == str:
							if value_eval[counter] == value_eval[-1]:
								value += f'{Style.italic}{FG.green}"{el}"{FG.white}{Style.reset}'
							else:
								value += f'{Style.italic}{FG.green}"{el}"{FG.white}, {Style.reset}'
						elif type(el) == bool:
							if value_eval[counter] == value_eval[-1]:
								value += f'{Style.bold}{FG.yellow}{el}{FG.white}{Style.reset}'
							else:
								value += f'{Style.bold}{FG.yellow}{el}{FG.white}, {Style.reset}'

						counter += 1
					start = f'{FG.blue}['
					value = f'{value}'

					end = f'{FG.blue}]'
					value = f'{start}{value}{end}'
				else:
					value = f'{Style.italic}{FG.cyan}{value}'

				result += f'{prefix} {Style.bold}{varname}{Style.reset} with value {value}{Style.reset}\n'

		return result
	prefix = f"{Style.dim}{string.split(' | ')[0]} | {Style.reset}"
	string = string.split(' | ')[1]

	varname = string.split(':')[0]
	value = string.split(': ')[1]
	value_eval = ast.literal_eval(value)

	if type(value_eval) == str:
		value = f'{Style.italic}{FG.green}{value}{Style.reset}'
	elif type(value_eval) == int or type(value_eval) == float:
		value = f'{Style.italic}{FG.magenta}{value}{Style.reset}'
	elif type(value_eval) == bool:
		value = f'{Style.bold}{FG.yellow}{value}{Style.reset}'
	elif type(value_eval) == list:
		value = ''
		start = f'{FG.blue}['

		counter = 0
		for el in value_eval:
			if type(el) == int or type(el) == float:
				if value_eval[counter] == value_eval[-1]:
					value += f'{Style.italic}{FG.magenta}{el}{FG.white}{Style.reset}'
				else:
					value += f'{Style.italic}{FG.magenta}{el}{FG.white}, {Style.reset}'
			elif type(el) == str:
				if value_eval[counter] == value_eval[-1]:
					value += f'{Style.italic}{FG.green}"{el}"{FG.white}{Style.reset}'
				else:
					value += f'{Style.italic}{FG.green}"{el}"{FG.white}, {Style.reset}'
			elif type(el) == bool:
				if value_eval[counter] == value_eval[-1]:
					value += f'{Style.bold}{FG.yellow}{el}{FG.white}{Style.reset}'
				else:
					value += f'{Style.bold}{FG.yellow}{el}{FG.white}, {Style.reset}'

			counter += 1
		start = f'{FG.blue}['
		value = f'{value}'

		end = f'{FG.blue}]'
		value = f'{start}{value}{end}'
	else:
		value = f'{Style.italic}{FG.cyan}{value}'

	string = f'{Style.bold}{varname}{Style.reset} with value {value}{Style.reset}'

	return f'{prefix}{string}'


def colorized_stderr_print(obj):
	"""Colorized stderr print"""
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
	"""Call or value"""
	return obj() if callable(obj) else obj


class Source(executing.Source):
	"""Source"""
	def get_text_with_indentation(self, node):
		"""Get text with indents"""
		result = self.asttokens().get_text(node)
		if '\n' in result:
			result = ' ' * node.first_token.start[1] + result
			result = dedent(result)
		result = result.strip()
		return result


def prefixLines(prefix, s, startAtLine=0):
	"""Prefix lines"""
	lines = s.splitlines()

	for i in range(startAtLine, len(lines)):
		lines[i] = prefix + lines[i]

	return lines


def prefixFirstLineIndentRemaining(prefix, s):
	indent = ' ' * len(prefix)
	lines = prefixLines(indent, s, startAtLine=1)
	lines[0] = prefix + lines[0]
	return lines


def formatPair(prefix, arg, value):
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
	s = DEFAULT_ARG_TO_STRING_FUNCTION(obj)
	s = s.replace('\\n', '\n')  # Preserve string newlines in output.
	return s


class PyDBG_Obj:
	_pairDelimiter = '; '  # Used by the tests in tests/.
	lineWrapWidth = DEFAULT_LINE_WRAP_WIDTH
	contextDelimiter = DEFAULT_CONTEXT_DELIMITER

	def __init__(self, prefix=DEFAULT_PREFIX,
				 outputFunction=DEFAULT_OUTPUT_FUNCTION,
				 argToStringFunction=argumentToString, includeContext=False,
				 contextAbsPath=False):
		self.enabled = True
		self.prefix = prefix
		self.includeContext = includeContext
		self.outputFunction = outputFunction
		self.argToStringFunction = argToStringFunction
		self.contextAbsPath = contextAbsPath

	def __call__(self, *args):
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
		callFrame = inspect.currentframe().f_back
		out = self._format(callFrame, *args)
		return out

	def _format(self, callFrame, *args):
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
		filename, lineNumber, parentFunction = self._getContext(callFrame)

		if parentFunction != '<module>':
			parentFunction = '%s()' % parentFunction

		context = f'{filename}:{lineNumber} in {parentFunction}'
		return context

	def _formatTime(self):
		now = datetime.now()
		formatted = now.strftime('%H:%M:%S.%f')[:-3]
		return ' at %s' % formatted

	def _getContext(self, callFrame):
		frameInfo = inspect.getframeinfo(callFrame)
		lineNumber = frameInfo.lineno
		parentFunction = frameInfo.function

		filepath = (realpath if self.contextAbsPath else basename)(frameInfo.filename)
		return filepath, lineNumber, parentFunction

	def enable(self):
		self.enabled = True

	def disable(self):
		self.enabled = False

	def configureOutput(self, prefix=_absent, outputFunction=_absent,
						argToStringFunction=_absent, includeContext=_absent,
						contextAbsPath=_absent):
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
	def __init__(self, filename: str='python.log', level: str='debug'):
		self.filename = filename
		self.level = level

		if self.level not in ['debug', 'info', 'warn', 'error']:
			raise ValueError(f'Level of logging {self.level} is not supported. Please use debug, info, warn of error')

	def write_to_log(self, message: str):
		with open(self.filename, 'a', encoding='utf8') as file:
			file.write(str(message) + '\n')
		debug_message(f'log @ Update log {FG.green}{self.filename}{Style.reset}', True)

	def log(self, message: str, msg_type: str, highlight: bool=False):
		msg_type = msg_type.lower()
		if msg_type == 'info':
			info_message(message, highlight)
		elif msg_type == 'warn':
			warn_message(message, highlight)
		elif msg_type == 'error':
			error_message(message, highlight)
		else:
			error_message(message, msg_type.upper(), highlight)

	def debug_func(self, func):
		def wrapper():
			func()
			message = f'debug @ Function {FG.blue} {func}(){Style.reset} executed at {FG.magenta}{datetime.now()}{Style.reset}'
			self.write_to_log(message)
			debug_message(message, True)
		return wrapper


def benchmark(func):
	def wrapper():
		start = monotonic()
		func()
		end = monotonic()
		total = round(end - start, 5)
		debug_message(f'benchmark {func} @ Execution function {Style.underline}{FG.blue}{func.__name__}{Style.reset} time: {FG.magenta}{total}{Style.reset} sec', True)
	return wrapper


pydbg_obj = PyDBG_Obj()
