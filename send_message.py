#send_message

import os
import discord
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
import grading
import translator_search
import datetime

load_dotenv()
TOKEN = 'discord_bot_token_goes_here'
GUILD = 'server_id_goes_here'

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m,q):
    if all(x in statsdb for x in stats):
        if neg == h:
            #print it into the channel
            embed = discord.Embed(title=a + " "+ j + " " + p + " Date: " + q, description=b+ " "+ c+ grade1 + " \n"+ d+ " "+ e + grade2 + " \n"+ f+ " "+ g+   grade3 +" \n"+ h+ " "+ i + "")
            embed.set_author(name= k)
            embed.set_footer(text="Mastery: " + l + " Roll Count: " + m + " Polarity: " + n + " Rank: " + o)
            await ctx.send(embed=embed)
    if neg == "1":
        if all(x in statsdb for x in stats):
            #print it into the channel
            embed = discord.Embed(title=a + " "+ j + " " + p + " Date: " + q, description=b+ " "+ c+ grade1 + " \n"+ d+ " "+ e + grade2 + " \n"+ f+ " "+ g+   grade3 +" \n"+ h+ " "+ i + "")
            embed.set_author(name= k)
            embed.set_footer(text="Mastery: " + l + " Roll Count: " + m + " Polarity: " + n + " Rank: " + o)
            await ctx.send(embed=embed)

