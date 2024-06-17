import jwt
from datetime import datetime, timedelta
import os

def generate_jwt_token(user_id):
    try:
        payload = {
            "exp": datetime.now() + timedelta(days=1),
            "iat": datetime.now(),
            "sub": str(user_id)
        }
        jwt_token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY"), algorithm="HS256")
        return jwt_token
    except Exception as e:
        return str(e)

def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
    except Exception as e:
        return str(e)
