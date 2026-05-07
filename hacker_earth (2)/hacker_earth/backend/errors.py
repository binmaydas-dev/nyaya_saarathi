from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger

class NyayaMitraException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class PDFProcessingError(NyayaMitraException):
    def __init__(self, message: str = "Failed to process PDF document."):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)

class OCRFailureError(NyayaMitraException):
    def __init__(self, message: str = "OCR processing failed or timed out."):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)

class UnsupportedFileError(NyayaMitraException):
    def __init__(self, message: str = "Unsupported file type. Please upload a valid PDF."):
        super().__init__(message, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

class FileTooLargeError(NyayaMitraException):
    def __init__(self, message: str = "File exceeds the maximum allowed size."):
        super().__init__(message, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

async def custom_exception_handler(request: Request, exc: NyayaMitraException):
    logger.error(f"Error handling request {request.url}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_type": exc.__class__.__name__,
            "message": exc.message
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error_type": "InternalServerError",
            "message": "An unexpected error occurred during processing."
        }
    )
