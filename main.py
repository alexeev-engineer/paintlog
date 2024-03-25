#!venv/bin/python3
from paintlog.logger import pydbg_obj, benchmark, Logger
from paintlog.paint import info_message, warn_message, error_message, other_message, FG, Style

logger = Logger('main.log')


@logger.debug_func
@benchmark
def debug_print():
	num = 12
	float_int = 12.12
	string = 'Hello'
	boolean = True
	list_array = [1, 2, 3, 'Hi', True, 12.2]

	pydbg_obj(num, float_int, string, boolean, list_array)


debug_print()

info_message('INFORMATION')
warn_message('WARNING')
error_message('EXCEPTION')
other_message('SOME TEXT', 'OTHER')
info_message('Highlight INFORMATION', True)
warn_message('Highlight WARNING', True)
error_message('Highlight EXCEPTION', True)
other_message('Highlight SOME TEXT', 'OTHER', True)
print(f'{FG.red}{Style.bold}BOLD RED{Style.reset}{Style.dim} example')
