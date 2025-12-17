import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---
# Pega a URL do banco do Render/Neon. Se não achar, usa SQLite local.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./delivery.db")

# Ajuste para compatibilidade do SQLAlchemy com o PostgreSQL no Render
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Se for SQLite, precisa do connect_args. Se for PostgreSQL (Neon), não pode ter.
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
# ---------------------------------------

# Daqui para baixo continuam suas classes (User, Produto, Pedido, etc.)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self,nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

    #status_pedidos = (("Pendente","Pendente"),
     #                 ("Cancelado","Cancelado"),
      #                ("Finalizado","Finalizado"))

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status",String) #status = Column("status",ChoiceType(choice=status_pedidos))
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="Pendente", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):
        #percorrer todos os itens do pedido
        #Somar todos os precos de todos os itens
        #Editar campo "preco", com o valor final do pedido
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade",Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido",ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
    
    



