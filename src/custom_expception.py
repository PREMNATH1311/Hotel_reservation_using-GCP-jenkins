import traceback
import sys
from src.logger import get_logger
import logging

class CustomException(Exception):

    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message)

    @staticmethod
    def get_detailed_error_message(error_message: str) -> str:
        exc_type, exc_value, exc_tb = traceback.sys.exc_info()

        # In case exc_info() returns None (rare cases)
        if exc_tb is None:
            return f"Error: {error_message}"

        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno

        detailed_message = (
            f"Error occurred in script: {file_name} "
            f"at line number: {line_number}. "
            f"Error message: {error_message}"
        )
        return detailed_message

    def __str__(self):
        return self.error_message







































# import traceback
# import sys
# from src.logger import get_logger
# import logging

# class CustomException(Exception):
    
#     def __init__(self, error_message,error_detail: sys):
#         super().__init__(error_message)
#         self.error_message = self.get_detailed_error_message(error_message, error_detail)
#         self.error_detail = error_detail
        
#     @staticmethod
#     def get_detailed_error_message(error_message: str, error_detail: sys) -> str:
#         # the first and second one is not used to that thrid one is used to get the traceback object
#         _, _, exc_tb = error_detail.exc_info()
#         # getting the line number from the traceback object
#         line_number = exc_tb.tb_lineno
#         # getting the file name from the traceback object
#         file_name = exc_tb.tb_frame.f_code.co_filename
#         detailed_message = f"Error occurred in script: {file_name} at line number: {line_number}. Error message: {error_message}"
#         return detailed_message
    
#     def __str__(self):
#         return self.error_message
    
#     # def __init__(self, message: str, errors: Exception = None):
#     #     super().__init__(message)
#     #     self.message = message
#     #     self.errors = errors
#     #     self.logger = get_logger(self.__class__.__name__)
#     #     self.log_exception()

#     # def log_exception(self):
#     #     exc_type, exc_value, exc_tb = sys.exc_info()
#     #     tb_info = traceback.extract_tb(exc_tb)
#     #     filename, line, func, text = tb_info[-1]
#     #     error_message = f"Exception occurred in file: {filename}, line: {line}, in function: {func}. Message: {self.message}"
#     #     if self.errors:
#     #         error_message += f" | Original error: {str(self.errors)}"
#     #     self.logger.error(error_message)