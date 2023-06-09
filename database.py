import mysql.connector
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Product(BaseModel):
    id: Optional[int]
    name: str
    category: str
    sku: str
    price: float
    quantity: int
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

class Category(BaseModel):
    id: Optional[int]
    name: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

class User(BaseModel):
    id: Optional[int]
    name: str
    email: str
    password: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    is_active: bool = True

def connect_to_database():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="vikas123",
        database="db1"
    )
    return db

def get_all_products():
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products")
    result = cursor.fetchall()
    products = [Product(
        id=row[0],
        name=row[1],
        category=row[2],
        sku=row[3],
        price=row[4],
        quantity=row[5],
        created_at=row[6],
        modified_at=row[7]
    ) for row in result]
    cursor.close()
    db.close()
    return products

def get_all_categories():
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categories")
    result = cursor.fetchall()
    categories = [Category(
        id=row[0],
        name=row[1],
        created_at=row[2],
        modified_at=row[3]
    ) for row in result]
    cursor.close()
    db.close()
    return categories

def get_product(product_id: int):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result:
        return Product(
            id=result[0],
            name=result[1],
            category=result[2],
            sku=result[3],
            price=result[4],
            quantity=result[5],
            created_at=result[6],
            modified_at=result[7]
        )
    else:
        return None

def create_product(product: Product):
    db = connect_to_database()
    cursor = db.cursor()
    sql = "INSERT INTO products (name, category, sku, price, quantity) VALUES (%s, %s, %s, %s, %s)"
    values = (product.name, product.category, product.sku, product.price, product.quantity)
    cursor.execute(sql, values)
    db.commit()
    product_id = cursor.lastrowid
    cursor.close()
    db.close()
    return get_product(product_id)

def update_product(product_id: int, product: Product):
    db = connect_to_database()
    cursor = db.cursor()
    sql = "UPDATE products SET name = %s, category = %s, sku = %s, price = %s, quantity = %s WHERE id = %s"
    values = (product.name, product.category, product.sku, product.price, product.quantity, product_id)
    cursor.execute(sql, values)
    db.commit()
    cursor.close()
    db.close()
    return get_product(product_id)

def delete_product(product_id: int):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
    db.commit()
    cursor.close()
    db.close()

def get_user_by_email(email: str):
    db = connect_to_database()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    if result:
        return User(
            id=result[0],
            name=result[1],
            email=result[2],
            password=result[3],
            created_at=result[4],
            modified_at=result[5],
            is_active=result[6]
        )
    else:
        return None

def verify_password(plain_password: str, hashed_password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
