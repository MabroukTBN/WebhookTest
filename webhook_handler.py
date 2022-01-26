import asyncio
from pyngrok import ngrok
from aiohttp import web
from discord.ext import commands

class GithubHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tunnel = None

    async def webserver(self):
        async def handler(request):
            return web.Response(text="Hello, world")

        app = web.Application()
        app.router.add_get('/', handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, '127.0.0.1', 5000)
        http_tunnel = ngrok.connect('5000')
        tunnels = ngrok.get_tunnels()
        self.tunnel = tunnels[0]
        print(self.tunnel)
        await self.bot.wait_until_ready()
        await self.site.start()
        print("Webserver On")

    def __unload(self):
        asyncio.ensure_future(self.site.stop())