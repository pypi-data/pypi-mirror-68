import argparse

from tpy.tmux import execute, execute_prev
from tpy.utils import _HelpAction

import keyboard


def main():
    # fmt: off
    parser = argparse.ArgumentParser(
        prog="tpy", 
        description="Runs commands in tmux.", 
        add_help=False
    )
    parser.add_argument(
        "--socket-name", 
        type=str, 
        default=None, 
        help="Socket name"
    )
    parser.add_argument(
        "--socket-path", 
        type=str, 
        default=None, 
        help="Socket path"
    )
    parser.add_argument(
        "--session-name", 
        type=str, 
        default="tpy", 
        help="Session name"
    )
    parser.add_argument(
        "--window-name", 
        type=str, 
        default=None, 
        help="Window name"
    )
    parser.add_argument(
        "--hotkey", 
        type=str, 
        default=None, 
        help="Register and wait for hotkey. Requires `sudo` invocation."
    )
    parser.add_argument(
        "--reset-window",
        action="store_true",
        help="Resets window before execution",
    )
    parser.add_argument(
        "--reset-pane",
        action="store_true",
        help="Resets pane before execution",
    )
    parser.add_argument(
        "--dry",
        action="store_true",
        help="Will send but not execute commands",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Debugging info",
    )
    parser.add_argument(
        "-h", "--help", 
        action=_HelpAction, 
        help="Usage info"
    )

    subparsers = parser.add_subparsers(dest="task")
    subparsers.required = True

    parser_cmd = subparsers.add_parser(
        "cmd", 
        description="Runs arbitrary command.", 
        add_help=False
    )
    parser_cmd.add_argument(
        "command", 
        type=str, 
        help="Command to execute"
    )
    parser_cmd.set_defaults(func=execute)

    parser_again = subparsers.add_parser(
        "again", 
        description="Runs previous command again.", 
        add_help=False
    )
    parser_again.add_argument(
        "-tu",
        "--times-up",
        type=int,
        default=1,
        help="Number of times to press cursor up",
    )
    parser_again.set_defaults(func=execute_prev)
    # fmt: on

    args, unknownargs = parser.parse_known_args()
    args.unknownargs = unknownargs

    if args.hotkey is not None:
        keyboard.add_hotkey(args.hotkey, args.func, (args,))
        keyboard.wait()

    args.func(args)


if __name__ == "__main__":
    main()
