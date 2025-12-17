
from sqlalchemy.orm import sessionmaker
from models import db
from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError


def gerar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
      session.close()


def verificar_token(token:str = Depends(oauth2_schema), session:Session=Depends(gerar_sessao)):
    try:
        dict_user = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dict_user.get("sub"))
    except:
        raise HTTPException(status_code=401, detail = "Acesso inválido")
    usuario = session.query(Usuario).filter(Usuario.id==id_user).first()
    return usuario


#*    
#def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(gerar_sessao)):
#    try:#
        #dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        #id_usuario = int(dic_info.get("sub"))
  #  except JWTError:
 #       raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token")
 #   # verificar se o token é válido
#    # extrair o ID do usuário do token
#    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
# #   if not usuario:
#        raise HTTPException(status_code=401, detail="Acesso Inválido")
#    return usuario