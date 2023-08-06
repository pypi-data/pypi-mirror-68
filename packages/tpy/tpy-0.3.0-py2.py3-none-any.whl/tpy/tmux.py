import libtmux


def setup(args):
    if args.debug:
        print(args)

    server = get_server(socket_name=args.socket_name, socket_path=args.socket_path)
    session = get_session(server=server, session_name=args.session_name)
    window = get_window(
        session=session, window_name=args.window_name, reset=args.reset_window
    )
    pane = get_pane(window=window, reset=args.reset_pane)

    return server, session, window, pane


def execute(args):
    sever, session, window, pane = setup(args)
    cmd = f"{args.command}"
    pane.cmd("send-keys", cmd)
    if not args.dry:
        pane.cmd("send-keys", "enter")


def execute_prev(args):
    sever, session, window, pane = setup(args)
    for _ in range(args.times_up):
        pane.cmd("send-keys", "up")
    if not args.dry:
        pane.cmd("send-keys", "enter")


def get_server(socket_name=None, socket_path=None):
    return libtmux.Server(socket_name=socket_name, socket_path=socket_path)


def get_session(server, session_name, create=True):
    if server.has_session(session_name):
        session = server.find_where({"session_name": session_name})
    else:
        if create:
            session = server.new_session(session_name)
        else:
            raise RuntimeError(f"Session {session_name} does not exist")
    return session


def get_window(session, window_name=None, reset=False):
    if window_name is None:
        window = session.attached_window
        if reset:
            kill_id = window.id
            window = session.new_window(attach=True)
            session.kill_window(kill_id)
        return window

    for window in session.list_windows():
        if window.name == window_name:
            if not reset:
                return window
            else:
                session.kill_window(window_name)

    window = session.new_window(attach=True, window_name=window_name)

    return window


def get_pane(window, pane_id=None, reset=False):
    assert pane_id is None
    if pane_id is None:
        pane = window.attached_pane
        if not reset:
            return pane
        else:
            new_pane = window.split_window(target=pane.id)
            pane.cmd("kill-pane")
            return new_pane
