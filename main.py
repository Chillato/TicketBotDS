import discord
from discord.ext import commands
from discord.ui import Button, View
import sqlite3
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc
try:
    conn = sqlite3.connect("ticket.db")
    conn.cursor().execute("CREATE TABLE IF NOT EXISTS ticket (openticket INT)")
    conn.commit()
except:
    pass
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Bot online")

@client.command()
@commands.has_permissions(administrator=True)
async def ticket(ctx):
    button = Button(label="Crea ticket 📨", style=discord.ButtonStyle.primary)
    button.callback = ticketfunction
    v = View(timeout=None).add_item(button)
    embed = discord.Embed(title="✉️ TICKET ✉️", description="Hai bisogno di aiuto o hai problemi? bene apri un ticket")
    embed.set_thumbnail(url="https://w7.pngwing.com/pngs/94/36/png-transparent-ticket-cinema-others-text-rectangle-logo.png")
    await ctx.send(embed=embed, view=v)

async def ticketfunction(interaction: discord.Interaction):
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name="aa") # mettere il ruolo che può accedere al ticket
    dio = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        interaction.user: discord.PermissionOverwrite(view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }
    if isOpen(interaction.user.id):
        await interaction.response.send_message("Hai già aperto un ticket aspetta 24 ore", ephemeral=True)
    else:
        closebtn = Button(label="Chiudi ticket 🔐", style=discord.ButtonStyle.red)
        closebtn.callback = close_ticket
        v = View(timeout=None).add_item(closebtn)
        channel = await interaction.guild.create_text_channel(name=f"{interaction.user.name}-ticket", overwrites=dio)
        ticketcreate = discord.Embed(title="🆘 Benvenuto nel ticket 🆘", description=f"Benvenuto nel tuo ticket ora chiedi quello che devi chiedere gli staff ti risponderanno presto")
        await channel.send(embed=ticketcreate, view=v)
        await interaction.response.send_message(f"Ho creato il tuo ticket con successo", ephemeral=True)
        conn.cursor().execute("INSERT INTO ticket (openticket) VALUES (?)", [interaction.user.id])
        conn.commit() 

async def close_ticket(interaction: discord.Interaction):
    if interaction.user.get_role(111) or interaction.user.get_role(111) or interaction.user.get_role(1111): # id dei ruoli
        await interaction.channel.delete()
async def reset_db():
    for a, in conn.cursor().execute("SELECT openticket FROM ticket").fetchall():
        try:
            conn.cursor().execute("DELETE FROM ticket WHERE openticket = ?", [a])
            conn.commit()
        except:
            pass

def isOpen(user_id: int):
    result = conn.cursor().execute("SELECT openticket FROM ticket WHERE openticket = ?", [user_id])
    if len(result.fetchall()) > 0:
        return True
    else:
        return False
    
scheduler = AsyncIOScheduler()
scheduler.add_job(reset_db, "interval", timezone=utc, minutes=86400)
scheduler.start()

client.run("MTA5MTg5NjMzODYyMDM2Mjc4MQ.G3fvBO.bX2SCBiVefZ-tg3Lt-2vFIYZV80JtM32pSwOFY")