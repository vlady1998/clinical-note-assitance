from fastapi import HTTPException, status

class BadRequestHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg or "Bad request",
        )


class AuthFailedHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=msg or "Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthTokenExpiredHTTPException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


class ForbiddenHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=msg or "Requested resource is forbidden",
        )


class NotFoundHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=msg or "Requested resource is not found",
        )


class ConflictHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=msg or "Conflicting resource request",
        )


class ServiceNotAvailableHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=msg or "Service not available",
        )

class InternalServerErrorHTTPException(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=msg or "Internal server error",
        )