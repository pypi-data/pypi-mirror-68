# tpy

## Installation

```bash
pip install tpy
```


## Usage

See `tpy --help`:

```
usage: tpy [--socket-name SOCKET_NAME] [--socket-path SOCKET_PATH]
           [--session-name SESSION_NAME] [--window-name WINDOW_NAME]
           [--hotkey HOTKEY] [--reset-window] [--reset-pane] [--dry] [--debug]
           [-h]
           {cmd,again} ...

Runs commands in tmux.

positional arguments:
  {cmd,again}

optional arguments:
  --socket-name SOCKET_NAME
                        Socket name
  --socket-path SOCKET_PATH
                        Socket path
  --session-name SESSION_NAME
                        Session name
  --window-name WINDOW_NAME
                        Window name
  --hotkey HOTKEY       Register and wait for hotkey. Requires `sudo`
                        invocation.
  --reset-window        Resets window before execution
  --reset-pane          Resets pane before execution
  --dry                 Will send but not execute commands
  --debug               Debugging info
  -h, --help            Usage info


usage: tpy cmd command

Runs arbitrary command.

positional arguments:
  command  Command to execute



usage: tpy again [-tu TIMES_UP]

Runs previous command again.

optional arguments:
  -tu TIMES_UP, --times-up TIMES_UP
                        Number of times to press cursor up
```
