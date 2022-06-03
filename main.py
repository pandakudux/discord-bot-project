# main file for gusefleyhead discord bot
from email.errors import FirstHeaderLineIsContinuationDefect
from pydoc import describe
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

    # creates and sends an embed for each person given in arguments or all of the people in the spreadsheet if no arguments are specified
    for person in debtList:
        # declaration of fields for the embed object
        title = f'{person}\'s debts'
        link = 'https://docs.google.com/spreadsheets/d/1cWEmMLPJBN803RNeucffQcJglPTY9DS54wrYPCHcHE0/edit#gid=0'
        # modifies the color of the embed and the description based on if a debt exists or not
        total = debts[person]["Total"]
        if total == 0:
            color = discord.Colour.green()
            desc = f'Congrats! {person} is free of debts, for now...'
        else:
            color = discord.Colour.red()
            desc = f'The amount of money {person} owes to people in gusefleyhead'

        # creates the embed object with the fields created above and adds fields for each debt person owes
        embed = discord.Embed(title=title, url=link, description=desc, color=color)
        for debt in debts[person].keys():
            if not debt == 'Total':
                embed.add_field(name=f'{debt}', value=f'${debts[person][debt]}', inline=True)
        # adds total value at the bottom of the embed which is seperated by a blank line
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name='Total', value=f'${total}', inline=False)
        if not total == 0:
            embed.set_footer(text='Don\'t forget to mark debts as payed in the spreadsheet!')
        # prints the embed to the given channel
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