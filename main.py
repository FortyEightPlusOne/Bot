import twitchio
import os
from twitchio.ext import commands
from tmbconfig import *
import random
from random import *
import requests
import time

counters = []
chanl = ""
queue = []
goal = 0
badgePerms=["idk"]

cooldowns = {"fortune":[0,10]}

def isNotOnCooldown(a):
    t=cooldowns[a]
    if time.time() - t[0] > t[1]:
         t[0] = time.time()
         cooldowns[a]=t
         return True
    else:
        return False

lastmsgs={}


# was working on a system to make the bot not respond in certain situations to prevent spam
'''def canrespond(id):
    try:
        last=lastmsgs[id]
        cooldown=int(open("data/users/"+str(id)+"/cooldown.txt").read())
        if time.time()-last > cooldown:
            return True
        else:
            return False
    except:
        lastmsgs[id]=time.time()
        return True'''

def getperms(id):
    return open("data/users/"+str(id)+"/perms.txt").read().split("\n")

def hasperm(id,perm):
    perms=getperms(id)
    return perm in perms

def getgrants(id):
    return open("data/users/"+str(id)+"/grants.txt").read().split("\n")

def hasgrant(id,grant):
    return grant in getgrants(id)

bot = commands.Bot(
    irc_token=TMI_TOKEN,
    client_id=CLIENT_ID,
    nick=BOT_NICK,
    prefix=BOT_PREFIX,
    initial_channels=CHANNEL,
    client_secret=CLIENT_SECRET
)

@bot.event
async def event_ready():
    global chanl
    chanl = bot.get_channel("technoblade")
    await chanl.send("pogging irl")

@bot.event
async def event_message(msg):
    if msg.author.id == 0:
        print(f"{msg.author.name.lower()}: {msg.content}")
        return
    #canmsg=canrespond(msg.author.id)
    print(f"{msg.author.name.lower()}: {msg.content}")
    global goal
    if not os.path.exists("data/users/"+str(msg.author.id)):
        os.makedirs("data/users/"+str(msg.author.id))
        f=open("data/users/"+str(msg.author.id)+"/cooldown.txt","w")
        f.write("3")
        f.close()
        f=open("data/users/"+str(msg.author.id)+"/perms.txt","w")
        f.write("sendcommands\n")
    if not os.path.exists("data/users/"+str(msg.author.id)+"/grants.txt"):
        f=open("data/users/"+str(msg.author.id)+"/grants.txt","w")
        f.write(".\n")
        f.close()
    path="data/users/"+str(msg.author.id)+"/"
    if not os.path.exists(path+"votes"):
        f=open(path+"votes","w")
        f.write(str(0))
        f.close()

    global counters
    #global whitelist2elecboogaloo
    if "48+1" in msg.content and random.randint(0,1) > 0:
        await msg.channel.send(choice(["why are u talking abt me 😳","that do be my name","pogger?","pogger.","hi " + msg.author.name]))
    first = msg.content.split()[0]
    try:
        i = int(first)
        if msg.author.name.lower() in counters:
            if i % 100 == 69:
                await msg.channel.send("nice")
            if i == goal:
                await msg.channel.send("the counter: " + msg.author.name + " hit " + str(goal)+"! do -next to advance the queue.")
            if randint(1,100)<3:
                await msg.channel.send("<3 "+ msg.author.name.upper() + choice([" SUPPORT"," IS 12/10"," FTW"," IS POGGER"]) + " <3")
            if i % 100 == 0 and not i % 500 == 0:
                await msg.channel.send(choice(["another 100! nice <3","can we get a pog for another 100?","gg's :D"]))
    except:
        #nothin here
        print(end="")
    if hasperm(msg.author.id,"sendcommands"):
        await bot.handle_commands(msg)

@bot.command(name="rate")
async def rate(ctx, *,args):
    if args == "me":
        args = ctx.message.author.name
    await ctx.channel.send("i rate " + args+ " a solid "+ str(randint(1,10))+"/10")

# queue rewrite, this isnt how queue works anymore