@bot.command()
async def search(ctx, arg1, arg2, arg3, arg4, arg5):
    #lists of data I want
    weapon_list = []
    stat1_list = []
    stat2_list = []
    stat3_list = []
    stat4_list = []
    prefix_list = []
    stat1val_list = []
    stat2val_list = []
    stat3val_list = []
    stat4val_list = []
    user_list = []
    mr_list = []
    rollcount_list = []
    polarity_list = []
    rank_list = []
    price_list = []
    date = []
    arg2 = translator_search.translate(arg2)
    arg3 = translator_search.translate(arg3)
    arg4 = translator_search.translate(arg4)
    arg5 = translator_search.translate(arg5)
    #data input
    neg = arg5
    stats = [arg2, arg3, arg4]
    weapon = arg1
    #grab data from dbdb = cur.execute("")
    con = sqlite3.connect("wfm.db",isolation_level=None)
    con.execute('pragma journal_mode=wal;')
    cur = con.cursor()
    #weapon name
    db = cur.execute("SELECT weapon FROM rivens;")
    db = db.fetchall()
    for i in db:
        weapon_list += [i]
    #stat names
    db = cur.execute("SELECT stat1name FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat1_list += [i]
    db = cur.execute("SELECT stat2name FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat2_list += [i]
    db = cur.execute("SELECT stat3name FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat3_list += [i]
    db = cur.execute("SELECT stat4name FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat4_list += [i]
    #stat vals
    db = cur.execute("SELECT stat1stats FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat1val_list += [i]
    db = cur.execute("SELECT stat2stats FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat2val_list += [i]
    db = cur.execute("SELECT stat3stats FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat3val_list += [i]
    db = cur.execute("SELECT stat4stats FROM rivens;")
    db = db.fetchall()
    for i in db:
        stat4val_list += [i]
    #prefix 
    db = cur.execute("SELECT prefix FROM rivens;")
    db = db.fetchall()
    for i in db:
        prefix_list += [i]
    #usernames
    db = cur.execute("SELECT usernames FROM rivens;")
    db = db.fetchall()
    for i in db:
        user_list += [i]
    #mr
    db = cur.execute("SELECT mr FROM rivens;")
    db = db.fetchall()
    for i in db:
        mr_list += [i]
    #rerolls
    db = cur.execute("SELECT rerolls FROM rivens;")
    db = db.fetchall()
    for i in db:
        rollcount_list += [i]
    #polarity
    db = cur.execute("SELECT polarity FROM rivens;")
    db = db.fetchall()
    for i in db:
        polarity_list += [i]
    #ranks
    db = cur.execute("SELECT rank FROM rivens;")
    db = db.fetchall()
    for i in db:
        rank_list += [i]
    #prices
    db = cur.execute("SELECT price FROM rivens;")
    db = db.fetchall()
    for i in db:
        price_list += [i]   
    #dates
    db = cur.execute("SELECT date FROM rivens;")
    db = db.fetchall()
    for i in db:
        date += [i]  
    #zip through the lists for what im searching for and print it out if it matches
    for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q in zip(weapon_list, stat1_list, stat1val_list, stat2_list, stat2val_list, stat3_list, stat3val_list, stat4_list, stat4val_list, prefix_list, user_list, mr_list, rollcount_list, polarity_list, rank_list, price_list,date):
        if weapon in a:
            a = str(a).replace("(","")
            a = str(a).replace(")","")
            a = str(a).replace(",","")
            a = str(a).replace("[]","")
            a = str(a).replace("'","")
            b = str(b).replace("(","")
            b = str(b).replace(")","")
            b = str(b).replace(",","")
            b = str(b).replace("[]","")
            b = str(b).replace("'","")
            c = str(c).replace("(","")
            c = str(c).replace(")","")
            c = str(c).replace(",","")
            c = str(c).replace("[]","")
            c = str(c).replace("'","")
            d = str(d).replace("(","")
            d = str(d).replace(")","")
            d = str(d).replace(",","")
            d = str(d).replace("[]","")
            d = str(d).replace("'","")
            e = str(e).replace("(","")
            e = str(e).replace(")","")
            e = str(e).replace(",","")
            e = str(e).replace("[]","")
            e = str(e).replace("'","")
            f = str(f).replace("(","")
            f = str(f).replace(")","")
            f = str(f).replace(",","")
            f = str(f).replace("[]","")
            f = str(f).replace("'","")
            g = str(g).replace("(","")
            g = str(g).replace(")","")
            g = str(g).replace(",","")
            g = str(g).replace("[]","")
            g = str(g).replace("'","")
            h = str(h).replace("(","")
            h = str(h).replace(")","")
            h = str(h).replace(",","")
            h = str(h).replace("[]","")
            h = str(h).replace("'","")
            i = str(i).replace("(","")
            i = str(i).replace(")","")
            i = str(i).replace(",","")
            i = str(i).replace("[]","")
            i = str(i).replace("'","")
            j = str(j).replace("(","")
            j = str(j).replace(")","")
            j = str(j).replace(",","")
            j = str(j).replace("[]","")
            j = str(j).replace("'","")
            k = str(k).replace("(","")
            k = str(k).replace(")","")
            k = str(k).replace(",","")
            k = str(k).replace("[]","")
            k = str(k).replace("'","")
            l = str(l).replace("(","")
            l = str(l).replace(")","")
            l = str(l).replace(",","")
            l = str(l).replace("[]","")
            l = str(l).replace("'","")
            m = str(m).replace("(","")
            m = str(m).replace(")","")
            m = str(m).replace(",","")
            m = str(m).replace("[]","")
            m = str(m).replace("'","")
            n = str(n).replace("(","")
            n = str(n).replace(")","")
            n = str(n).replace(",","")
            n = str(n).replace("[]","")
            n = str(n).replace("'","")
            o = str(o).replace("(","")
            o = str(o).replace(")","")
            o = str(o).replace(",","")
            o = str(o).replace("[]","")
            o = str(o).replace("'","")
            p = str(p).replace("(","")
            p = str(p).replace(")","")
            p = str(p).replace(",","")
            p = str(p).replace("[]","")
            p = str(p).replace("'","")
            q = str(q).replace("(","")
            q = str(q).replace(")","")
            q = str(q).replace(",","")
            q = str(q).replace("[]","")
            q = str(q).replace("'","")
            statsdb = [b,d,f]
            grades = grading.grade_weapon(a, c, b, e, d, g, f)
            grade1 = str(grades[0])
            grade2 = str(grades[1])
            grade3 = str(grades[2])
            #await neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m)
            if arg1 == a:
                if "1" in stats:
                    if arg2 == arg3 == arg4 == "1":
                        if neg == h:
                            #print it into the channel
                            embed = discord.Embed(title=a + " "+ j + " " + p + " Date: " + q, description=b+ " "+ c+ grade1 + " \n"+ d+ " "+ e + grade2 + " \n"+ f+ " "+ g+   grade3 +" \n"+ h+ " "+ i + "")
                            embed.set_author(name= k)
                            embed.set_footer(text="Mastery: " + l + " Roll Count: " + m + " Polarity: " + n + " Rank: " + o)
                            await ctx.send(embed=embed)
                        if neg == "1":
                            #print it into the channel
                            embed = discord.Embed(title=a + " "+ j + " " + p  + " Date: " + q, description=b+ " "+ c+ grade1 + " \n"+ d+ " "+ e + grade2 + " \n"+ f+ " "+ g+   grade3 +" \n"+ h+ " "+ i + "")
                            embed.set_author(name= k)
                            embed.set_footer(text="Mastery: " + l + " Roll Count: " + m + " Polarity: " + n + " Rank: " + o)
                            await ctx.send(embed=embed)
                    if arg2 and arg3 == "1":
                        stats = [arg4]
                        await neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m,q)
                    if arg3 and arg4 == "1":
                        stats = [arg2]
                        await neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m,q)
                    if arg2 == "1":
                        stats = [arg4, arg3]
                        await neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m,q)
                    if arg3 == "1":
                        stats = [arg4, arg2]
                        await neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m,q)
                    if arg4 == "1":
                        stats = [arg2, arg3]
                        await neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m,q)
                else:
                    await neg_search(ctx,statsdb, stats, neg, h,a,j,p,b,c,grade1,d,e,grade2,f,g,grade3,i,k,l,n,o,m,q)
bot.run(TOKEN)