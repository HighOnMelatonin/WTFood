import discord
import random
import json

client = discord.Client()

raw = open('food.json', 'r+')
food = json.load(raw)
raw.close()

raw = open('dessert.json', 'r+')
after = json.load(raw)
##Dessert comes after a meal, sooo "after"
raw.close()

##Dessert


@client.event
async def on_ready():
    guilds = []
    for guild in client.guilds:
        guilds.append(guild)

    print(f"{client.user} is connected to the following guild(s): ")
    for guild in guilds:
        print(f'{guild.name:<25} {str(guild.id):^35}')



def sendhelp():
    help_title = "How I work:"

    helpmessage = f'''Having trouble deciding what to eat?
    Type 'FindFood' and I will suggest a cuisine for you

    > FindFood
    > How does Japanese Food sound?

    If you're satisfied with my suggestion, type 'FindDish' and I will recommend a dish from that cuisine

    > FindFood
    > How does Japanese Food sound?
    > FindDish
    > Can I interest you in Ramen

    You can always resend 'FindFood' or 'FindDish' if my suggestion is not something you like

    If you would like to suggest cuisines that I do not know about, type 'SuggestFood'

    > SuggestFood Italian
    > Italian sounds interesting

    To suggest dishes for the different cuisines, type 'SuggestDish'

    > SuggestDish Aglio Olio; Italian
    > Aglio Olio sounds nice, I should try it some time


    Fancy dessert?
    Type 'FindDessert'

    > FindFood
    > How does Japanese food sound?
    > FindDessert
    > Have you tried Taiyaki?

    Have dessert to recommend? Type 'SuggestDessert'

    > SuggestDessert Gelato; Italian
    > Gelato 
    '''

    return help_title, helpmessage


def findfood(lastcuisine):
    cuisines = list(food.keys())
    templast = lastcuisine

    cuisines.sort()
    templast.sort()
    
    if cuisines == templast:
        return False

    else:
        cuisine = random.choice(cuisines)

        while cuisine in lastcuisine:
            cuisine = random.choice(cuisines)
        
        return cuisine


def finddish(cuisine, lastdish):
    dishes = food[cuisine]
    templast = lastdish

    dishes.sort()
    templast.sort()
    
    if templast == dishes:
        return False

    else:
        dish = random.choice(dishes)
        
        while (dish in lastdish):
            dish = random.choice(dishes)
        
        return dish


def finddessert(cuisine, lastdessert):
    desserts = after[cuisine]
    templast = lastdessert

    desserts.sort()
    templast.sort()

    if templast == desserts:
        return False

    else:
        dessert = random.choice(desserts)

        while (dessert in lastdessert):
            dessert = random.choice(desserts)


def givefood(cuisine):
    cuisines = list(food.keys())

    if not cuisine in cuisines:
        d = {cuisine: []}
        food.update(d)

        raw = open('food.json', 'r+')
        json.dump(food, raw, indent = 4)
        raw.close()

        after.update(d)
        raw = open('dessert.json', 'r+')
        json.dump(after, raw, indent = 4)
        raw.close()
        return True

    else:
        return False


def givedish(cuisine, dish):
    cuisines = list(food.keys())
    
    if not cuisine in cuisines:
        givefood(cuisine)

    dishes = food[cuisine]
    if not dish in dishes:
        food[cuisine].append(dish)

        raw = open('food.json', 'r+')
        json.dump(food, raw, indent = 4)
        raw.close()
        return True

    else:
        return False


def givedessert(cuisine, dessert):
    cuisines = list(food.keys())

    if not cuisine in cuisines:
        givefood(cuisine)

    desserts = after[cuisine]
    if not dessert in desserts:
        after[cuisine].append(dessert)

        raw = open('dessert.json', 'r+')
        json.dump(after, raw, indent = 4)
        raw.close()
        return True

    else:
        return False


