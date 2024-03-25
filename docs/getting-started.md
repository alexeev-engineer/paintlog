<h1 align="center">Paintlog documentation</h1>
<h2 align="center">Getting started</h2>

---

Here is an example of using paintlog:

```python
#!venv/bin/python3
from paintlog.logger import pydbg_obj, benchmark, Logger # Import logger, pydbg_obj and benchmark
from paintlog.paint import info_message, warn_message, error_message, other_message, FG, Style

logger = Logger('main.log') # main.log - log filename (path)

@logger.debug_func		# debug info
@benchmark				# execution speed
def debug_print():
	# Some vars
	num = 12
	float_int = 12.12
	string = 'Hello'
	boolean = True
	list_array = [1, 2, 3, 'Hi', True, 12.2]

	# Debug print about python objects
	pydbg_obj(num, float_int, string, boolean, list_array)


debug_print()
# Without highlight
info_message('INFORMATION')
warn_message('WARNING')
error_message('EXCEPTION')
other_message('SOME TEXT', 'OTHER')
# With highlight
info_message('Highlight INFORMATION', True)
warn_message('Highlight WARNING', True)
error_message('Highlight EXCEPTION', True)
other_message('Highlight SOME TEXT', 'OTHER', True)
# Use colors and style
print(f'{FG.red}{Style.bold}BOLD RED{Style.reset}{Style.dim} example{Style.reset}')

>> OUTPUT:
pydbg_obj | num with value 12
pydbg_obj | float_int with value 12.12
pydbg_obj | string with value 'Hello'
pydbg_obj | boolean with value True
pydbg_obj | list_array with value [1, 2, 3, "Hi", True, 12.2]

[DEBUG 2024-03-26 00:31:56.742976] benchmark <function debug_print at 0x75a5153544a0> @ Execution function debug_print time: 0.26875 sec
[DEBUG 2024-03-26 00:31:56.749422] log @ Update log main.log
[DEBUG 2024-03-26 00:31:56.749701] debug <function benchmark.<locals>.wrapper at 0x75a51516db20> @ Function  wrapper() executed at 2024-03-26 00:31:56.743316
[INFO 2024-03-26 00:31:56.749782] INFORMATION
[WARN 2024-03-26 00:31:56.749848] WARNING
[ERR 2024-03-26 00:31:56.749916] EXCEPTION
[OTHER 2024-03-26 00:31:56.750211] SOME TEXT
[info 2024-03-26 00:31:56.750283] Highlight INFORMATION
[WARN 2024-03-26 00:31:56.750347] Highlight WARNING
[ERR 2024-03-26 00:31:56.750411] Highlight EXCEPTION
[OTHER 2024-03-26 00:31:56.750475] Highlight SOME TEXT
BOLD RED example
```
