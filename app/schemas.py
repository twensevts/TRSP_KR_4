from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, conint, constr


class ProductCreate(BaseModel):
    title: str
    price: Decimal
    count: int
    description: str


class ProductRead(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SimpleUserCreate(BaseModel):
    username: str
    age: int


class SimpleUserRead(SimpleUserCreate):
    id: int


class StrictUserIn(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: str | None = "Unknown"


class ErrorResponse(BaseModel):
    detail: str
    error_code: str


class ValidationIssue(BaseModel):
    field: str
    message: str


class ValidationErrorResponse(BaseModel):
    detail: str
    errors: list[ValidationIssue]
