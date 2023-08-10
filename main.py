import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import os

intents = discord.Intents.all()
intents.members = True


queues = {}

def check_queue(ctx, id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        source = queues[id].pop(0)
        player = voice.play(source)

client = commands.Bot(command_prefix = ";", intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('summertime saga'))
    print("EVE is now online")

@client.command()
async def hello(ctx):
    await ctx.send("Hello, i am EVE")

@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye")


    
@client.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
       # source = FFmpegPCMAudio('infernoalbum.mp3')
       # player = voice.play(source)
        
    else:
        await ctx.send("You are not in a voice channel")

@client.command(pass_context = True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel")

@client.command(pass_context = True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("There is no audio being played at the moment")


@client.command(pass_context =True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("There is no aduio paused")

@client.command(pass_context =True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

@client.command(pass_context =True)
async def play(ctx,arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    player = voice.play(source, after=lambda x=None: check_queue(ctx, ctx.message.guild.id))
 
@client.command(pass_context =True)
async def queue(ctx, arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav ' 
    source = FFmpegPCMAudio(song)

    guild_id = ctx.message.guild.id

    if guild_id in queues:
        queues[guild_id].append(source)

    else:
        queues[guild_id] = [source]

    await ctx.send("Added to queue")

@client.command()
async def threaten(ctx, user:discord.Member, *, message=None):
    message = "7 days"
    embed = discord.Embed(title=message)
    await user.send(embed=embed)



client.run(os.environ["DISCORD_TOKEN"])