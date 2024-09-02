import discord
import yt_dlp
import yt_dlp as youtube_dl
from discord import app_commands, Interaction
from discord.ext import commands

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': True}

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
    async def play(self, ctx: Interaction, *, url: str):
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

        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(f"ytsearch:{url}", download=False)
            if 'entries' in info and info['entries']:
                info = info['entries'][0]
                url = info['url']
                title = info['title']
                self.queue.append((url, title))
                await ctx.followup.send(f"Adicionado na fila, jovem!: {title}")
            else:
                await ctx.followup.send("Não consegui encontrar o vídeo. Por favor, verifique o URL.")

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
        if voice_client and voice_client.is_playing():
            voice_client.stop()
            await self.play_next(ctx)
            await ctx.response.send_message("Música intancável. Por isso está sendo pulada.")
        else:
            await ctx.response.send_message("Nenhuma música está tocando no momento.")


async def setup(bot):
    await bot.add_cog(Slash(bot))
