import discord
import Pixiv_Main
from discord.ext import commands

bot = commands.Bot(command_prefix='$')
client = discord.Client


@bot.event
async def on_ready():
    print(bot.user.name)
    print(bot.user.id)


@bot.command()
async def owner(ctx):
    app_info = await bot.application_info()
    await ctx.send(app_info.owner)


@bot.command()
async def s_img(ctx, img_id):
    img_info = Pixiv_Main.search(img_id, 'large')
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
async def s_user(ctx, userid: str):
    user_info = Pixiv_Main.user_info(userid)
    embed = discord.Embed(title=user_info[0], url=user_info[6])
    await ctx.send(file=discord.File('temp/user/' + str(userid) + '.png'))
    await ctx.send(embed=embed)
    await ctx.send('Works:    ' + str(user_info[2]))
    await ctx.send('Job:    ' + str(user_info[3]))
    await ctx.send('Location:   ' + str(user_info[4]))
    await ctx.send('Gender:    ' + str(user_info[5]))


@bot.command()
async  def s_userimg(ctx, userid: str):
    img_info = Pixiv_Main.user_img(userid)
    await ctx.send('该用户作品如下')
    i = 1
    while i < img_info[0]:
        embed = discord.Embed(title=img_info[i][1], description=img_info[i][0], url=img_info[i][2])
        if img_info[i][3] != 1:
            a = 0
            while a < img_info[i][3]:
                await ctx.send('原图', file=discord.File('temp/' + str(img_info[i][0]) + '_p' + str(a) + '.png'))
                a += 1
            await ctx.send(embed=embed)
        else:
            if img_info[i][4] == 'ugoira':
                await ctx.send('合成GIF时间:	' + img_info[5])
                await ctx.send('GIF', file=discord.File('temp/' + str(img_info[i][0]) + '.gif'))
                await ctx.send(embed=embed)
            else:
                p_count = 0
                await ctx.send('原图', file=discord.File('temp/' + str(img_info[i][0]) + '_p' + str(p_count) + '.png'))
                await ctx.send(embed=embed)
        i += 1


@bot.command()
async def ban(ctx, member: discord.Member):
    if str(ctx.message.author) == 'Your ID':
        await ctx.send('Command sent by' + str(ctx.message.author))
        await ctx.send('banned' + str(member.display_name))
        await discord.Member.ban(member)
    else:
        await ctx.send("You don't have enough authority")


@bot.command()
async def unban(ctx, member: discord.Member):
    if str(ctx.message.author) == 'Your ID':
        await ctx.send('Command sent by' + str(ctx.message.author))
        await ctx.send('Unbanned' + str(member.display_name))
        await discord.Member.unban(member)
    else:
        await ctx.send("You don't have enough authority")


@bot.command()
async def kick(ctx, member: discord.Member):
    if str(ctx.message.author) == 'Your ID':
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
    if str(ctx.message.author) == 'Your ID':
        await ctx.send('Clean  Success ' + 'Command sent by ' + str(ctx.message.author))
        Pixiv_Main.clean()
    else:
        await ctx.send("You don't have enough authority")


bot.run("Your Bot Token")
