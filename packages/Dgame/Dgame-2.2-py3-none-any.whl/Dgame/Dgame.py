import discord
import asyncio
        
async def dgame(ca, meg, sleeps):
    while True:
        await ca.change_presence(status=discord.Status.online, activity=discord.Game(name=meg[0]))
        meg.append(meg.pop(0))
        await asyncio.sleep(sleeps)

