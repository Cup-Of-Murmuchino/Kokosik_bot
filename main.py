import discord
from discord.ext import commands
import sqlite3
import random
from  random import randint

client = commands.Bot(";")
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
activity = discord.Activity(name='My activity', type=discord.ActivityType.streaming)

@client.event
async def on_ready():
    print('Bot CONNECTED')
    # await channel.send('Бот в онлайне, теперь все команды работают')

    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
username TEXT,
id INT,
minecraft_name TEXT,
exp BIGINT,		
ranks INT,
warns INT
)""")

    connection.commit()

@client.command()
async def reg(ctx, *name):
    author = ctx.author
    check = cursor.execute(f"""SELECT username FROM users WHERE id = {author.id}""").fetchone()
    if check is None:
        cursor.execute(f"""INSERT INTO users VALUES('{author.name}',{author.id},'{name[0]}',0,0,0)""")
        connection.commit()
        await ctx.send(f"{author.mention} вы успешно зарегистрировались!")
        # await ctx.message.add_reaction('👍')
    else:
        await ctx.send(f"Вы уже зарегистрировались!")

@client.command()
async def check(ctx,user:discord.Member):
    check = cursor.execute(f"SELECT username FROM users WHERE id = {user.id}").fetchone()
    if check:
        await ctx.send("True")
    else:
        await ctx.send("False")

@client.group()
async def nickname(ctx):
    pass

@nickname.command()
async def minecraft(ctx,user:discord.Member):
    Minecraft = cursor.execute(f"SELECT minecraft_name FROM users WHERE id = {user.id}").fetchone()
    # await ctx.channel.purge(limit=1)
    if Minecraft is not None:
        await ctx.send(f"Никнейм {user} в Minecraft: {Minecraft[0]}")
    else:
        await ctx.send(f"Пользователь не загеристрирован.")

@nickname.command()
async def discord(ctx,*user):
    name = cursor.execute(f"SELECT username FROM users WHERE minecraft_name = '{user[0]}'").fetchone()
    if name is None:
        await ctx.send(f"Такое имя не зарегистрировано!")
    else:
        for i in cursor.execute(f"SELECT minecraft_name FROM users"):
            if i[0] == user[0]:
                await ctx.send(f"Имя {user[0]} в майнкрафт: {name[0]}")

@client.command()
async def rename(ctx, *name):
    """Take new Minecraft user name as argument. Rename Minecraft user name if user exists in table."""
    author = ctx.author
    check = cursor.execute(f"""SELECT username FROM users WHERE id = {author.id}""").fetchone()
    if check is not None:
        cursor.execute(f"""UPDATE users SET minecraft_name = "{name[0]}" WHERE id = {author.id}""")
        connection.commit()
        await ctx.send(f"{author.mention} вы успешно изменили имя!")

@client.command()
async def delete(ctx):
    author = ctx.author
    check = cursor.execute(f"""SELECT username FROM users WHERE id = {author.id}""").fetchone()
    if check:
        cursor.execute(f"""DELETE FROM users WHERE id = {author.id}""")
        await ctx.send(f"{author.mention} вы успешно удалили свои данные.")
    else:
        await ctx.send(f"Такой записи нет.")

@client.event
async def on_message(message):
    await client.process_commands(message)
    author = message.author
    content = (message.content).split()
    if not author.bot:
        for i in content:
            exp = randint(1,2)
            print(exp)
            cursor.execute(f"""UPDATE users SET exp = exp + {exp} WHERE id = {author.id}""")
            connection.commit()
            print(cursor.execute(f"SELECT exp FROM users WHERE id = {author.id}").fetchone())





client.run("ODUyNjQyMjQzNDk5MjYxOTUz.YMJy-A.NfI1VYGzHFmtzsYiEoTI_Zz7pZE")