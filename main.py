from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import List

from database import (
    get_all_products,
    get_product,
    create_product,
    update_product,
    delete_product,
    get_all_categories,
    get_user_by_email,
    verify_password,
    create_access_token,
    decode_access_token,
    Product,
    Category,
    User,
)

app = FastAPI()

SECRET_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJSb2xlIjoiQWRtaW4iLCJJc3N1ZXIiOiJJc3N1ZXIiLCJVc2VybmFtZSI6IkphdmFJblVzZSIsImV4cCI6MTY4NTk4NTUzNSwiaWF0IjoxNjg1OTg1NTM1fQ.syGfaZCvaeJkR98tG0P9eVSwe6XcQGvBXOmzd63__Xo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user = get_user_by_email(token)
    if user is None:
        raise credentials_exception
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/products", response_model=List[Product])
def get_products():
    return get_all_products()

@app.get("/products/{product_id}", response_model=Product)
def get_single_product(product_id: int):
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.post("/products", response_model=Product)
def create_single_product(product: Product, current_user: User = Depends(get_current_active_user)):
    return create_product(product)

@app.put("/products/{product_id}", response_model=Product)
def update_single_product(product_id: int, product: Product, current_user: User = Depends(get_current_active_user)):
    updated_product = update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_single_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    delete_product(product_id)

@app.get("/categories", response_model=List[Category])
def get_categories():
    return get_all_categories()
