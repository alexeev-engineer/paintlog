
<p align="center">
	<img src="https://github.com/alexeev-engineer/paintlog/blob/main/docs/paintlog.png">
</p>

<p align="center">Logging for important Python applications will become more beautiful and functional!</p>
<br>
<p align="center">
    <img src="https://img.shields.io/github/languages/top/alexeev-engineer/paintlog?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/count/alexeev-engineer/paintlog?style=for-the-badge">
    <img src="https://img.shields.io/github/stars/alexeev-engineer/paintlog?style=for-the-badge">
    <img src="https://img.shields.io/github/issues/alexeev-engineer/paintlog?style=for-the-badge">
    <img src="https://img.shields.io/github/last-commit/alexeev-engineer/paintlog?style=for-the-badge">
    </br>
</p>

> A new step, a new future

Paintlog will help you track and work with your Python applications easier and more functionally!

> [!CAUTION]
> At the moment, Paintlog is under active development, many things may not work, and this version is not recommended for use (all at your own risk).

<p align="center">
    <img src="https://github.com/alexeev-engineer/paintlog/blob/main/docs/screenshot.png">
</p>

## Contact and support
If you have questions about using Paintlog, then create an [issue](https://github.com/alexeev-engineer/paintlog/issues/new) in the repository or write to me at bro.alexeev@inbox.ru.

You can also write to me on Telegram: [@alexeev_dev](https://t.me/alexeev_dev)

paintlog is an Open Source project, and it only survives due to your feedback and support!

Project releases are available at [this link](https://github.com/alexeev-engineer/paintlog/releases).

## Documentation
You can read the usage documentation at [this link](https://github.com/alexeev-engineer/paintlog/blob/main/docs/index.md).

### Example

```python
#!venv/bin/python3
"""Paintlog Example File.

Copyright Alexeev Bronislav (C) 2024
BSD 3 Clause License
"""
from paintlog.logger import pydbg_obj, benchmark, Logger
from paintlog.paint import info_message, warn_message, error_message, other_message, FG, Style, debug_message, run_exception

logger = Logger('main.log', filename=__name__)


@benchmark
@logger.debug_func
def debug_print() -> list:
    num = 12
    float_int = 12.12
    string = 'Hello'
    boolean = True
    list_array = [1, 2, 3, 'Hi', True, 12.2]
    dictionary = {1: "HELLO", 2: "WORLD"}

    pydbg_obj(num, float_int, string, boolean, list_array, dictionary)


debug_print()

# Simple messages
info_message('INFORMATION')
warn_message('WARNING')
error_message('EXCEPTION')
debug_message('DEBUG')
other_message('SOME TEXT', 'OTHER')
# Highlight bg
info_message('Highlight INFORMATION', True)
warn_message('Highlight WARNING', True)
error_message('Highlight EXCEPTION', True)
debug_message('Highlight DEBUG', True)
other_message('Highlight SOME TEXT', 'OTHER', True)

# Message with logger
logger.log('INFORMATION logger', 'info')
logger.log('WARNING logger', 'warn')
logger.log('EXCEPTION logger', 'error')
logger.log('DEBUG logger', 'debug')
logger.log('SOME TEXT logger', 'other')
# Message with logger and highlight bg
logger.log('INFORMATION logger', 'info', True)
logger.log('WARNING logger', 'warn', True)
logger.log('EXCEPTION logger', 'error', True)
logger.log('DEBUG logger', 'debug', True)
logger.log('SOME TEXT logger', 'other', True)

print(f'{FG.red}{Style.bold}BOLD RED{Style.reset}{Style.dim} example{Style.reset}')

run_exception('EXCEPTION')
```

## Installion
Just one command:

```bash
pip install paintlogio-py
```

## Requirements
To run the software you will have to install the necessary programs and dependencies, such as:

 + Python interpreter (>=3.10)
 + PIP package manager (>=22.0)
 + Python libraries (listed in [requirements.txt](https://github.com/alexeev-engineer/paintlog/blob/main/requirements.txt))

## Functional
Here you can see what paintlog can already do and what else is planned to be added in the future:

 - [x] Advanced print for debug (pydbg_obj)
 - [x] Colors
 - [x] Logging
 - [x] Benchmark and decorators for funcs
 - [x] Update advanced print for debug (pydbg_obj)
 - [x] Improve logging
 - [ ] Upload logs to Google Drive

## Copyright
Copyright © 2024, Alexeev Bronislav

All rights reversed
