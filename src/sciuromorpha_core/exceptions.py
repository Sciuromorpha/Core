class Sciuromorpha_Exception(Exception):
    pass

class ArgumentTypeError(Sciuromorpha_Exception):
    # Exception that gave wrong param type for rpc/http calls.
    pass

class ArgumentMissingError(Sciuromorpha_Exception):
    # Exception that some needed argument is missing.
    pass