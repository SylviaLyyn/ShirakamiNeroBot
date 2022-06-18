import discord
import os
import requests
import json
import random
import asyncio
import typing
from discord.ext import commands,tasks
from googletrans import Translator
import numpy as np

description = '''An example bot to showcase the discord.ext.commands extension
module.'''

#setup
activity=discord.Game(name="Nero at Your Service!")
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='?', description=description, intents=intents, activity=activity, status=discord.Status.idle)
client = discord.Client(intents=intents)
normalmsg = commands.Bot(command_prefix='!',intents=discord.Intents.all())


# sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]

#listbahasa
languages = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
}

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person",
  "I will sing a song for you",
  ":fire:",
  "Aku selalu ada disisimu"
]

roll_responses = [
  ":ok_hand: | What a bad day... It's a ", 
  ":ok_hand: | What a lucky day! It's a ", 
  ":ok_hand: | Nice! It's a ",
  ":ok_hand: | Booo.. It's a ", 
  ":ok_hand: | Yikes! It's a "
]

hai = ['hello','hai','hi','halo','nero']
sedih = ['sedih','sad','mengsad','mengsedih']

#nyari quote
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#tl ges
def get_translate(bahasa: str, isi: str):
  translator = Translator()
  translation = translator.translate(isi, dest=bahasa)
  return(translation.text)

#namabot
def namabot(teks):
  a = len(teks)
  return(teks[:a-5])
  

# ------------------------------ Mulai Command Bot ------------------------------

#pas diidupin
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

# ini dimatiin kalau mau comand bawahnya bekerja semua
@bot.event
async def on_message(message):
  username = str(message.author).split('#')[0]
  user_message = str(message.content)
  channel = str(message.channel.name)

  print(f'{username}: {user_message} ({channel})')
  
  if user_message.lower() in hai:
    await message.channel.send(f'Hai bang {username}')
    return

#tambah 2 angka
@bot.command()
async def add(ctx, *num):
    x = 0;
    for i in num:
      x = x+int(i);
    """Adds two numbers together."""
    await ctx.send("Your result: " + str(x))

#kapan sebuah member join
@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')

#roll dice
@bot.command()
async def dice(ctx, dice: str):
    """Roll dadu n sisi sebanyak n kali (NdN format)"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format harus NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

#roll random
@bot.command()
async def roll(ctx, limit: int):
  """Memilih bilangan random dari 1 sampai n"""
  result2 = random.choice(roll_responses) + str(random.randint(1, limit)) + "!"
  result1 = ":game_die: | You roll a " + str(limit) + " sided dice!"
  await ctx.send (result1)
  await ctx.send (result2)

# @bot.command()
# async def graph(ctx):
#   fig, ax = plt.subplots()
#   u = np.linspace(0, 10, 8, endpoint=True)
#   ax.plot(u, np.cos(u))
#   await ctx.send(plt.show())


@bot.command()
async def cheer(ctx):
  """Penyemangat"""
  result = str(random.choice(starter_encouragements) + " / " + namabot(str(bot.user)))
  await ctx.send(result)

@bot.command()
async def hash(ctx, base: int, mod: int):
  """Create Hashing Base on The Algorithm Input"""
  finalhash = base % mod
  result = "Index array = " + str(finalhash)
  await ctx.send(result)

@bot.command()
async def quote(ctx):
  """Quote random"""
  quote = get_quote()
  await ctx.send(quote)

@bot.command()
async def tl(ctx, *, isi):
  """Translate ke bahasa lain (lihat ?bahasa untuk list bahasa)"""
  tujuan = isi[:2]
  kalimat = isi[3:]
  try:
    get_translate(tujuan, kalimat)
  except:
    await ctx.send("Bahasa tidak ditemukan!")
  else:
    await ctx.send(get_translate(tujuan, kalimat))

@bot.command()
async def luas(ctx, bangun: typing.Optional[str] = 'gaada', param1=-1, param2=1):
  """Menghitung luas"""
  if param1 == -1 or bangun == 'gaada':
    await ctx.send(':negative_squared_cross_mark: | Gagal melakukan perhitungan!')
    await ctx.send(':white_check_mark: | ?luas <bangun> <parameter1> <parameter>')
  else:
    if bangun == 'segitiga':
      luas = round(((param1*param2)/2), 2)
      result1 = ":triangular_ruler: | Alas = " + str(param1) + ", Tinggi = " + str(param2) + " ..."
      result2 = ":ok_hand: | Luas Segitiga: " + str(luas)
      await ctx.send(result1)
      await ctx.send(result2)
    elif bangun == 'segiempat':
      luas = round(((param1*param2)), 2)
      result1 = ":orange_square: | Panjang = " + str(param1) + ", Lebar = " + str(param2) + " ..."
      result2 = ":ok_hand: | Luas Segiempat: " + str(luas)
      await ctx.send(result1)
      await ctx.send(result2)
    else:
      await ctx.send('Bangun tidak valid!')

@bot.command()
async def bahasa(ctx):
  """List bahasa"""
  await ctx.send(languages)

  
  


bot.run(os.environ['nero'])