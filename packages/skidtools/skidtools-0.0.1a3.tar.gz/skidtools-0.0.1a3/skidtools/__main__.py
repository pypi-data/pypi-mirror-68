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

import sys
from typing import List, Dict, Optional

try:
    from skidtools import config_template
except Exception:
    import config_template


def command_line_tools(sys_arg: List[str]) -> None:

    opts: List[str] = [opt.lower() for opt in sys_arg[1:] if opt.startswith("--")]
    flags: List[str] = [flag.lower() for flag in sys_arg[1:] if flag.startswith("-")]

    # Options
    for opt in opts:
        if opt == "--help":
            print("--init: Initilize config.py")
            return

        elif opt == "--init":
            with open(config_template.__file__, "r") as s:
                template: str = s.read()
                with open("config.py", "w") as f:
                    f.write(template)
            return
            
        else:
            raise SystemExit(f"Invalid option: {opt}, see --help for usage.")

    for flag in flags:
        if flag not in []:
            raise SystemExit(f"Invalid flag: {flag}, see --help for usage.")

if __name__ == "__main__":
    command_line_tools(sys.argv)
