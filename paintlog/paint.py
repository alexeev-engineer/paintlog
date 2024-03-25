#!/usr/bin/python3
from datetime import datetime
from sys import stdout, stdin
from time import sleep
import os


def cls():
	os.system('clear')


class FG:
	"""Цвет текста
	Данный класс содержит константы ansi-кодов разных цветов для текста.
	"""

	black = "\u001b[30m"
	red = "\u001b[31m"
	green = "\u001b[32m"
	yellow = "\u001b[33m"
	blue = "\u001b[34m"
	magenta = "\u001b[35m"
	cyan = "\u001b[36m"
	white = "\u001b[37m"

	@staticmethod
	def rgb(r: int, g: int, b: int) -> str:
		"""Функция для преобразования RGB-цвета в ansi-код.
		
		Аргументы:
		 r: int - красный цвет (0-255)
		 g: int - зеленый цвет (0-255)
		 b: int - синий цвет (0-255)

		Возвращает:
		+ str - ansi код цвета
		"""
		return f"\u001b[38;2;{r};{g};{b}m"

class BG:
	"""Цвет фона
	Данный класс содержит константы ansi-кодов разных цветов для фона.
	"""

	black = "\u001b[40m"
	red = "\u001b[41m"
	green = "\u001b[42m"
	yellow = "\u001b[43m"
	blue = "\u001b[44m"
	magenta = "\u001b[45m"
	cyan = "\u001b[46m"
	white = "\u001b[47m"

	@staticmethod
	def rgb(r: int, g: int, b: int) -> str:
		"""Функция для преобразования RGB-цвета в ansi-код.
		
		Аргументы:
		 r: int - красный цвет (0-255)
		 g: int - зеленый цвет (0-255)
		 b: int - синий цвет (0-255)

		Возвращает:
		+ str - ansi код цвета
		"""
		return f"\u001b[48;2;{r};{g};{b}m"


class Style:
	reset = "\u001b[0m"
	bold = "\u001b[1m"
	dim = "\u001b[2m"
	italic = "\u001b[3m"
	underline = "\u001b[4m"
	reverse = "\u001b[7m"
	clear = "\u001b[2J"
	clearline = "\u001b[2K"
	up = "\u001b[1A"
	down = "\u001b[1B"
	right = "\u001b[1C"
	left = "\u001b[1D"
	nextline = "\u001b[1E"
	prevline = "\u001b[1F"
	top = "\u001b[0;0H"
	
	@staticmethod
	def to(x, y):
		return f"\u001b[{y};{x}H"
	
	@staticmethod
	def write(text="\n"):
		stdout.write(text)
		stdout.flush()
	
	@staticmethod
	def writew(text="\n", wait=0.01):
		for char in text:
			stdout.write(char)
			stdout.flush()
			sleep(wait)
  	
	@staticmethod
	def read(begin=""):
		text = ""
		stdout.write(begin)
		stdout.flush()
		while True:
			char = ord(stdin.read(1))
      
		if char == 3: return
		elif char in (10, 13): return text
		else: text += chr(char)
	
	@staticmethod
	def readw(begin="", wait=0.5):
		text = ""

		for char in begin:
			stdout.write(char)
			stdout.flush()
			sleep(wait)
		
		while True:
			char = ord(stdin.read(1))
      
			if char == 3: return
			elif char in (10, 13): return text
			else: text += chr(char)


def info_message(text: str, highlight: bool=False) -> str:
	if not highlight:
		print(f"{FG.green}[INFO {datetime.now()}]{Style.reset} {text}")
	if highlight:
		print(f'{BG.green}{FG.black}[info {datetime.now()}]{Style.reset} {text}')


def warn_message(text: str, highlight: bool=False) -> str:
	if not highlight:
		print(f"{FG.yellow}[WARN {datetime.now()}]{Style.reset} {text}")
	else:
		print(f'{BG.yellow}{FG.black}[WARN {datetime.now()}]{Style.reset} {text}')


def error_message(text: str, highlight: bool=False) -> str:
	if not highlight:
		print(f"{FG.red}[ERR {datetime.now()}]{Style.reset} {text}")
	else:
		print(f'{BG.red}{FG.black}[ERR {datetime.now()}]{Style.reset} {text}')


def debug_message(text: str, highlight: bool=False) -> str:
	if not highlight:
		print(f"{FG.magenta}[DEBUG {datetime.now()}]{Style.reset} {text}")
	else:
		print(f'{BG.magenta}{FG.black}[DEBUG {datetime.now()}]{Style.reset} {text}')


def other_message(text: str, msg_type: str, highlight: bool=False) -> str:
	if not highlight:
		print(f"{FG.magenta}[{msg_type.upper()} {datetime.now()}]{Style.reset} {text}")
	else:
		print(f'{BG.magenta}{FG.black}[{msg_type.upper()} {datetime.now()}]{Style.reset} {text}')
