import discord
from discord import app_commands
from discord.ext import commands

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

    @app_commands.command()
    async def wow(self, ctx:discord.Interaction):
        my_embed = discord.Embed(title="WoW")
        img_principal = discord.File('img/wow.gif', 'imagem.gif')
        my_embed.set_image(url="attachment://imagem.gif")
        await ctx.response.send_message(file=img_principal, embed=my_embed)
    
    @app_commands.command()
    async def ok(ctx:discord.Interaction):
        my_embed = discord.Embed(title="Ok.")
        img_principal = discord.File('img/ok.jpg', 'imagem.jpg')
        thumb_principal = discord.File('img/ok.jpg', 'thumb.jpg')
        my_embed.set_thumbnail(url="attachment://thumb.jpg")
        my_embed.set_image(url="attachment://imagem.jpg")
        my_embed.description = "ok"
        await ctx.response.send_message(files=[img_principal, thumb_principal], embed=my_embed)



async def setup(bot):
    await bot.add_cog(Slash(bot))