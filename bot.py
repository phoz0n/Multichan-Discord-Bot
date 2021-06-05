import discord
import json
import urllib3 
import random
from discord.ext import commands

default_intents = discord.Intents.default()
default_intents.members = True
#client = discord.Client(intents=default_intents)
client = commands.Bot(command_prefix = '!')
http = urllib3.PoolManager()

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message):
     
    if message.author == client.user:
        return
    
    #4chan random img
    if message.content.lower().startswith('random'):
        
        #Search board
        searchBoard = str(message.content).split(' ')
        if len(searchBoard) == 1:
            board = 'wsg'
        else:
            board = searchBoard[1]
        
        #Fetch threads from bord Worksafe gifs
        response = http.request('GET', 'https://a.4cdn.org/' + board + '/catalog.json')
        
        if response.status != 200:
            response = http.request('GET', 'https://a.4cdn.org/boards.json')
            board_response = json.loads(response.data)
            board_list = board_response['boards']
            boards = list(map(lambda z: '/' + z['board'] + '/', board_list))
            print('\n'.join(boards))
            await message.channel.send(' '.join(boards))
            return    
        
        pages = json.loads(response.data)
        
        threads = []
        for i in pages:
            threads = threads+i["threads"]
        
        #Exclude threads without images
        threads_images = list(filter(lambda x: x['images'] > 0, threads))
        
        #Fetch a random thread from threads
        thread_pif = threads_images[random.randrange(0,len(threads_images)-1)]
        response = http.request('GET', 'https://a.4cdn.org/' + board + '/thread/' + str(thread_pif['no']) + '.json')
        thread = json.loads(response.data)
        posts = thread['posts']
        
        #Exclude posts without images from the random thread
        posts_images = list(filter(lambda x: 'filename' in x, posts))
        
        #Fetch a random post from the random thread
        post_pif = posts_images[random.randrange(0,len(posts_images)-1)]
         
        #Send the webm to discord channel
        await message.channel.send('https://is2.4chan.org/'+ board +'/' + str(post_pif['tim']) + str(post_pif['ext']))
        return
    
client.run('')


