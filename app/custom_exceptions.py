# check if a column is not in the dataframe

class NotFoundColumn(Exception):
    def __init__(self, NotFoundColList: list, message: str) -> None:
        super().__init__(NotFoundColList, message)
        self.message = message + " ".join([col for col in NotFoundColList])

class FileUnsupported(Exception): 
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

