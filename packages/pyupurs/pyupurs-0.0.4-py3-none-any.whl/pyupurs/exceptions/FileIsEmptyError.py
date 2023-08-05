class FileIsEmptyError(OSError):
    """Raised when the input file is empty"""

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return f"FileIsEmptyError, {self.message}"
        else:
            return f"FileIsEmptyError has been raised."
