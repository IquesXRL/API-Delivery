from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import gerar_sessao, verificar_token
from main import bcrypt_context, EXP_ACCESS_TOKEN, ALGORITHM, SECRET_KEY
from schemas import UsuarioSchema,LoginSchema
from sqlalchemy.orm import Session
from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from fastapi.security import OAuth2PasswordRequestForm




#Criando "Roteador"
auth_router = APIRouter(prefix="/auth", tags=["Auth"])

#Criando Rotas
@auth_router.get("/")
async def autenticar():
    return{"mensagem":"Usuário autenticado", "Verify":False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session:Session = Depends(gerar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(staus_code=400, detail="Usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        new_user = Usuario(
            nome=usuario_schema.nome,
            email=usuario_schema.email,
            senha=senha_criptografada,
            ativo=usuario_schema.ativo,
            admin=usuario_schema.admin
        )
        session.add(new_user)
        session.commit()
        return {"mensagem": f"Sucesso, usuario {new_user.email} cadastrado."}


def gerar_token(id_usuario, duracao_token = timedelta(minutes=EXP_ACCESS_TOKEN)):
    expira_token = datetime.now(timezone.utc) + duracao_token
    dic_jwt = {"sub": str(id_usuario), "exp":expira_token}
    jwt_encode = jwt.encode(dic_jwt,SECRET_KEY,ALGORITHM)
    #token =  f"wasdxyz{id_usuario}"
    return jwt_encode

def autenticar_usuario(email,senha,session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha,usuario.senha):
        return False
    return usuario


#Gerar tokens
@auth_router.post("/login")
async def login(login_schema:LoginSchema, session:Session=Depends(gerar_sessao)):
    usuario = autenticar_usuario(login_schema.email,login_schema.senha,session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não existe")
    else:
        access_token = gerar_token(usuario.id)
        refresh_token = gerar_token(usuario.id, timedelta(days=7))
        return{
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    

@auth_router.post("/login-form")
async def login(login_form: OAuth2PasswordRequestForm = Depends(), session:Session=Depends(gerar_sessao)):
    usuario = autenticar_usuario(login_form.username,login_form.password,session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não existe")
    else:
        access_token = gerar_token(usuario.id)
        return{
            "access_token": access_token,
            "token_type": "Bearer"
        }

    
@auth_router.get("/refresh")
async def use_rt(usuario:Usuario = Depends(verificar_token)):
    access_token = gerar_token(usuario.id)
    return {
        "access_token":access_token,
        "token_type": "Bearer"
    }

#*
#@auth_router.post("/login-form")
#async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session:Session=Depends(gerar_sessao)):
#    usuario = autenticar_usuario(dados_formulario.username,dados_formulario.password,session)
#    if not usuario:
        #raise HTTPException(status_code=400, detail="Usuário não existe")
#    else:
#        access_token = gerar_token(usuario.id)
#        return{
#            "access_token": access_token,
#            "token_type": "Bearer"
#        }
    
#*    
#@auth_router.get("/refresh")
#async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
#    access_token = gerar_token(usuario.id)
#    return {
#        "access_token": access_token,
#        "token_type": "Bearer"
#        }