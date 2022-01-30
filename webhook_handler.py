import asyncio
import json
import requests
import os
import logging
from dotenv import load_dotenv
from pyngrok import ngrok
from aiohttp import web
from discord.ext import commands

load_dotenv()


class WebhookHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def webserver(self):
        async def handler(request):
            parsed = json.dumps(json.loads(request.json),
                                indent=4, sort_keys=True)
            channel = self.bot.get_channel(932556602609901568)
            await channel.send(parsed)
            return web.Response(text=parsed)

        app = web.Application()
        app.router.add_get('/', handler)
        app.router.add_post('/', handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, '127.0.0.1', 5000)

        # logger = logging.getLogger()
        # logger.setLevel(logging.DEBUG)
        # handler = logging.StreamHandler()
        # handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        # logger.addHandler(handler)

        # NGROK        
        self.tunnel = ngrok.connect('5000', 'tcp').public_url

        # TRELLO
        url = "https://api.trello.com/1/webhooks/"
        headers = {"Accept": "application/json"}
        query = {'key': str(os.getenv("Trello_API_Key")),
                 'token': str(os.getenv("Trello_Token")),
                 'callbackURL': self.tunnel,
                 'idModel': '61f272b074ba662112db4352'}
        response = requests.request("POST", url, headers=headers, params=query)
        print(json.dumps(response.text, indent=4, sort_keys=True))

        await self.bot.wait_until_ready()
        await self.site.start()
        print("Webserver On")

    def __unload(self):
        asyncio.ensure_future(self.site.stop())
