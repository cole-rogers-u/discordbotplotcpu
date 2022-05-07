
import os
import discord
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from discord.ext import commands
import io
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
data_stream = io.BytesIO()
bot = commands.Bot(command_prefix='$')
DF = pd.read_csv("CPU_benchmark.csv")
DF['cpuMark'] = pd.to_numeric(DF['cpuMark'],errors='coerce')
DF['threadMark'] = pd.to_numeric(DF['threadMark'],errors='coerce')

def searchFunc(df, subtring, column):
    return df[df[column].str.contains(subtring,case=False)]

try:
    cpus = pd.read_csv("CPU_benchmark.csv")
except Exception as e:
    print(e)

@bot.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@bot.command()
async def cpubot(ctx):
    help = "Type $cpubot for help\nType $search \"cpuname\" to search\n\
Type $showAllCPU to get a summary of every CPU's benchmark score\n\
Type $showMyCPU \"cpuName\" to see the selected cpu on a histogram\n use $showMyThread to see your thread on a histogram"
    await ctx.send(help)

@bot.command()
async def search(ctx, subtring):
    result = searchFunc(DF, subtring, 'cpuName')
    message = ""
    if result.shape[0] == 0:
        message = "ERROR: CPU not found.\n"
        result = ""
    elif result.shape[0] > 10:
        message = "TOO MANY VALUES: Try a more specific search.\n"
    await ctx.send('{} {}'.format(message, result))



@bot.command()
async def showAllCPU(ctx):
    plt.hist(DF['cpuMark'])
    plt.savefig("temp.png")
    plt.close()
    image = discord.File("temp.png")
    await ctx.send("Here is a histogram of all CPUs CPU mark scores")
    await ctx.send(file=image)


@bot.command()
async def showMyCPU(ctx,sub):
    if not sub:
        await ctx.send("Format: showMyCPU \"cpuName\"")
        return
    cpu = searchFunc(DF, sub, 'cpuName')
    plt.hist(DF['cpuMark'])
    if cpu['cpuMark'].loc[cpu.index[0]] == 0:
        await ctx.send("data not found for this cpu")
    plt.axvline(cpu['cpuMark'].loc[cpu.index[0]], color='k', linestyle='dotted', linewidth=5)
    plt.savefig("temp.png")
    plt.close()
    image = discord.File("temp.png")
    await ctx.send("Here is a histogram of all CPUs CPU mark scores")
    await ctx.send(file=image)

@bot.command()
async def showMyThread(ctx,sub):
    if not sub:
        await ctx.send("Format: showMyCPU \"cpuName\"")
        return
    cpu = searchFunc(DF, sub, 'cpuName')
    if cpu.shape[0] != 1:
        await ctx.send("Enter exact CPU name")
        return
    plt.hist(DF['threadMark'])
    plt.axvline(cpu['threadMark'].loc[cpu.index[0]], color='k', linestyle='dotted', linewidth=5)
    plt.savefig("temp.png")
    plt.close()
    image = discord.File("temp.png")
    await ctx.send("Here is a histogram of all CPUs Thread mark scores")
    await ctx.send(file=image)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

bot.run(TOKEN)
