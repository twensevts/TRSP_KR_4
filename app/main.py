from threading import Lock
from itertools import count

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .database import Base, engine, get_session
from .exceptions import CustomExceptionA, CustomExceptionB
from .models import Product
from .schemas import (
    ErrorResponse,
    ProductCreate,
    ProductRead,
    SimpleUserCreate,
    SimpleUserRead,
    StrictUserIn,
    ValidationErrorResponse,
)

app = FastAPI(title="Control Work #4")

users_db: dict[int, dict[str, object]] = {}
_user_id_seq = count(start=1)
_user_id_lock = Lock()


@app.exception_handler(CustomExceptionA)
async def custom_exception_a_handler(_: Request, exc: CustomExceptionA) -> JSONResponse:
    payload = ErrorResponse(detail=exc.message, error_code=exc.error_code).model_dump()
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(CustomExceptionB)
async def custom_exception_b_handler(_: Request, exc: CustomExceptionB) -> JSONResponse:
    payload = ErrorResponse(detail=exc.message, error_code=exc.error_code).model_dump()
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    issues = [
        {"field": ".".join(str(item) for item in error["loc"][1:]), "message": error["msg"]}
        for error in exc.errors()
    ]
    payload = ValidationErrorResponse(detail="Validation failed", errors=issues).model_dump()
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, content=payload)


def next_user_id() -> int:
    with _user_id_lock:
        return next(_user_id_seq)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/users", response_model=SimpleUserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: SimpleUserCreate) -> dict[str, object]:
    user_id = next_user_id()
    users_db[user_id] = user.model_dump()
    return {"id": user_id, **users_db[user_id]}


@app.get("/users/{user_id}", response_model=SimpleUserRead)
def get_user(user_id: int) -> dict[str, object]:
    if user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"id": user_id, **users_db[user_id]}


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int) -> Response:
    if users_db.pop(user_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/validated-users")
def create_validated_user(user: StrictUserIn) -> dict[str, object]:
    return user.model_dump()


@app.get("/errors/a")
def raise_custom_a() -> None:
    raise CustomExceptionA(message="Business rule failed", status_code=409, error_code="RULE_A")


@app.get("/errors/b")
def raise_custom_b() -> None:
    raise CustomExceptionB(message="Target resource was not found", status_code=404, error_code="RULE_B")


@app.post("/products", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, session: Session = Depends(get_session)) -> Product:
    db_product = Product(**product.model_dump())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int, session: Session = Depends(get_session)) -> Product:
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
