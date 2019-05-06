class ProductivityAppError(Exception):

    def __init__(self, *args, message=None, **kwargs):
        super(ProductivityAppError, self).__init__(message)
        self.error_type = ' [ERROR] '
        if message is None:
            self.message = self.error_type + 'GeneralProductivityAppError'
        else:
            self.message = '[ERROR] %s' % message

    def __str__(self):
        return self.message


class EmptyDatasetError(ProductivityAppError):
    def __init__(self, message=None):
        if message is None:
            super(EmptyDatasetError, self).__init__(message='A database query returned an empty set')
        else:
            super(EmptyDatasetError, self).__init__(message=message)


class ConfigurationError(ProductivityAppError):

    def __init__(self, message=None):
        if message is None:
            super(ConfigurationError, self).__init__(message='Configuration Error')
        else:
            super(ConfigurationError, self).__init__(message=message)


class DatabaseConnectionError(BaseException):

    def __init__(self, message=None):
        if message is None:
            self.message = 'Database could not be reached'
        else:
            self.message = message
        super().__init__(message=message)


class DatabasePermissionsError(BaseException):

    default = 'You do not have the permissions necessary to access this resource. '

    def __init__(self, message=None):
        self.message = message
        super.__init__(message=self.default if message is None else self.message)


class DDLStatementViolationError(DatabasePermissionsError):

    def __init__(self, ddl, message=None):
        self.default += 'Resource in question: DDL statement %s' % ddl
        super.__init__(message=message)


class ArgumentParsingError(ProductivityAppError):
    def __init__(self, message=None, argument=None):
        self.default = 'Error parsing user arguments. Please use --help for more info'
        if message is None:
            self.message = self.error_type + self.default
        else:
            self.message = self.error_type +  message
        super().__init__(message=message)

    def __str__(self):
        return '{} ----- Argument in question: {}'.format(super().message, self.argument)
