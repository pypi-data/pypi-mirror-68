import logging
import pytest

_LOGGER = logging.getLogger(__name__)
import mspyteams.aiohttp as card_aiohttp
from aiohttp import web, ClientSession


async def resp(request):
    if request.method == "POST":
        data = await request.json()

        return web.Response()
    return web.Response(status=501, text="Wrong response")


@pytest.fixture
async def mock_server(aiohttp_server):
    app = web.Application()
    app.router.add_post("/testwebhook", resp)
    server = await aiohttp_server(app)

    yield server


@pytest.mark.asyncio
async def test_send(mock_server, card):
    card.title = "title"
    card.text = "text"
    async with ClientSession() as session:
        res = await card_aiohttp.send(
            card, f"http://localhost:{mock_server.port}/testwebhook", session
        )
    assert res[0] == 200
