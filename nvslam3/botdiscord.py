import discord
import mysql.connector
from mysql.connector import Error
from discord.ext import tasks, commands

intents = discord.Intents().all()
client = commands.Bot(command_prefix='!', intents=intents)
# Remplacez ces informations par les vôtres
DATABASE = 'portfolio'
USER = 'root'
PASSWORD = ''
HOST = '127.0.0.1'
BOT_TOKEN = ''

# Établir une connexion à la base de données
try:
    conn = mysql.connector.connect(
        host=HOST,
        database=DATABASE,
        user=USER,
        password=PASSWORD
    )
    print('Connexion à la base de données réussie!')
except Error as e:
    print(f'Erreur de connexion à la base de données: {e}')

# Définir l'ID du salon où envoyer les messages
channel_id = 1106488839662477427  # Remplacez par l'ID de votre salon


# Fonction pour envoyer un message Discord
async def send_message(channel_id, msg):
    channel = client.get_channel(channel_id)
    if not channel:
        print(f"Channel not found with ID {channel_id}")
        return
    await channel.send(msg)
    print(f'Message envoyé : {msg}')

def get_new_contacts():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE Notification = 0')
    new_contacts = cursor.fetchall()
    cursor.close()
    print(f'Contacts récupérés : {new_contacts}')
    return new_contacts

@tasks.loop(minutes=1)
async def check_contacts():
    channel_id = 1106488839662477427
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contacts WHERE Notification = 0')
    new_contacts = cursor.fetchall()
    if new_contacts :
        for contact in new_contacts:
            if not contact[6]: # Vérifier si le champ "sent" est False
                msg = f'Nouveau contact: {contact[1]} ({contact[2]})\nSujet: {contact[3]}\nMessage: {contact[4]}'
                await send_message(channel_id, msg)
                print(f'Message envoyé : {msg}')
                cursor = conn.cursor()
                cursor.execute('UPDATE contacts SET Notification = %s WHERE id = %s', (True, contact[0])) # Mettre le champ "sent" à True
                conn.commit()
                cursor.close()



@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0}'.format(round(client.latency, 1)))


# Démarrer la tâche périodique
@client.event
async def on_ready():
    print('Bot connecté à Discord!')
    check_contacts.start()


# Démarrer le client Discord
client.run(BOT_TOKEN)