'''@bot.command(name="setqueue",aliases=["sq"])
async def sq(ctx,*,q):
    global queue
    queue = q
    await ctx.channel.send("queue set")'''

@bot.command(name="queue",aliases=["q"])
async def q(ctx):
    global queue
    s=""
    for i in queue:
        s+=" "+i
    await ctx.channel.send_me(s)

@bot.command(name="clearandadd",aliases=["cadd","ca"])
async def cad(ctx,usera):
    global counters
    counters = []
    if usera not in counters:
        counters.append(usera.lower())
        await ctx.channel.send(usera + " is now counting!")
    else:
        await ctx.channel.send("that user is already counting")

@bot.command(name="imcounting",aliases=["ic"])
async def imcounting(ctx):
    global counters
    if ctx.message.author.name.lower() not in counters:
        counters.append(ctx.message.author.name.lower())
        await ctx.channel.send(ctx.message.author.name + " is now counting!")
    else:
        await ctx.channel.send("ur already on the list lmao")

@bot.command(name="addcounter",aliases=["ac"])
async def imcounting(ctx,usera):
    global counters
    if usera not in counters:
        counters.append(usera.lower())
        await ctx.channel.send(usera + " is now counting!")
    else:
        await ctx.channel.send("that user is already counting")

@bot.command(name='_8ball',aliases=['8ball','8b'])
async def _8ball(ctx, *,question):
    responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
    await ctx.channel.send(f'{choice(responses)}')

@bot.command(name='coin')
async def coin(ctx):
    await ctx.channel.send("It landed on " + f'{choice(["heads","tails"])}')

@bot.command(name='randomnum',aliases=["rn"])
async def rand(ctx,n1,n2):
    r = randint(int(n1),int(n2))
    r = str(r)
    await ctx.channel.send(r)

@bot.command(name="whoscounting",aliases=["list","counters","wc"])
async def whoscounting(ctx):
    global counters
    counterstr = ""
    for i in counters:
        counterstr+=i+" "
    await ctx.channel.send("the current counters are: " + counterstr)

@bot.command(name="imnotcounting",aliases=["inc"])
async def imnotcounting(ctx):
    global counters
    if ctx.message.author.name in counters:
        counters.remove(ctx.message.author.name.lower())
        await ctx.channel.send(ctx.message.author.name + " is no longer a counter!")
    else:
        await ctx.channel.send("you arent counting")

@bot.command(name="bancheck")
async def bancheck(ctx):
    await ctx.channel.send("dont worry " + ctx.message.author.name + ", you arent banned!")

@bot.command(name="removecounter",aliases=["rm","rc","remove","rem"])
async def removecounter(ctx,usera):
    global counters
    if usera in counters:
        counters.remove(usera.lower())
        await ctx.channel.send(usera + " is no longer a counter.")
    else:
        await ctx.channel.send(usera + " wasnt a counter.")

@bot.command(name="click")
async def click(ctx):
    url = "https://clickthatbutton.com"

    x=103
    y=174

    r = requests.post(url,data={"submit.x":str(x),"submit.y":str(y)})

    await ctx.channel.send(r.json())

@bot.command(name="clearcounters",aliases=["clear","c","clr"])
async def clear(ctx):
    global counters
    counters = []
    await ctx.channel.send_me("has cleared the counter list")

@bot.command(name='pokenumber')
async def pokenumber(ctx,pokename):
    r = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokename)
    data = r.json()
    await ctx.channel.send(pokename + "'s number is : " + str(data["game_indices"][0]["game_index"]))

@bot.command(name='pokename')
async def pokename(ctx,pokenumber):
    r = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokenumber)
    data = r.json()
    await ctx.channel.send("Pokemon number " + pokenumber + " is: " + data["species"]["name"])

