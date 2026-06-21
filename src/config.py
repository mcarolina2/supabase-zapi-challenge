#Configuração da aplicação: leitura de variáveis de ambiente e setup de logging.
from __future__ import annotations
import dotenv
import logging
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    #Lançada quando uma variável de ambiente obrigatória não está definida.


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_key: str
    supabase_table: str
    zapi_instance_id: str
    zapi_token: str
    zapi_client_token: str
    max_contacts: int


def _get_env(name: str, required: bool = True, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise ConfigError(f"Variável de ambiente obrigatória não definida: {name}")
    return value or ""


def load_settings() -> Settings:
    #Carrega e valida todas as variáveis de ambiente necessárias.
    return Settings(
        supabase_url=_get_env("SUPABASE_URL"),
        supabase_key=_get_env("SUPABASE_KEY"),
        supabase_table=_get_env("SUPABASE_TABLE", required=False, default="contacts"),
        zapi_instance_id=_get_env("ZAPI_INSTANCE_ID"),
        zapi_token=_get_env("ZAPI_TOKEN"),
        zapi_client_token=_get_env("ZAPI_CLIENT_TOKEN"),
        max_contacts=int(_get_env("MAX_CONTACTS", required=False, default="3")),
    )


def setup_logging() -> None:
    #Configura logging para console e arquivo (app.log).
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("app.log", encoding="utf-8"),
        ],
    )
