from pydantic import BaseModel
from typing import Optional, List

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        orm_atribute = True

class PedidoSchema(BaseModel):
    usuario: int

    class Config:
        orm_atribute = True


class LoginSchema(BaseModel):
    email:str
    senha:str
    
    class Config:
        orm_atribute = True


class ItemPedidoSchema(BaseModel):
        quantidade:int
        sabor:str
        tamanho:str
        preco_unitario:float

        class Config:
            orm_atribute = True

class ReponsePedidoSchema(BaseModel):
        id:int
        status: str
        preco: float
        itens: List[ItemPedidoSchema] #Também depende de um schema

        class Config:
            orm_atribute = True
        