@bot.command(name = 'pokestats')
async def pokestats(ctx, pokename0, stat0):
    r =  requests.get("https://pokeapi.co/api/v2/pokemon/" + pokename0)
    data = r.json()
    if (stat0 == "weight"):
        await ctx.channel.send(pokename0 + "'s weight is: "+ str(data["weight"]))
    elif (stat0 == "speed"):
        await ctx.channel.send(pokename0 + "'s base speed is: "+ str(data["stats"][0]["base_stat"]))
    elif (stat0 == "special-defence"):
        await ctx.channel.send(pokename0 + "'s base special defence is: "+ str(data["stats"][1]["base_stat"]))
    elif (stat0 == "special-attack"):
        await ctx.channel.send(pokename0 + "'s base special attack is: "+ str(data["stats"][2]["base_stat"]))
    elif (stat0 == "defence"):
        await ctx.channel.send(pokename0 + "'s base defence is: "+ str(data["stats"][3]["base_stat"]))
    elif (stat0 == "attack"):
        await ctx.channel.send(pokename0 + "'s base attack is: "+ str(data["stats"][4]["base_stat"]))
    elif (stat0 == "hp" or stat0 == "health"):
        await ctx.channel.send(pokename0 + "'s base hp is: "+ str(data["stats"][5]["base_stat"]))
    else:
        await ctx.channel.send("sorry, " + stat0 + " isnt a valid stat. the valid stats for pokesats are: speed, special-defence, special-attack, defence, attack, and hp (or health)")


#whitelist removed, no need for these commands at the moment
'''@bot.command(name="whitelistadd",aliases=["wa","wadd"])
async def poggggggg(ctx,usera):
    usera = usera.lower()
    global whitelist2elecboogaloo
    if not usera in whitelist2elecboogaloo:
        whitelist2elecboogaloo.append(usera)
        await ctx.channel.send(f"{usera} added to the whitelist! (since command was used this will only last until bot restarts)")
    else:
        await ctx.channel.send("user already in whitelist")'''

'''@bot.command(name="wlist")
async def poggerchaamppp(ctx):
    global whitelist2elecboogaloo
    string = ""
    for i in whitelist2elecboogaloo:
        string += i+" "
    print(string)'''

# this command was a bad idea

"""@bot.command(name="stop")
async def stop(ctx):
    quit()"""

@bot.command(name="setgoal",aliases=["sg"])
async def setgoal(ctx,ngoal):
    global goal
    try:
        goal = int(ngoal)
        await ctx.channel.send("goal set to " + str(goal))
    except:
        await ctx.channel.send("thats not a number >:C")

@bot.command(name="goal",aliases=["g"])
async def getgoal(ctx):
    global goal
    await ctx.channel.send("the goal is: " + str(goal))

@bot.command(name="id")
async def getID(ctx,t):
    a=await bot.get_users(t)
    await ctx.channel.send(a[0][0])

@bot.command(name="motd")
async def getmotd(ctx):
    await ctx.channel.send("/me " + open("data/motd.txt","r").read())

@bot.command(name="welcome")
async def welcome(ctx,name):
    s=open("data/welcome.txt","r").read()
    s=s.replace("%n",name)
    await ctx.channel.send("/me "+s)

@bot.command(name="edit")
async def edit(ctx,mode,*,text):
    if not hasperm(ctx.author.id,"edit"): return
    if mode=="motd":
        f=open("data/motd.txt","w")
        f.write(text)
        await ctx.channel.send("motd updated")
    elif mode=="motdadd":
        f=open("data/motd.txt","a")
        f.write(text)
        await ctx.channel.send("motd updated")
    elif mode=="welcome":
        f=open("data/welcome.txt","w")
        f.write(text)
        await ctx.channel.send("welcome message updated")
    elif mode=="welcomeadd":
        f=open("data/welcome.txt","a")
        f.write(text)
        await ctx.channel.send("welcome message updated")

@bot.command(name="queueme",aliases=["qm","qme"])
async def qm(ctx):
    global queue
    if not ctx.author.name in queue:
        queue.append(ctx.author.name)

@bot.command(name="dequeueme",aliases=["dqm","deqm","deqme"])
async def dqm(ctx):
    global queue
    queue.remove(ctx.author.name)

