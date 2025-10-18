import discord
import yt_dlp
import yt_dlp as youtube_dl
from discord import app_commands, Interaction
from discord.ext import commands

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {
    'format': 'bestaudio',
    'noplaylist': True, 
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    },
    'skip_download': True,
    'age_limit': 999,
    'cookiesfrombrowser': ('firefox',),
    'geo_bypass': True,
}

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        super().__init__()

    @app_commands.command()
    async def wow(self, ctx: discord.Interaction):
        my_embed = discord.Embed(title="WoW")
        img_principal = discord.File('img/wow.gif', 'imagem.gif')
        my_embed.set_image(url="attachment://imagem.gif")
        await ctx.response.send_message(file=img_principal, embed=my_embed)

    @app_commands.command()
    async def ok(self, ctx: discord.Interaction):
        my_embed = discord.Embed(title="Ok.")
        img_principal = discord.File('img/ok.jpg', 'imagem.jpg')
        thumb_principal = discord.File('img/ok.jpg', 'thumb.jpg')
        my_embed.set_thumbnail(url="attachment://thumb.jpg")
        my_embed.set_image(url="attachment://imagem.jpg")
        my_embed.description = "ok"
        await ctx.response.send_message(files=[img_principal, thumb_principal], embed=my_embed)

    @app_commands.command()
    async def play(self, ctx: Interaction, *, url: str): # Argumento é 'url'
        if ctx.user.voice is None:
            await ctx.response.send_message(
                "O teu, entre em canal de voz para executar o comando! Te ligue bico de luz!"
            )
            return

        voice_channel = ctx.user.voice.channel
        voice_client = ctx.guild.voice_client

        if voice_client is None:
            voice_client = await voice_channel.connect()
        else:
            await voice_client.move_to(voice_channel)

        await ctx.response.defer()

        if url.startswith(('http', 'www.')):
            source_url = url # Usa o link puro
        else:
            source_url = f"ytsearch:{url}" 
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(source_url, download=False)
            
            if 'entries' in info and info['entries']:
                info = info['entries'][0]
        
            try:
                final_url = info['url']
                title = info['title']
            except KeyError:
                await ctx.followup.send("Não consegui encontrar o vídeo. Por favor, verifique o URL ou o termo de busca.")
                return

        self.queue.append((final_url, title))
        await ctx.followup.send(f"Adicionado na fila, jovem!: {title}")
        
        if not voice_client.is_playing():
            await self.play_next(ctx)

    async def play_next(self, ctx: Interaction):
        if self.queue:
            url, title = self.queue.pop(0)
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
            ctx.guild.voice_client.play(source, after=lambda _: self.bot.loop.create_task(self.play_next(ctx)))
            await ctx.followup.send(f"Está tocando agora: {title}")
        elif not ctx.guild.voice_client.is_playing():
            await ctx.followup.send("Acabou as músicas na fila meu jovem!!")

    @app_commands.command()
    async def pular(self, ctx: discord.Interaction):
        voice_client = ctx.guild.voice_client
        
        await ctx.response.defer() 
        
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            
            await self.play_next(ctx) 
            
            await ctx.followup.send("Música é uma porcaria. Por isso está sendo pulada.")
            
        else:
            await ctx.followup.send("Nenhuma música está tocando no momento.")
    @app_commands.command()
    async def stop(self, ctx: discord.Interaction):
        voice_client = ctx.guild.voice_client
        await ctx.response.defer() 
        
        if voice_client:
            if voice_client.is_playing() or voice_client.is_paused():
                voice_client.stop()
                self.queue.clear()
                await voice_client.disconnect()
                await ctx.followup.send("Pois é, também estava de saco cheio, obrigado por parar e sair.")
            else:
                 await ctx.followup.send("Jovem se é besta?! Nenhuma música está tocando no momento.")
                 
        else:
            await ctx.followup.send("Eu nem estou no canal de voz, te ligue bico de luz!")

async def setup(bot):
    await bot.add_cog(Slash(bot))
