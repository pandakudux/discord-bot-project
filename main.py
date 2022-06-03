# main file for gusefleyhead discord bot
import discord
from discord.ext import commands
from debt_calc import calc_indv_debts

# create the bot for the code to connect to the bot
bot = commands.Bot(command_prefix='?')
TOKEN = 'OTgyMzQyNjc2ODU2ODUyNDgx.G-HNfq.ck0swfBlgYsKOrKEiZ0QE1gb-3OSS_HfuDtN8w'

# Command to calculate and display debts using embeds
# command defined using the commands extension of discord
@bot.command(name='debts')
async def post_debts(ctx, *args):

    # debug code
    print('entering debts...')

    # create nested dict of debts
    debts = calc_indv_debts()

    # functionality to display only the debts of the given person arguments
    # if no additional arguments are given, default to showing all debts
    debtList = []
    if len(args) == 0:
        debtList = debts.keys()
    else:
        for person in args:
            debtList.append(person)

    # creates and sends an embed for each person given in arguments or all of the people if no arguments are specified
    for person in debtList:
        embed = discord.Embed(title=f'{person}\'s debts', url='https://docs.google.com/spreadsheets/d/1cWEmMLPJBN803RNeucffQcJglPTY9DS54wrYPCHcHE0/edit#gid=0',description=f'The amount of money that {person} owes to each person in gusefleyhead')
        for debt in debts[person].keys():
            if not debt == 'Total':
                embed.add_field(name=f'{debt}', value=f'${debts[person][debt]}', inline=True)
        embed.add_field(name='Total', value=f'${debts[person]["Total"]}', inline=False)
        # print the embed
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def test(ctx):
    await ctx.send('bruh')
    print("TEST")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.listen()
async def on_message(message):
    if message.author == bot.user:
        return

    print(message.content)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

bot.run(TOKEN)