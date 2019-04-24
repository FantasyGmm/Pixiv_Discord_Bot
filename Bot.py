import discord
import Pixiv_Main
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
client = discord.Client
guild = discord.Guild


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
async def s_img(ctx, img_id):
    img_info = Pixiv_Main.search(img_id)
    embed = discord.Embed(title=img_info[1], description=img_id, url=img_info[2])
    if img_info[3] != 1:
        i = 0
        while i < img_info[3]:
            await ctx.send('原图', file=discord.File('temp/' + str(img_id) + '_p' + str(i) + '.png'))
            i += 1
        await ctx.send(embed=embed)
    else:
        if img_info[4] == 'ugoira':
            await ctx.send('合成GIF时间:	' + img_info[5])
            await ctx.send('GIF', file=discord.File('temp/' + str(img_id) + '.gif'))
            await ctx.send(embed=embed)
        else:
            p_count = 0
            await ctx.send('原图', file=discord.File('temp/' + str(img_id) + '_p' + str(p_count) + '.png'))
            await ctx.send(embed=embed)


@bot.command()
async def ban(ctx, member: discord.Member):
    if str(ctx.message.author) == 'Your Id':
        await ctx.send('Command sent by' + str(ctx.message.author))
        await ctx.send('banned' + str(member.display_name))
        await discord.Member.ban(member)
    else:
        await ctx.send("You don't have enough authority")


@bot.command()
async def unban(ctx, member: discord.Member):
    if str(ctx.message.author) == 'Your Id':
        await ctx.send('Command sent by' + str(ctx.message.author))
        await ctx.send('Unbanned' + str(member.display_name))
        await discord.Member.unban(member)
    else:
        await ctx.send("You don't have enough authority")


@bot.command()
async def kick(ctx, member: discord.Member):
    if str(ctx.message.author) == 'Your Id':
        await ctx.send('Command sent by' + str(ctx.message.author))
        await ctx.send('Kick' + str(member.display_name))
        await discord.Member.kick(member)
    else:
        await ctx.send("You don't have enough authority")


@bot.command()
async def logout(ctx):
    if str(ctx.message.author) == 'Your ID':
        await ctx.send('Logout  Success ' + 'Command sent by' + str(ctx.message.author))
        await client.logout(bot)
    else:
        await ctx.send("You don't have enough authority")


@bot.command()
async def cleanimg(ctx):
    if str(ctx.message.author) == 'Your Id':
        await ctx.send('Clean  Success ' + 'Command sent by' + str(ctx.message.author))
        Pixiv_Main.clean()
    else:
        await ctx.send("You don't have enough authority")


bot.run("your bot token")
