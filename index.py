import discord
from discord.ext import commands
from discord import app_commands

from dotenv import load_dotenv
load_dotenv()

import os

permission = discord.Intents.default()
permission.message_content = True
permission.members = True
permission.voice_states = True
bot = commands.Bot(command_prefix=".", intents=permission)

async def carregar_commands():
    for arquivos in os.listdir('commands'):
        print(arquivos)
        if arquivos.endswith('.py'):
            await bot.load_extension(f"commands.{arquivos[:-3]}")

@bot.command()
async def sync(ctx:commands.Context):
    print(ctx.author.id)
    if ctx.author.id == 292079306409246730:
        sics = await bot.tree.sync()
        await ctx.reply(f"{len(sics)} comandos foram sincronizados com sucesso")
    else:
        await ctx.reply('Você é fraco lhe falta ódio e QI')


@bot.event
async def on_ready():
    await carregar_commands()
    await bot.tree.sync()
    print("Bah tchê estou aí na atividade")

# @bot.event
# async def on_message(msg:discord.Message):
#     autor = msg.author
#     if autor.bot:
#         return
#     if autor.id == 895417703022616577:
#         await msg.reply('você é boiola')

@bot.event
async def on_member_join(membro:discord.Member):
    channel = bot.get_channel(399554361912590337)
    my_embed = discord.Embed(title=f"Bem-vindo, {membro.name}!" )
    img_principal = discord.File('img/entrou.jpg', 'imagem.jpg')
    thumb_principal = discord.File('img/tb_entrou.jpg', 'thumb.jpg')
    my_embed.set_thumbnail(url="attachment://thumb.jpg")
    my_embed.set_image(url="attachment://imagem.jpg")
    my_embed.description = "Aproveite a passagem, e lembre-se de deixar bem especificado seu tipo de mulher\nCuidado com o politico ele tentará de converter para a Guerra, mas somente os chefe da casa tem algum poder"
    await channel.send(files=[img_principal, thumb_principal], embed=my_embed)

@bot.event
async def on_member_remove(membro:discord.Member):
    channel = bot.get_channel(399554361912590337)
    my_embed = discord.Embed(title=f"Não aguentou a pressão, {membro.name}!" )
    img_principal = discord.File('img/saiu.jpg', 'imagem.jpg')
    thumb_principal = discord.File('img/tb_saiu.jpg', 'thumb.jpg')
    my_embed.set_thumbnail(url="attachment://thumb.jpg")
    my_embed.set_image(url="attachment://imagem.jpg")
    my_embed.description = ""
    await channel.send(files=[img_principal, thumb_principal], embed=my_embed)

bot.run(os.environ['TOKEN'])