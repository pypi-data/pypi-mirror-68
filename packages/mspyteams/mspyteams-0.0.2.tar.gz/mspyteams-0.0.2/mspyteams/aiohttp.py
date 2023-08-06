"""Send card using aiohttp"""

import logging
from typing import TYPE_CHECKING
import aiohttp

if TYPE_CHECKING:
    from mspyteams.card import Card

_LOGGER = logging.getLogger(__name__)


async def send(card: "Card", webhook_url, session: aiohttp.ClientSession):
    """Send the card to the teams webhook."""
    data = card.card_data()
    async with session.post(webhook_url, json=data) as response:
        return response.status, await response.text()
