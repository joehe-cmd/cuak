import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f"Estou pronto! Estou conectado como {bot.user}")

    await bot.change_presence(activity=discord.Game(name="Minecraft"))
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="PornHub"))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "palavrão" in message.content:
        await message.channel.send(f"Por favor, {message.author} não ofenda os demais usuários")

        await message.delete()
    
    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction, user):
    print(reaction.emoji)
    if reaction.emoji == "🍺":
        role = user.guild.get_role(1278167394048802837)
        await user.add_roles(role)
    elif reaction.emoji == "🧃":
        role = user.guild.get_role(1278167462772346901)
        await user.add_roles(role)

# ID do canal onde a mensagem de boas-vindas será enviada
WELCOME_CHANNEL_ID = 1280162832578514986  # Substitua pelo ID do seu canal de boas-vindas
AUTOROLE_ID = 1280194449942646868  # Substitua pelo ID do cargo desejado

@bot.event
async def on_member_join(member):
    print(f'{member} acabou de entrar no servidor.')  # Mensagem de debug
    await bot.wait_until_ready()  # Garante que o bot esteja completamente inicializado
    await send_welcome_message(member)

async def send_welcome_message(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    
    if channel is not None:
        print(f'Canal encontrado: {channel.name}')  # Mensagem de debug
        embed = discord.Embed(
            title="Bem-vindo(a) ao servidor!",
            description=f"Olá {member.mention}, seja bem-vindo(a) ao nosso servidor! Esperamos que você se divirta e aproveite a estadia!",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"{member.guild.name} • © Todos os direitos reservados.")
        
        await channel.send(embed=embed)
        print('Mensagem de boas-vindas enviada.')  # Mensagem de debug
    else:
        print("Canal de boas-vindas não encontrado.")

 # Atribuição de cargo
    role = member.guild.get_role(AUTOROLE_ID)
    if role is not None:
        await member.add_roles(role)
        print(f"Cargo '{role.name}' foi atribuído a {member.name}.")
    else:
        print("Cargo não encontrado.")


@bot.command(name='setautorole')
@commands.has_permissions(administrator=True)
async def set_autorole(ctx, role: discord.Role):
    global AUTOROLE_ID
    AUTOROLE_ID = role.id
    await ctx.send(f"O cargo {role.name} foi definido como Autorole.")
    print(f"Autorole definido para o cargo '{role.name}'.")

@bot.command()
async def dado(ctx, *, dice: str):
    """Comando de dado"""
    try:
        # Divide a entrada em duas partes, por exemplo, '2d6' em '2' e '6'
        num, sides = dice.lower().split('d')
        num = int(num)
        sides = int(sides)
        
        if num < 1 or sides < 1:
            await ctx.send("O número de dados e o número de lados devem ser pelo menos 1.")
            return

        results = [random.randint(1, sides) for _ in range(num)]
        total = sum(results)
        results_str = ', '.join(map(str, results))
        
        await ctx.send(f"{ctx.author.mention} rolou {num} dado(s) de {sides} lados e obteve **{results_str}** (total: **{total}**).")
    
    except ValueError:
        await ctx.send("Uso incorreto. Use a notação XdY, onde X é o número de dados e Y é o número de lados.")
    except Exception as e:
        await ctx.send(f"Erro: {e}")

# Comando de teste
@bot.command(name="testwelcome")
async def test_welcome(ctx, member: discord.Member):
    """Comando para testar o boas vindas"""
    await send_welcome_message(member)
    await ctx.send(f"Mensagem de boas-vindas de teste enviada para {member.mention}.")


@bot.command(name="oi")
async def send_hello(ctx):
    """O bot te da oi"""
    name = ctx.author.name

    response = "Olá, " + name

    await ctx.send(response)

@bot.command(name="calcular")
async def calculate_expression(ctx, *expression):
    """Calculadora"""
    expression = "".join(expression)

    print(expression)

    response = eval(expression)

    await ctx.send("A resposta é: " + str(response))

@bot.command(name= "segredo")
async def secret(ctx):
    """Mensagem Direta"""
    await ctx.author.send("Bem-vindo!")
    await ctx.author.send("Obrigado por entrar")
    await ctx.author.send("E se divirta")

@bot.command()
async def ping(ctx):
    """Ping-Pong"""
    await ctx.send('Pong!')

@bot.command()
async def abraço(ctx, member: discord.Member):
    """Abrace um membro"""
    # Lista de GIFs de abraço
    gifs = [
        "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
        "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
        "https://media.giphy.com/media/143v0Z4767T15e/giphy.gif",
        "https://media.giphy.com/media/3bqtLDeiDtwhq/giphy.gif",
        "https://media.giphy.com/media/xT39CXg70nNS0MFNLy/giphy.gif"
    ]
    
    # Escolhe um GIF aleatório
    gif = random.choice(gifs)
    
    # Cria um embed
    embed = discord.Embed(
        title="Abraço!",
        description=f'{ctx.author.mention} deu um abraço em {member.mention}! 🤗',
        color=discord.Color.purple()
    )
    embed.set_image(url=gif)
    
    # Envia o embed
    await ctx.send(embed=embed)

@bot.command()
async def sorteio(ctx):
    """Comando sortear um membro"""
    members = ctx.guild.members
    winner = random.choice(members)
    await ctx.send(f'O vencedor do sorteio é: {winner.mention}!')

@bot.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Comando para banir um membro.(Adiministrador)"""
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} foi banido do servidor. Motivo: {reason}')
                   
@bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Comando para expulsar um membro.(Adiministrador)"""
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} foi expulso do servidor. Motivo: {reason}')

@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    """Comando para mutar um membro.(Adiministrador)"""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")

    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)

    await member.add_roles(mute_role)
    await ctx.send(f'{member.mention} foi mutado. Motivo: {reason}')

@bot.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    """Comando desmutar um membro. (Adiministrador)"""
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    
    if mute_role in member.roles:
        await member.remove_roles(mute_role)
        await ctx.send(f'{member.mention} foi desmutado.')
    else:
        await ctx.send(f'{member.mention} não está mutado.')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    """Comando para apagar mensagens"""
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} mensagens foram deletadas.', delete_after=5)

@bot.command()
async def ajuda(ctx):
    """Comando para mostrar a lista de comandos disponíveis."""
    embed = discord.Embed(
        title="Lista de Comandos",
        description="Aqui estão os comandos disponíveis:",
        color=discord.Color.blue()
    )

    # Adiciona os comandos ao embed
    for command in bot.commands:
        # Adiciona cada comando com sua descrição (se houver)
        embed.add_field(
            name=f'!{command.name}',
            value=command.help or 'Sem descrição',
            inline=False
        )

    # Envia o embed com a lista de comandos
    await ctx.send(embed=embed)


bot.run("YOUR_TOKEN_HERE")
