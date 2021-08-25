import os
import discord
import random
from dotenv import load_dotenv
from datetime import datetime
from discord.ext import commands
from selenium import webdriver
from time import sleep
import random
import bs4
import requests
import math
from discord.ext.commands import Bot
import playsound
from gtts import gTTS
import ffmpeg
from stat import S_IREAD
from stat import S_IWUSR
import string

client=Bot("")

useChrome=False
if useChrome==True:
    chromedriver_path = 'chromedriver' 
    webdriver = webdriver.Chrome(executable_path=chromedriver_path)

intents = discord.Intents.default()
intents.members=True
client = discord.Client(intents=intents)

load_dotenv("text.txt")
TOKEN = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    sys_channel=member.guild.system_channel
    if sys_channel:
        try:
            await sys_channel.send('Hey '+member.mention+' welcome to '+member.guild.name+'! To see all my functions, type "?functions"!')
        except Exception as error:
            print (error)




@client.event
async def on_message(message):

    guild = message.guild

    if "?functions" in message.content:
        response=('i am capable of:\nfunctions by typing: "?functions"random number generator by typing: "?rng"\ngetting the time for people in other time zones by typing "?current times"\ncreating polls by typing "?create poll"+a list of the options (?create poll op1,op2,op3)\nvoting in a poll by typing "?poll vote"+the number of the option you want to choose (?vote 1)\ngetting your average sleep schedule by typing "?sleep"\nsay something mean by typing "?offendn\ndeveloper only features:\nturning me on and off')
        await message.channel.send(response)

    elif "?rng" in message.content:
        message.content=message.content.replace("?rng","")
        if len(message.content)==0 or message.content[0]==" " and len(message.content)<2:
             response="ERROR: please add perimeters for the random number"
             await message.channel.send(response)

        else:
            try:
                message.content=message.content[1:len(message.content)]
                paramOne=message.content.split(",")[0]
                paramTwo = message.content.split(",")[-1]
                print(paramOne,paramTwo)


                paramOne=int(paramOne)
                paramTwo=int(paramTwo)
                rng=random.randint(paramOne,paramTwo)
            except:
                rng='ERROR: incorrect formatting. example: "bot rng 25,75"'
            await message.channel.send(rng)

    elif "?current times" in message.content:
        now = datetime.now()
        minute=now.strftime("%M")
        england=now.strftime("%H")
        england=int(england)
        a=england+9
        if a>23:
            a=a-24
        israel=england+2
        if israel>23:
            israel=israel-24
        GandN=england+1
        if GandN==24:
            GandN=0
        c=england-5
        if c<0:
            c=c+24
        england=str(england)
        israel=str(israel)
        GandN=str(GandN)
        c=str(c)
        a=str(a)
        response=str("Englands time is "+ england+":"+minute+"\nNetherlands and Germanys time is "+GandN+":"+minute+"\nIsrael and Russias time is "+israel+":"+minute+"\nCanadas time is "+c+":"+minute+"\nAustralias time is "+a+":"+minute)

        response=response.replace("'","")
        await message.channel.send(response)
        


    elif "?create poll" in message.content:
        currentPole= open("poll files/current_pole.txt","r")
        torf=currentPole.read()
        currentPole.close()
        if torf== "True":
            await message.channel.send("there is already an active poll!")
        elif torf == "False":
            currentPole= open("poll files/current_pole.txt","w+")
            currentPole.write("True")
            currentPole.close()
            pollList=[]
            message.content=message.content.replace("bot create poll ","")
            count=0
            lastCount=0
            loop=bool(True)
            while loop == True:
                if count==len(message.content):
                    pollList.append(message.content[lastCount:count])
                    break
                else:
                    if message.content[count]==",":
                        pollList.append(message.content[lastCount:count])
                        lastCount=count
                        count=count+2
                    else:
                        count=count+1
            count=0
            pollList[0]=","+pollList[0]
            loop=bool(True)
            while loop==True:
                if count<len(pollList):
                    num=str(count+1)
                    add2list=pollList[count].replace(",","")
                    file=open ("poll files/poll.txt","a")
                    file.write(add2list)
                    file.write("\n")
                    file.close()
                    
                    pollList[count]=pollList[count].replace(",","type "+num+" for ")
                    await message.channel.send(pollList[count])
                    count=count+1
                else:
                    break


                
    elif "?poll vote" in message.content:
        currentPole= open("poll files/current_pole.txt","r")
        torf=currentPole.read()
        currentPole.close()

        if torf == "False":
            await message.channel.send("there is no poll currently open!")
        elif torf == "True":
            
            alreadyVoted=open("poll files/already voted.txt")
            voter=alreadyVoted.read().splitlines()
            alreadyVoted.close()
            
            message.author=str(message.author)
            author=message.author.split("#")[0]
            if author in voter:
                await message.channel.send(f'{author} has already voted!')
            else:
            
                message.content=message.content.replace("bot poll vote ","")
                message.content= int(message.content)

                options=open("poll files/poll.txt","r")
                get=options.read().splitlines()
                options.close()
                
                if message.content>len(get)+1:
                    await message.channel.send(f'ERROR: not a valid vote. There isnt this many options!')
                elif message.content<1:
                    await message.channel.send(f'ERROR: not a valid vote. Please choose a number greater than 0!')
                else:
                    await message.channel.send(f'{author} voted for {get[message.content-1]}!')
                    file=open("poll files/already voted.txt","a")
                    file.write(author)
                    file.write("\n")
                    file.close()

                    file=open("poll files/votes.txt","a")
                    file.write(str(message.content))
                    file.write("\n")
                    file.close()


    elif "bot close poll" in message.content:
        file=open("poll files/current_pole.txt","r")
        openPole=file.read()
        file.close()
        
        if openPole == "False":
            await message.channel.send("ERROR: there is no poll currently open!")
        else:

            collect=open("poll files/votes.txt")
            vote=collect.read().splitlines()
            collect.close()

            if len(vote)==0:
                await message.channel.send("No votes yet, nothing has won")
                
            else:
                options=open("poll files/poll.txt","r")
                choice=options.read().splitlines()
                length=len(choice)
                options.close()

                def most_frequent(vote):
                    return max(set(vote), key = vote.count)

                winner=int(most_frequent(vote))
                howmany=0

                num=0
                loop=bool(True)
                while loop == True:
                    if num==len(vote):
                        break
                    else:
                        if vote[num]==winner:
                            print("fuck")
                            howmany=howmany+1
                        num=num+1
                            
            
                await message.channel.send(f'{choice[winner-1]} won the poll with {howmany} votes!')

            file=open("poll files/current_pole.txt","w")
            file.write("False")
            file.close()

            file=open("poll files/poll.txt","w")
            file.write("")
            file.close()

            file=open("poll files/already voted.txt","w")
            file.write("")
            file.close()

            file=open("poll files/votes.txt","w")
            file.write("")
            file.close()

    elif "bot offend" in message.content:
        file= open("offend.txt","r")
        mean=file.read().splitlines()
        offend=random.choice(mean)
        await message.channel.send(offend)


        

    elif "bot sleep" in message.content:
        message.author=str(message.author)
        author=message.author.split("#")[0]
        now = datetime.now()
        minute=now.strftime("%M")
        hour=now.strftime("%H")

        file=open("sleep list/"+author,"a+")
        file.write(hour+":"+minute)
        file.write("\n")
        file.close()

        file=open("sleep list/"+author,"r")
        schedule=file.read().splitlines()
        file.close()
        count=0
        hour=0
        minute=0
        loop=bool(True)
        while loop == True:
            if count==len(schedule):
                break
            else:
                current=schedule[count]
                currentH=current.split(":")[0]
                currentM=current.split(":")[-1]
                
                currentH=int(currentH)
                currentM=int(currentM)
                
                hour=hour+currentH
                minute=minute+currentM
                count=count+1
        
        minute=minute+(hour*60)
        divide=minute/len(schedule)
        averageH=math.floor(divide/60)
        averageM=math.floor(divide%60)
        

        await message.channel.send(f'Good night {author}!\nyour average time to go to bed is {averageH}:{averageM}')




    if not guild:
        if message.author.name==USER:
            return

        

client.run(TOKEN)
