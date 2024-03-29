import discord
from discord.ext import tasks
from discord.client import Client
import json
import urllib3
import random
import os
from dotenv import load_dotenv
from yandex import YandexImage
import re

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.counter = 0

    async def setup_hook(self) -> None:
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(hours=3)
    async def my_background_task(self):
        await self.wait_until_ready()
        response = http.request('GET', 'https://www.reddit.com/r/18_19/random.api', headers={'User-agent':useragent} )
        data = json.loads(response.data)
        channel = self.get_channel(channel_id)
        try:
            gallery = ''
            for x in data[0]['data']['children'][0]['data']['gallery_data']['items']:
                gallery = gallery + 'https://i.redd.it/' + x['media_id'] + '.jpg '
            await channel.send(gallery)
            return
        except:
            pass
        try:
            await channel.send(data[0]['data']['children'][0]['data']['title'] + ' ' + data[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url'])
            return
        except:
            pass
        try:
            await channel.send(data[0]['data']['children'][0]['data']['title'] + ' ' + data[0]['data']['children'][0]['data']['url'])
        except:
            await channel.send('Not found 🤖')

            await channel.send(self.counter)
    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in
    
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
http = urllib3.PoolManager()

load_dotenv()
intents = discord.Intents.default()
client = MyClient(intents=discord.Intents.default())
channel_id = int(os.getenv('CHANNEL'))
channel = client.get_channel(channel_id)
http = urllib3.PoolManager()
quatrechan_boards = ['3','a','aco','adv','an','b','bant','biz','c','cgl','ck','cm','co','d','diy','e','f','fa','fit','g','gd','gif','h','hc','his','hm','hr','i','ic','int','jp','k','lgbt','lit','m','mlp','mu','n','news','o','out','p','po','pol','pw','qa','qst','r','r9k','s','s4s','sci','soc','sp','t','tg','toy','trash','trv','tv','u','v','vg','vip','vm','vmg','vp','vr','vrpg','vst','vt','w','wg','wsg','wsr','x','xs','y']
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
accept = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
redditModeList = ['hot', 'new', 'top', 'rising', 'random', 'controversial', 'best']
badWords = os.getenv('BADWORDS').split(",")
game = discord.Game("Counter-Strike: Global Offensive")

async def reddit(board, message: discord.Message):
    response = http.request('GET', 'https://www.reddit.com/r/' + board + '/random.api', headers={'User-agent':useragent} )
    data = json.loads(response.data)
    try:
        gallery = ''
        for x in data[0]['data']['children'][0]['data']['gallery_data']['items']:
            gallery = gallery + 'https://i.redd.it/' + x['media_id'] + '.jpg '
        await message.reply(gallery)
        return
    except:
        pass
    try:
        await message.reply(data[0]['data']['children'][0]['data']['title'] + ' ' + data[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url'])
        return
    except:
        pass
    try:
        await message.reply(data[0]['data']['children'][0]['data']['title'] + ' ' + data[0]['data']['children'][0]['data']['url'])
    except:
        await message.reply('Not found, try this instead \n Random image from subreddit pic: random pic \n Random image from 4chan /g/: random g \n Random image from yandex: image cat')

async def quatrechamps(board, message: discord.Message):
    r = http.request('GET', 'https://a.4cdn.org/' + board + '/catalog.json')
    pages = json.loads(r.data)

    threads = []
    for i in pages:
        threads = threads+i["threads"]

    #Exclude threads without images
    threads_images = list(filter(lambda x: x['images'] > 0, threads))

    #Fetch a random thread from threads
    thread_pif = threads_images[random.randrange(0,len(threads_images)-1)]
    r = http.request('GET', 'https://a.4cdn.org/' + board + '/thread/' + str(thread_pif['no']) + '.json')
    thread = json.loads(r.data)
    posts = thread['posts']

    #Exclude posts without images from the random thread
    posts_images = list(filter(lambda x: 'filename' in x, posts))

    #Fetch a random post from the random thread
    post_pif = posts_images[random.randrange(0,len(posts_images)-1)]

    #Send the webm to discord channel
    msg = await message.reply('https://i.4cdn.org/'+ board +'/' + str(post_pif['tim']) + str(post_pif['ext']))

    if board == 'b':
        await msg.add_reaction(emoji="🤔")

@client.event
async def on_message(message: discord.Message):

    if message.author == client.user:
        return

    if message.channel.id != channel_id:
        return

    for i in badWords:
       if i in message.content:
            await message.reply(message.author.display_name + ' pas de ça chez nous!')
            await message.add_reaction('💩')
            return
    
    if message.content.lower().startswith('help'):
        await message.reply('Random image from subreddit pic: random pic \n Random image from 4chan /g/: random g \n Random image from yandex: image cat \n Random TikTok from trending: tiktok')
        return

    if message.content.lower().startswith('wesh'):
        await message.reply('wesh alors!')
        return

    #4chan random img
    if message.content.lower().startswith('random'):

        #Split received words in array
        searchBoard = str(message.content).split(' ')
        if len(searchBoard) == 1:
            board = 'wsg'
        else:
            board = searchBoard[1]

        #4chan boards
        if board in quatrechan_boards:
            await quatrechamps(board,message)

        #Reddit subreddits
        else:
            await reddit(board,message)
        return

    # Yandex image search
    if message.content.lower().startswith('image'):
        parser = YandexImage()
        yandexsearch = str(message.content).split(' ')
        r = parser.search(yandexsearch[1])
        randomIndex = random.randint(0, len(r)-1)
        await message.reply(r[randomIndex].url)
        return
    
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
http = urllib3.PoolManager()

load_dotenv()
intents = discord.Intents.default()
client = MyClient(intents=discord.Intents.default())
channel_id = int(os.getenv('CHANNEL'))
channel = client.get_channel(channel_id)
http = urllib3.PoolManager()
quatrechan_boards = ['3','a','aco','adv','an','b','bant','biz','c','cgl','ck','cm','co','d','diy','e','f','fa','fit','g','gd','gif','h','hc','his','hm','hr','i','ic','int','jp','k','lgbt','lit','m','mlp','mu','n','news','o','out','p','po','pol','pw','qa','qst','r','r9k','s','s4s','sci','soc','sp','t','tg','toy','trash','trv','tv','u','v','vg','vip','vm','vmg','vp','vr','vrpg','vst','vt','w','wg','wsg','wsr','x','xs','y']
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'
accept = 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
redditModeList = ['hot', 'new', 'top', 'rising', 'random', 'controversial', 'best']
badWords = os.getenv('BADWORDS').split(",")
game = discord.Game("Counter-Strike: Global Offensive")

async def reddit(board, message: discord.Message):
    response = http.request('GET', 'https://www.reddit.com/r/' + board + '/random.api', headers={'User-agent':useragent} )
    data = json.loads(response.data)
    try:
        gallery = ''
        for x in data[0]['data']['children'][0]['data']['gallery_data']['items']:
            gallery = gallery + 'https://i.redd.it/' + x['media_id'] + '.jpg '
        await message.reply(gallery)
        return
    except:
        pass
    try:
        await message.reply(data[0]['data']['children'][0]['data']['title'] + ' ' + data[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url'])
        return
    except:
        pass
    try:
        await message.reply(data[0]['data']['children'][0]['data']['title'] + ' ' + data[0]['data']['children'][0]['data']['url'])
    except:
        await message.reply('Not found, try this instead \n Random image from subreddit pic: random pic \n Random image from 4chan /g/: random g \n Random image from yandex: image cat')

async def quatrechamps(board, message: discord.Message):
    r = http.request('GET', 'https://a.4cdn.org/' + board + '/catalog.json')
    pages = json.loads(r.data)

    threads = []
    for i in pages:
        threads = threads+i["threads"]

    #Exclude threads without images
    threads_images = list(filter(lambda x: x['images'] > 0, threads))

    #Fetch a random thread from threads
    thread_pif = threads_images[random.randrange(0,len(threads_images)-1)]
    r = http.request('GET', 'https://a.4cdn.org/' + board + '/thread/' + str(thread_pif['no']) + '.json')
    thread = json.loads(r.data)
    posts = thread['posts']

    #Exclude posts without images from the random thread
    posts_images = list(filter(lambda x: 'filename' in x, posts))

    #Fetch a random post from the random thread
    post_pif = posts_images[random.randrange(0,len(posts_images)-1)]

    #Send the webm to discord channel
    msg = await message.reply('https://i.4cdn.org/'+ board +'/' + str(post_pif['tim']) + str(post_pif['ext']))

    if board == 'b':
        await msg.add_reaction(emoji="🤔")

@client.event
async def on_message(message: discord.Message):

    if message.author == client.user:
        return

    if message.channel.id != channel_id:
        return

    for i in badWords:
       if i in message.content:
            await message.reply(message.author.display_name + ' pas de ça chez nous!')
            await message.add_reaction('💩')
            return
    
    if message.content.lower().startswith('help'):
        await message.reply('Random image from subreddit pic: random pic \n Random image from 4chan /g/: random g \n Random image from yandex: image cat \n Random TikTok from trending: tiktok')
        return

    if message.content.lower().startswith('wesh'):
        await message.reply('wesh alors!')
        return

    #4chan random img
    if message.content.lower().startswith('random'):

        #Split received words in array
        searchBoard = str(message.content).split(' ')
        if len(searchBoard) == 1:
            board = 'wsg'
        else:
            board = searchBoard[1]

        #4chan boards
        if board in quatrechan_boards:
            await quatrechamps(board,message)

        #Reddit subreddits
        else:
            await reddit(board,message)
        return

    # Yandex image search
    if message.content.lower().startswith('image'):
        parser = YandexImage()
        yandexsearch = str(message.content).split(' ')
        r = parser.search(yandexsearch[1])
        randomIndex = random.randint(0, len(r)-1)
        await message.reply(r[randomIndex].url)
        return

client.run(os.getenv('TOKEN'))