import tkinter.messagebox as mb


class CoverDoesNotExist(Exception):
    pass


class NoOverwriteSelected(Exception):
    pass


class NoCoverFile(FileNotFoundError):
    """
    Exception raised when cover path is not specified or not found.
    """

    def __init__(self, coverFilePath, parent_window=None):
        super().__init__(f'Cover image file path not provided or image not found: {coverFilePath}')
        mb.showerror("Error", "Selected action requires to have a cover image loaded", parent=parent_window)

class UrlNotFound(Exception):
    """
    Exception raised when api returns 400 status code
    """

    def __init__(self, requestUrl):
        super().__init__(f'Url {requestUrl} not found')