@bot.command(name="queuenext",aliases=["next","qn","qnext"])
async def qn(ctx):
    global queue
    if not (hasperm(ctx.author.id,"editqueue") or ctx.author.name == queue[0]): return
    queue=queue[1:]
    await ctx.channel.send(queue[0] + " is up!")

@bot.command(name="dropkick",aliases=["punt"])
async def kick(ctx,target):
    if target=="me": target=ctx.author.name
    await ctx.channel.send_me(" dropkicked "+target)

@bot.command(name="setbio")
async def writebio(ctx, *, text):
    f=open("data/users/"+str(ctx.message.author.id)+"/bio.txt","w")
    f.write(text)

@bot.command(name="bio",aliases=["b"])
async def readb(ctx,name):
    if name=="me": name=ctx.author.name
    a=await bot.get_users(name)
    f=open("data/users/"+a[0][0]+"/bio.txt","r")
    badges=""
    if hasgrant(a[0][0],"idk"): badges+= "[alpha male] "
    elif hasperm(a[0][0],"idk"): badges+= "[idk] "
    if badges=="":badges+='[NBG] '
    await ctx.channel.send_me(badges+ f"{name}'s bio: "+f.read())

@bot.command(name="test")
async def getownid(ctx):
    a=await bot.get_users("fortyeightplusone")
    print(a[0][0])

@bot.command(name="red")
async def red(ctx):
    f=open("data/users/"+str(ctx.author.id)+"/cooldown.txt","r+")
    '''if "." in f.read():
        f.seek(0)
        f.write("0")
        f.seek(0)'''
    if time.time()-float(f.read()) > 3600:
        f.seek(0)
        f.write(str(time.time()))
        f=open("data/red.txt","r+")
        r=f.read()
        f.seek(0)
        f.write( str( int( r ) + 1 ) )
        f.seek(0)
        await ctx.channel.send("red: "+f.read()+" blue: "+open("data/blue.txt","r").read())

@bot.command(name="blue")
async def blue(ctx):
    f=open("data/users/"+str(ctx.author.id)+"/cooldown.txt","r+")
    '''if "." in f.read():
        f.seek(0)
        f.write("0")
        f.seek(0)'''
    if time.time()-float(f.read()) > 3600:
        f.seek(0)
        f.write(str(time.time()))
        f.seek(0)
        f=open("data/blue.txt","r+")
        r=f.read()
        f.seek(0)
        f.write( str( int( r ) + 1 ) )
        f.seek(0)
        await ctx.channel.send("red: "+open("data/red.txt","r").read()+" blue: "+f.read())

@bot.command(name="setln",aliases=["setnum","setlast","sl"])
async def setln(ctx,new):
    f=open("data/lastnum","w")
    f.write(new)
    await ctx.channel.send("lastnum set")

@bot.command(name="lastnum",aliases=["ln"])
async def getln(ctx):
    await ctx.channel.send(open("data/lastnum","r").read())

@bot.command(name="grant",aliases=["g"])
async def grant(ctx,user,perm):
    id1=ctx.author.id
    id2=await bot.get_users(user)
    id2=id2[0][0]
    path="data/users/"+str(id2)+"/perms.txt"
    if hasgrant(id1,perm.strip()) and os.path.exists(path) and not hasperm(id2,perm):
        f=open(path,"a")
        f.write(perm.strip()+"\n")

@bot.command(name="givegrant")
async def grantgrant(ctx,user,grant):
    if not hasperm(ctx.author.id,"admin"): return
    id2= (await bot.get_users(user))[0][0]
    f=open("data/users/"+str(id2)+"/grants.txt","a")
    f.write(grant.strip()+"\n")

@bot.command(name="removeperm")
async def remperm(ctx,user,perm):
    id=ctx.author.id
    id2=await bot.get_users(user)
    print(id2)
    id2=id2[0][0]
    path="data/users/"+str(id2)+"/perms.txt"
    if hasgrant(id1,perm.strip()) and os.path.exists(path) and hasperm(id2,perm.strip()):
        f=open(path,"r")
        r=f.read()
        f.close()
        f=open(path,"w")
        r.remove(perm)
        f.write(r)
        f.close()

