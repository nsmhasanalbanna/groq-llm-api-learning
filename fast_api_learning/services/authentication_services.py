from pwdlib import PasswordHash
from clients.post_gres_client import get_post_gres_connection
from psycopg.errors import UniqueViolation
from fastapi import HTTPException
from utils.jwt_utils import create_access_token

passwordhash = PasswordHash.recommended()

def hash_password(password : str):
    hashed_password = passwordhash.hash(password)

    return hashed_password

def verify_password(hashed_password, password):
    return passwordhash.verify(password,hashed_password)

def store_users(data):
    hashed_password = hash_password(data.password)
    connection = get_post_gres_connection()
    try:
        with connection.cursor() as cursor:
            try :
                cursor.execute(
                    """
                    INSERT INTO users (email, password_hash)
                    VALUES (%s, %s)
                    RETURNING id;
                    """,
                    (data.email, hashed_password)
                )
                user_id = cursor.fetchone()[0]
                connection.commit()
            except UniqueViolation:
                connection.rollback()
                raise HTTPException(status_code=409,detail="email already exists")

            return {
                "user_id" : user_id,
                "email" : data.email
            }

    finally:
        connection.close()

def verify_login(data):
    connection = get_post_gres_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id,password_hash
                FROM public.users
                WHERE email = %s;
                """,
                (data.email,)
                )
            row = cursor.fetchone()
            if row is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password"
                )
            
            user_id = row[0]
            password = row[1]
            verification_result = verify_password(password , data.password)
            if not verification_result:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid email or password"
                )
            return {
                        "access_token" : create_access_token(user_id),
                        "token_type" : "bearer"
                    }
    finally:
        connection.close()
    
