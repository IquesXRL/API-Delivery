from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, create_engine # Adicionei create_engine
from alembic import context
import sys
import os

# Garante que o Alembic encontre seus modelos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from models import Base # Certifique-se que o 'Base' está com 'B' maiúsculo se for o caso

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def get_url():
    # 1. Busca a URL do banco nas variáveis de ambiente
    url = os.getenv("DATABASE_URL")
    if not url:
        # Se não houver variável (local), usa a que está no alembic.ini
        url = config.get_main_option("sqlalchemy.url")
    
    # 2. Corrige o prefixo para o SQLAlchemy moderno
    if url and url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

def run_migrations_offline() -> None:
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # Em vez de engine_from_config, criamos o engine diretamente com a URL dinâmica
    url = get_url()
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()