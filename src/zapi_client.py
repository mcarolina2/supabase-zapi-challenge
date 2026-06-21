"""Integração com a Z-API: envio de mensagens de texto via WhatsApp."""

from __future__ import annotations

import logging
import re

import requests

logger = logging.getLogger(__name__)

_ZAPI_BASE_URL = "https://api.z-api.io"


class ZApiError(Exception):
    """Lançada quando a requisição à Z-API falha."""


class ZApiClient:
    """Cliente fino sobre o endpoint send-text da Z-API."""

    def __init__(self, instance_id: str, token: str, client_token: str, timeout: int = 15) -> None:
        self._url = f"{_ZAPI_BASE_URL}/instances/{instance_id}/token/{token}/send-text"
        self._headers = {
            "Content-Type": "application/json",
            "Client-Token": client_token,
        }
        self._timeout = timeout

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        """Remove tudo que não é dígito. Ex.: '+55 (83) 9 9999-9999' -> '5583999999999'."""
        return re.sub(r"\D", "", phone)

    def send_text(self, phone: str, message: str) -> dict:
        """Envia uma mensagem de texto. Levanta ZApiError em caso de falha."""
        clean_phone = self._normalize_phone(phone)
        payload = {"phone": clean_phone, "message": message}

        logger.info("Enviando mensagem para %s...", clean_phone)
        try:
            resp = requests.post(
                self._url, json=payload, headers=self._headers, timeout=self._timeout
            )
            resp.raise_for_status()
        except requests.RequestException as exc:
            logger.error("Falha ao enviar mensagem para %s: %s", clean_phone, exc)
            raise ZApiError(f"Erro ao enviar mensagem para {clean_phone}: {exc}") from exc

        logger.info("Mensagem enviada com sucesso para %s.", clean_phone)
        return resp.json()
