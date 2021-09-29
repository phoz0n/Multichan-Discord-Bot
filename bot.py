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
quatrechan_boards = ['3','a','aco','adv','an','b','bant','biz','c','cgl','ck','cm','co','d','diy','e','f','fa','fit','g','gd','gif','h','hc','his','hm','hr','i','ic','int','jp','k','lgbt','lit','m','mlp','mu','n','news','o','out','p','po','pol','pw','qa','qst','r','r9k','s','s4s','sci','soc','sp','t','tg','toy','trash','trv','tv','u','v','vg','vip','vm','vmg','vp','vr','vrpg','vst','vt','w','wg','wsg','wsr','x','xs','y']
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
redditModeList = ['hot', 'new', 'top', 'rising', 'random', 'controversial', 'best']
@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message):
     
    if message.author == client.user:
        return
    
    #4chan random img
    if message.content.lower().startswith('random'):
        
        #Split received words in array
        searchBoard = str(message.content).split(' ')
        redditMode = 'random' #hot, new, top, rising, random, controversial
        if len(searchBoard) == 1:
            board = 'wsg'
        else:
            board = searchBoard[1]

        #if len(searchBoard) == 3 and searchBoard[2] in redditModeList:
        #   redditMode = searchBoard[2]

        #4chan boards
        if board in quatrechan_boards:
            response = http.request('GET', 'https://a.4cdn.org/' + board + '/catalog.json')
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

        #Reddit subreddits
        else:
            response = http.request('GET', 'https://www.reddit.com/r/' + board + '/' + redditMode + '.api', headers={'User-agent':useragent} )
            data = json.loads(response.data)
            try:
                await message.channel.send(data[0]['data']['children'][0]['data']['title'] + ' ' + data[0]['data']['children'][0]['data']['url'] )
            except:
                await message.channel.send('Not found')
            return

client.run('')