def reset():
    lastcuisine = []
    lastdish = []
    lastdessert = []
    return lastcuisine, lastdish, lastdessert


def reply(choice):
    ##Choice should be 0, 1, 2, 3, 4 or 5; corresponding to the lists below
    newfood = ['{0} food sounds interesting',\
        '{0} food sounds nice, I should try it some time',\
            'Ok, maybe I\'ll try {0} food next time']

    known = ["I think I've heard of {0} food before",\
        "I think someone told me about {0} food before",\
            "Ahh yes, I've had {0} food before"]

    recc = ["Can I interest you in {0} food?",
            "Would you like to have {0} food?",
            "How does {0} food sound?",
            "Have you had {0}?"]

    noclue = ["I've run out of ideas, sorryy",
    "I can't think of anything else, sorryy"]

    noexist = ["I don't think {0} exists"]

    newdish = ['{0} sounds interesting',\
        '{0} sounds nice, I should try it some time',\
            'Ok, maybe I\'ll try {0} next time']

    responses = [newfood, known, recc, noclue, noexist, newdish]
    options = responses[choice]

    return random.choice(options)


lastcuisine, lastdish, lastdessert = reset()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if (message.content == 'WTFhelp') or (message.content == 'WTFHelp') or (message.content.startswith('<@!935529175811510312>')):
        help_title, helpmessage = sendhelp()
        await message.channel.send(embed = discord.Embed(title = help_title, description = helpmessage))
        return

    if 'FindFood' in message.content:
        cuisine = findfood(lastcuisine)

        if cuisine:
            lastcuisine.append(cuisine)
            response = reply(2)
            remessage = response.format(cuisine)

        else:
            remessage = reply(3)

    if 'FindDish' in message.content:
        dish = finddish(lastcuisine[-1], lastdish)

        if dish:
            lastdish.append(dish)
            response = reply(2)
            remessage = response.format(dish)

        else:
            remessage = reply(3)
        
        await message.channel.send(remessage)
        return

    if 'FindDessert' in message.content:
        dessert = finddessert(lastcuisine[-1], lastdessert)

        if dessert:
            lastdessert.append(dessert)
            response = reply(2)
            remessage = response.format(dessert)

        else:
            remessage = reply(3)

    if 'SuggestFood' in message.content:
        cuisine = message.content[12:]

        allalph = True
        for char in cuisine:
            if char.isdigit():
                allalph = False
                break
        
        if not allalph:
            remessage = reply(4)
        
        else:
            if givefood(cuisine):
                givefood(cuisine)

                if 'food' in cuisine or 'Food' in cuisine:
                    cuisine = cuisine[:-5]
                    response = reply(0)
                    remessage = response.format(cuisine)

                else:
                    response = reply(0)
                    remessage = response.format(cuisine)

            else:
                response = reply(1)
                remessage = response.format(cuisine)

    if 'SuggestDish' in message.content:
        semicol = message.content.index(';')
        dish = message.content[12:semicol]
        cuisine = message.content[semicol + 2:]

        allalph = True
        for char in cuisine:
            if char.isdigit():
                allalph = False
                break
        
        if not allalph:
            remessage = reply(4)

        else:
            if givedish(cuisine, dish):
                givedish(cuisine, dish)
                response = reply(5)
                remessage = response.format(dish)

            else:
                response = reply(1)
                remessage = response.format(dish)

    if 'SuggestDessert' in message.content:
        semicol = message.content.index(';')
        dessert = message.content[15:semicol]
        cuisine = message.content[semicol + 2:]

        allalph = True
        for char in cuisine:
            if char.isdigit():
                allalph = False
                break

        if not allalph:
            remessage = reply(4)

        else:
            if givedessert(cuisine, dessert):
                givedessert(cuisine, dessert)
                response = reply(5)
                remessage = response.format(dessert)

            else:
                response = reply(1)
                remessage = response.format(dessert)

    await message.channel.send(remessage)
    return



client.run(token)

##Clear input history


