from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import gerar_sessao, verificar_token
from models import Pedido, Usuario, ItemPedido
from schemas import PedidoSchema,ItemPedidoSchema,ReponsePedidoSchema
from typing import List

order_router = APIRouter(prefix="/order",tags=["Orders"],dependencies= [Depends(verificar_token)])

@order_router.get("/")
async def pedidos():
    return{"Mensagem":"Sem pedidos"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema:PedidoSchema, session:Session=Depends(gerar_sessao)):
    novo_pedido = Pedido(
        usuario=pedido_schema.usuario
    )
    session.add(novo_pedido)
    session.commit()
    return {"mensagem":"Pedido Adicionado"}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido:int, session: Session = Depends(gerar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não encontrado.")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuário não autorizado.")
    pedido.status = "cancelado"
    session.commit()
    return{
        "mensagem":f"Pedido {pedido.id} cancelado!",
        "pedido": pedido
    }

@order_router.get("/lista")
async def listar_pedidos(session: Session = Depends(gerar_sessao),usuario: Usuario= Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Usuário não autorizado")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos" : pedidos
        }
    
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def add_item_pedido(id_pedido: int,
                          item_pedido_schema: ItemPedidoSchema,
                          session: Session = Depends(gerar_sessao),
                          usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        HTTPException(status_code=401,detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        HTTPException(status_code=401, detail="Usuário não autorizado")
    item_pedido = ItemPedido(item_pedido_schema.quantidade,
                             item_pedido_schema.sabor,
                             item_pedido_schema.tamanho,
                             item_pedido_schema.preco_unitario,
                             id_pedido) #ordem importa
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem":"Item criado com sucesso",
        "item_id":item_pedido.id,
        "preco_pedido":pedido.preco
    }

#remover item de pedido
@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int,
                          session: Session = Depends(gerar_sessao),
                          usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        HTTPException(status_code=401,detail="Item no pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        HTTPException(status_code=401, detail="Usuário não autorizado")

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem":"Item removido com sucesso",
        "itens_pedido": pedido.itens,
        "pedido":pedido
        
    }


#Finalizar pedido
@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido:int, session: Session = Depends(gerar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não encontrado.")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuário não autorizado.")
    pedido.status = "finalizado"
    session.commit()
    return{
        "mensagem":f"Pedido {pedido.id} finalizado com sucesso!",
        "pedido": pedido
    }


#visualizar 1 pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(gerar_sessao), usuario: Usuario= Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não encontrado.")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuário não autorizado.")
    return {
        "quantidade-itens-pedido": len(pedido.itens),
        "pedido":pedido
    }


#Visualizar todos os pedidos
@order_router.get("/lista/pedidos-usuario", response_model=List[ReponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(gerar_sessao),usuario: Usuario= Depends(verificar_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos
        