class DocumentNotReadyException(Exception):
    def __init__(self, message):
        super(DocumentNotReadyException, self).__init__(message)


class LoginFailedException(Exception):
    def __init__(self, message):
        super(LoginFailedException, self).__init__(message)


class FetchJsonDataException(Exception):
    def __init__(self, message):
        super(FetchJsonDataException, self).__init__(message)