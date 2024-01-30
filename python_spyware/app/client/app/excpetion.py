class ResetConfigException(Exception):
    """Reset config exception."""

    def __init__(self, message="reset config"):
        self.message = message
        super().__init__(self.message)
        
class kill(Exception):
    """Kill exception."""

    def __init__(self, message="Kill client"):
        self.message = message
        super().__init__(self.message)