@bot.command(name="request",aliases=["req","r"])
async def req(ctx,which,which2):
    name=ctx.author.name
    perm=which.strip()=="perm"
    grant=which.strip()=="grant"
    if grant:
        f=open("data/requests/grants.txt","a+")
        f.write(name + " wants the grant: "+which2+"\n")
    if perm:
        f=open("data/requests/"+which.strip()+".txt","a+")
        f.write(name+" wants this perm\n")

@bot.command(name="readreqs",aliases=["rr","requests","reqs"])
async def readreqs(ctx,which,num):
    print(which,which.strip(),num)
    print(hasgrant(ctx.author.id,"admin"))
    if not (hasgrant(ctx.author.id,which.strip()) or hasperm(ctx.author.id,"admin")): return
    print("test2")
    f=open("data/requests/"+which.strip()+".txt")
    r=f.read()
    lst=r.split("\n")
    print("test")
    await ctx.channel.send(lst[int(num)-1])

@bot.command(name="removerequest",aliases=["rmreq","rmrq","remreq"])
async def remreq(ctx,which,num):
    if not(hasgrant(ctx.author.id,which.strip()) or hasperm(ctx.author.id,"admin")): return
    f=open("data/requests/"+which.strip()+".txt","r")
    r=f.read()
    lst=r.split("\n")
    req=lst[int(num)-1]
    lst.remove(req)
    new="\n".join(lst)
    f=open("data/requests/"+which.strip()+".txt","w")
    f.write(new)
    await ctx.channel.send("request removed ("+req+")")

@bot.command(name="requestcount",aliases=["rcount","rc"])
async def rcount(ctx,which):
    f=open("data/requests/"+which+".txt")
    r=f.read()
    lst=r.split("\n")
    await ctx.channel.send(str(len(lst)-1))

@bot.command(name="perms")
async def listperms(ctx):
    await ctx.channel.send(" ".join(open("data/users/"+str(ctx.author.id)+"/perms.txt").read().split("\n")))

@bot.command(name="grants")
async def listgrants(ctx):
    await ctx.channel.send(" ".join(open("data/users/"+str(ctx.author.id)+"/grants.txt").read().split("\n")))

@bot.command(name="queueadd")
async def qadd(ctx,name):
    if not hasperm(ctx.author.id, "editqueue"): return
    global queue
    queue.append(name)

@bot.command(name="queueremove")
async def qrem(ctx,name):
    if not hasperm(ctx.author.id,"editqueue"): return
    global queue
    queue.remove(name)

@bot.command(name="queueclear")
async def qclear(ctx):
    if not hasperm(ctx.author.id,"editqueue"): return
    global queue
    queue=[]

@bot.command(name="fortuneadd")
async def fadd(ctx,*,text):
    if not hasperm(ctx.author.id,"fortunes"): return
    f=open("data/fortunes.txt","a")
    f.write(text+"\n")

@bot.command(name="fortune")
async def fortune(ctx):
    if not isNotOnCooldown("fortune"): return
    f=open("data/fortunes.txt")
    r=f.read()
    lst=r.split("\n")
    await ctx.channel.send(choice(lst))

@bot.command(name="randomuser")
async def randusr(ctx):
    users=await bot.get_chatters("technoblade")
    all=getattr(users,"all")
    await ctx.channel.send(" ".join("@/"+choice(all)))

@bot.command(name="stab")
async def stab(ctx,name):
    if name=="me":name=ctx.author.name
    await ctx.channel.send_me("stabbed "+name)

@bot.command(name="hug")
async def hug(ctx,name):
    if name=="me":await ctx.channel.send_me(" gave "+ctx.author.name+" a warm hug.")
    else: await ctx.channel.send(ctx.author.name + " gave " + name + " a warm hug.")

@bot.command(name="help")
async def help(ctx):
    await ctx.channel.send("commands list and info: bit .ly/39SVWN6")

# will add a list of "badge perms" whic the user can remove from themselves without the grant

#@bot.command(name="removebadge")
#async def rmbdg(ctx,badge):
#    

bot.run()
