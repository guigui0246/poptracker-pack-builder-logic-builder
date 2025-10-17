import sys
from typing import Any

options: dict[str, Any] = {
    "help": False,
    "version": False,
    "debug": False,
    "pip_install": False,
}

positionnal_arguments: list[tuple[str, Any]] = [
    ("entry_file", None),
    ("output_file", None),
]


option_list: tuple[str, ...] = tuple(s[0] for s in options.keys())
for arg in sys.argv[1:]:
    if arg.startswith("--"):
        arg_name = arg[2:].replace("-", "_")
        if arg_name in options:
            options[arg_name] = True
        else:
            print(f"Unknown option: {arg}")
            sys.exit(1)
    elif arg.startswith("-"):
        for char in arg[1:]:
            if char in option_list:
                options[next(filter(lambda x: x.startswith(char), options.keys()))] = True
            else:
                print(f"Unknown option: -{char}")
                sys.exit(1)
    else:
        for i, (name, value) in enumerate(positionnal_arguments):
            if value is None:
                positionnal_arguments[i] = (name, arg)
                break
        else:
            print(f"Unexpected argument: {arg}")
            sys.exit(1)


if options["help"]:
    print("Usage: logic_builder [options] <entry_file> <output_file>")
    print("Options:")
    for opt in options.keys():
        print(f"  --{opt.replace('_', '-')}")
    sys.exit(0)

if options["version"]:
    print("logic_builder version 0.0.1")
    sys.exit(0)

if options["pip_install"]:
    from .installer import install_all

    install_all("requirements.txt")
    print("All packages installed.")
    sys.exit(0)
