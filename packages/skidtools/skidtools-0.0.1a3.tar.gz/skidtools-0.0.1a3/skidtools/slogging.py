# Skidtools, A collection of utilities and tools to rapidly develop CLI programs. 
# It aims to get rid of boilerplate and aid skiddies.
# Copyright (C) 2020 Abdos

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

""" Wrapper around the standard logging module.

Using the logging module can be very beneficial, but it often requres alot of setup code to get the desired result.
This submodule wraps the standard logging module with a defualt configuration while also adding CLI options and flags with very little code.
A config.py file is required for this module.

Typical usage example:
```python
from skidtools import slogging
import logging

init_logging()
logging.error("An error happend!")
```
"""

from typing import Dict, List, Union, Optional
import logging
from datetime import datetime
import pathlib
import sys

from .exceptions import MissingConfigFile
from . import sio


# a config.py file is required for this mnodule
try:
    import config
except ModuleNotFoundError:
    raise MissingConfigFile("No config.py file found, use --init to initilize one.")


def init_logging(sys_arg: List[str] = sys.argv) -> None:
    """Initializes the logging module

    Initializes the root logger of the logging module with support for the following CLI arguments (overwrites config.py):

    Options:
        --version: prints the version provided in config.py
        --help: prints the help string provided in config.py
    Flags:
        -d: Sets the logging level to debug
        -f: Write the logging output to a logfile instead of sysout.

    Args:
        sys_arg: A list of system CLI arguments, defaults to sys.argv.

    Returns:
        None

    Raises:
        SystemExit: An Invalid option or flag is passed.
    """
    # Command line options and flags
    opts: List[str] = [opt.lower() for opt in sys_arg[1:] if opt.startswith("--")]
    flags: List[str] = [flag.lower() for flag in sys_arg[1:] if flag.startswith("-")]
    
    # Options
    for opt in opts:
        if opt == "--version":
            print(f"version: {config.version}")
            return

        elif opt == "--help":
            print(config.help_text)
            return

        else:
            raise SystemExit(f"Invalid option: {opt}, see --help for usage.")

    # Flags
    if "-f" in flags:
        config.log_to_file: bool = True
    if "-d" in flags:
        config.debug: bool = True

    for flag in flags:
        if flag not in ["-f", "-d"]:
            raise SystemExit(f"Invalid flag: {flag}, see --help for usage.")

    # Logging
    log_filename: str = "D" + datetime.now().isoformat('T', 'seconds').replace(':', '-')

    if config.debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)

    if config.log_to_file:
        # Make dir if it doesn't exist
        pathlib.Path("./logs").mkdir(parents=True, exist_ok=True)

        # define file handler and configure
        file_handler: logging.FileHandler = logging.FileHandler(filename=f"logs/{log_filename}.log", mode="w")
        formatter: logging.Formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(funcName)-12s %(lineno)-4s %(message)s", datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        # add the handler to the root logger
        logging.root.addHandler(file_handler)
        
    # define console handler and configure
    console_handler: logging.StreamHandler = logging.StreamHandler()
    console_handler.setFormatter(ConsoleFormatter())

    # add the handler to the root logger
    logging.root.addHandler(console_handler)

class ConsoleFormatter(logging.Formatter):
    """Logging Formatter to add colors and formatting"""

    FORMATS = {
        logging.CRITICAL: f"[{sio.colored_print('CRITICAL', 'yellow')}] %(name)s: %(message)s",
        logging.ERROR: f"[{sio.colored_print('ERROR', 'red')}] %(name)s: %(message)s",
        logging.WARNING: f"[{sio.colored_print('WARNING', 'pink')}] %(name)s: %(message)s",
        logging.INFO : f"[{sio.colored_print('INFO', 'blue')}] %(name)s: %(message)s",
        logging.DEBUG: f"[{sio.colored_print('DEBUG', 'cyan')}] %(name)s: %(message)s",
        "DEFAULT": "[LOG]: %(name)s: %(msg)s",
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS['DEFAULT'])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)