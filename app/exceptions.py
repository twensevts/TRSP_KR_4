from dataclasses import dataclass


@dataclass
class CustomExceptionA(Exception):
    message: str = "Rule A was violated"
    status_code: int = 409
    error_code: str = "CUSTOM_A"


@dataclass
class CustomExceptionB(Exception):
    message: str = "Resource not found"
    status_code: int = 404
    error_code: str = "CUSTOM_B"
