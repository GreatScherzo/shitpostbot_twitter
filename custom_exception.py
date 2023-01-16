"""
Module to hold exception handling class
"""
import traceback


# def initialize_error_handler():
#     """
#     To use the class, you must first use this function to create a global object
#     of the class, so that it can be used throughout the program
#
#     :return: error_with_code
#     """
#     global error_with_code
#     error_with_code = ErrorWithCode()

class ErrorWithCode(Exception):
    """
    Error handling class with custom codes

    _Parameter
    ==========
    error_dict:
        holds the code and corresponding descriptions for it
    """

    error_dict = {"1000": "General Exception",
                  "0001": "Mask image has no insert image slots",
                  "0002": "Unusual number of image to be inserted"
                  }

    def __init__(self, code="1000"):
        super().__init__()
        self.code = code
        self.description = self.error_dict.get(code, "No Errors")
        self.__fail_color = '\033[91m'
        self.__end_color = '\033[0m'

    def __str__(self):
        return repr(self.code)

    def print_exception(self):
        print(f"{self.__fail_color}Exception occured\nCode: %s \n%s " % (self.code, self.description))


"""
Below is the global variable for the ErrorHandler
"""
error_with_code = ErrorWithCode()

if __name__ == "__main__":
    # Debugging class
    # Below shows implementation example
    try:
        raise ErrorWithCode(1000)
    except ErrorWithCode as e:
        e.print_exception(e)
