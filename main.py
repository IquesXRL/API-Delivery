from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXP_ACCESS_TOKEN = int(os.getenv("EXP_ACCESS_TOKEN"))

#auth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-form") #*

# Criando API
app = FastAPI(
    title="API Delivery",
    docs_url="/", # Isso define o Swagger na raiz
    redoc_url=None
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

#Importando Rotas
from auth_routes import auth_router
from order_routes import order_router
# Incluindo Rotas na API
app.include_router(auth_router)
app.include_router(order_router)

#npx neonctl@latest init