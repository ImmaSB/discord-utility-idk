import discord
from discord.ext import commands
import requests
import aiohttp
import random
from discord.ext.commands import CommandNotFound

prefix = ""

bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), case_insensitive=True, intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity = discord.Game(name=f'{prefix}help for a list of commands! Currently in {len(bot.guilds)} server(s)!'))
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.channel.send("Command Not Found, Please Try Again!")
    
@bot.command()
async def help(ctx):
  em = discord.Embed(title="Help Has Arrived!", description=f"List of commands available for the bot{prefix}", color=ctx.author.color)
  em.add_field(name=f"**Prefix**", value=f"**My Prefix Is** `{prefix}` (Dot)", inline=False)
  em.add_field(name=f"**Basic Commands**", value=f"`{prefix}latency`   `{prefix}myid`   `{prefix}pfp`   `{prefix}aboutme`", inline=False)
  em.add_field(name=f"**Moderation**", value=f"`{prefix}kick [user] [reason]`   `{prefix}ban [user] [reason]`   `{prefix}unban [user#discriminator]`   `{prefix}clear [amount of messages]`   `{prefix}mute [member] [reason]`   `{prefix}unmute [member] [reason]`", inline=False)
  em.add_field(name=f"**Utility**", value=f"`{prefix}modmail [ping mod] [content]`   `{prefix}sum [value 1] [value 2]`   `{prefix}multiply [value 1] [value 2]`   `{prefix}subtract [value 1] [value 2]`   `{prefix}divide [value 1] [value 2]`", inline=False)
  em.add_field(name=f"**Fun**", value=f"`{prefix}meme`   `{prefix}dankmeme`   `{prefix}cats`", inline=False)
  
  em.set_footer(text=f"Requested by {ctx.author.display_name}")
  em.set_thumbnail(url=ctx.author.avatar_url)
  await ctx.channel.send(embed=em)
  
  
@bot.command(aliases=["myping", "ping"])
async def latency(ctx):
  await ctx.channel.send("My Latency Is " + str(round(bot.latency*1000)) + "ms")

@bot.command()
async def myid(ctx, member: discord.Member=None):
  member = member or ctx.author
  await ctx.channel.send(f"ID Of {member.display_name}: `{member.id}`")

@bot.command(aliases=["mm", "dmmod"])
async def modmail(ctx, member:discord.Member, *, content):
  em = discord.Embed(title="New Modmail!")
  em.add_field(name="Content: ", value = content)
  em.set_footer(text=f"Message From {ctx.author}", icon_url=ctx.author.avatar_url)

  await member.send(embed=em)

@bot.command(aliases=["profilepic"])
async def pfp(ctx, member: discord.Member=None):
  member = member or ctx.author
  em = discord.Embed(color = member.color, timestamp = ctx.message.created_at)
  em.set_thumbnail(url=member.avatar_url)

  await ctx.channel.send(embed=em)
  
@bot.command(aliases=["about", "spy", "profile"])
async def aboutme(ctx, member: discord.Member=None):
  member = member or ctx.author
  roles = member.roles
  em = discord.Embed(color = member.color, timestamp=ctx.message.created_at)
  em.set_author(name=f"User Info - {member}")
  em.set_thumbnail(url=member.avatar_url)
  em.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
  em.add_field(name="ID: ", value = member.id)
  em.add_field(name="Guild Game: ", value=member.display_name)
  em.add_field(name="Created At: ", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))
  em.add_field(name="Joined at: ", value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %P UTC"))
  em.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
  em.add_field(name="Top role: ", value=member.top_role.mention)

  await ctx.channel.send(embed=em)

@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, limit: int):
  if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=limit+1)
        await ctx.send(f'{limit} Messages Cleared by {ctx.author.mention}', delete_after=3)
  else:
    ctx.channel.send(f"{ctx.author.mention}, You don't have the needed permission")

@bot.command(aliases=["cat", "meow", "cutecats"])
async def cats(ctx):
  r = requests.get('http://aws.random.cat/meow')
  if r.status_code == 200:
      js = r.json()
      await ctx.channel.send(js['file'])

@bot.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, member: discord.Member=None, *, reason=None):
  member == None or member
  if member == None:
    await ctx.channel.send("You can't kick yourself chad")
  elif member == ctx.message.author:
    await ctx.channel.send("Can't Kick Yourself Chad")
  else:
    await member.kick(reason=reason)
    await ctx.channel.send(f'User {member} has kicked.')


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None, *, reason=None):
  reason == reason or "For Being A Retard"
  member == None or member
  if member == None:
    await ctx.channel.send("You can't ban yourself chad")
  elif member == ctx.message.author:
    await ctx.channel.send("Can't Ban Yourself Chad")
  else:
    await member.ban(reason=reason)
    await ctx.channel.send(f'User {member} has banned, Reason: {reason}')

@bot.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split("#")
  
  for ban_entry in banned_users:
    user = ban_entry.user

    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.channel.send(f"Unbanned {user.name}#{user.discriminator}")

@bot.command(aliases=["add"])
async def sum(ctx, first: int, second: int):
    await ctx.reply(f"{first}+{second}={first+second}")
    
@bot.command(aliases=["minus"])
async def subtract(ctx, first: int, second: int):
    await ctx.reply(f"{first}-{second}={first-second}")

@bot.command()
async def multiply(ctx, first: int, second: int):
    await ctx.reply(f"{first}*{second}={first*second}")

@bot.command()
async def divide(ctx, first: int, second: int):
    await ctx.reply(f"{first}/{second}={first/second}")

@bot.command(aliases=["memes"], pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="Memes", description="Your Daily Dose Of Memes!")
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command(aliases=["dankmemes", "dank"], pass_context=True)
async def dankmeme(ctx):
    embed = discord.Embed(title="Memes", description="Your Daily Dose Of **Dank** Memes!")
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason: str = None):
        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)
        if not muted_role:
            return await ctx.send("There is no role called **Muted**")
        try:
            await member.add_roles(muted_role, reason=reason)
            await ctx.send(f"{member.mention} has been muted.")
        except Exception as e:
            await ctx.send(e)


@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member, *, reason: str = None):
        muted_role = next((g for g in ctx.guild.roles if g.name == "Muted"), None)
        if not muted_role:
            return await ctx.send("There is no role called **Muted**")
        try:
            await member.remove_roles(muted_role, reason=reason)
            await ctx.send(f"{member.mention} has been unmuted.")
        except Exception as e:
            await ctx.send(e)

 
bot.run("TOKEN HERE") # https://discord.com/developers
