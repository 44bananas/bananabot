#bot_rewrote_filters

import os
import discord
from discord.ext import tasks
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import filters
import blacklist
import asyncio
import grading_data
import decimal
import grading
from datetime import date

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents = intents)

#loop to scrape
@tasks.loop(seconds=10)
async def wfm_snipe_loop():
    todays_date = date.today()
    #wfm scraper
    # select the db
    con = sqlite3.connect("wfm.db")
    cur = con.cursor()
    # get the identifier data from the table
    db = cur.execute("SELECT identifier FROM rivens;")
    db = db.fetchall()
    # create the lists
    user = []
    mr = []
    bo_price = []
    start_price = []
    prefix = []
    rank = []
    rerolls = []
    weapon = []
    positive_stat = []
    positive_value = []
    negative_stat = []
    negative_value = []
    num_positives = []
    num_negatives = []
    polarity = []
    wfm_auc = []
    # get the webpage and json
    test = requests.get('https://api.warframe.market/v1/auctions')
    data = dict(test.json())
    # selec the data from the json
    data = data['payload']['auctions']
    for i in data:
        # check if the auction is a riven
        if i['item']['type'] == 'riven':
            # grab the stats
            bo_price += [i['buyout_price']]
            start_price += [i['starting_price']]
            user += [i['owner']['ingame_name']]
            mr += [i['item']['mastery_level']]
            prefix += [i['item']['name']]
            rank += [i['item']['mod_rank']]
            rerolls += [i['item']['re_rolls']]
            weapon += [i['item']['weapon_url_name']]
            polarity += [i['item']['polarity']]
            wfm_auc += [i['id']]
            count = 0
            count2 = 0
            # grabs all stats
            for x in i['item']['attributes']:
                x = dict(x)
                # gets the stats
                if any([True for keys, values in x.items() if values == True]):
                    positive_stat += [x['url_name']]
                    count += 1
                if any([True for keys, values in x.items() if values == True]):
                    positive_value += [x['value']]
                if any([True for keys, values in x.items() if values == False]):
                    negative_value += [x['value']]
                    count2 += 1
                if any([True for keys, values in x.items() if values == False]):
                    negative_stat += [x['url_name']]
            # counting how many pos stats and neg stats
            num_positives += [count]
            num_negatives += [count2]
        # select the db
        con = sqlite3.connect("wfm.db")
        cur = con.cursor()
    # loop the data
    for a, b, c, d, e, f, g, h, j, k, l, m in zip(user, weapon, prefix, start_price, bo_price, rank, mr, rerolls, num_positives, num_negatives, polarity, wfm_auc):
        stat_1_grade = ""
        stat_2_grade = ""
        stat_3_grade = ""
        neg_stat = []
        neg_value = []
        pos_val_1 = []
        pos_val_2 = []
        pos_val_3 = []
        pos_stat_1 = []
        pos_stat_2 = []
        pos_stat_3 = []
        # getting the # of stats from the list and then removing them so they wont be reused
        positives_stat = positive_stat[0:j]
        del positive_stat[0:j]
        negatives_stat = negative_stat[0:k]
        del negative_stat[0:k]
        positives_value = positive_value[0:j]
        del positive_value[0:j]
        negatives_value = negative_value[0:k]
        del negative_value[0:k]
        # setting the stats 1/2/3/4
        try:
            pos_val_1 = str(positives_value[0])
        except:
            pos_val_1 = str([])
        try:
            pos_val_2 = str(positives_value[1])
        except:
            pos_val_2 = str([])
        try:
            pos_val_3 = str(positives_value[2])
        except:
            pos_val_3 = str([])
        pos_stat_1 = str(positives_stat[0]).replace("_", " ")
        try:
            pos_stat_2 = str(positives_stat[1]).replace("_", " ")
        except:
            pos_stat_2 = str([])
        try:
            pos_stat_3 = str(positives_stat[2]).replace("_", " ")
        except:
            pos_stat_3 = str([])
        for i in negatives_value:
            neg_value = str(i)
        for i in negatives_stat:
            neg_stat = str(i).replace("_", " ")
        # turn it all into strings
        a = str(a)
        b = str(b).replace("_", " ")
        c = str(c)
        d = str(d)
        e = str(e)
        f = str(f)
        g = str(g)
        h = str(h)
        j = str(j)
        k = str(k)
        m = str(m)
        neg_stat = str(neg_stat)
        neg_value = str(neg_value)
        pos_val_1 = str(pos_val_1)
        pos_val_2 = str(pos_val_2)
        pos_val_3 = str(pos_val_3)
        pos_stat_1 = str(pos_stat_1)
        pos_stat_2 = str(pos_stat_2)
        pos_stat_3 = str(pos_stat_3)
        grades = grading.grade_weapon(b, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3)
        grade1 = str(grades[0])
        grade2 = str(grades[1])
        grade3 = str(grades[2])
        #list for filter
        pos_stats = [pos_stat_1, pos_stat_2, pos_stat_3]
        # unquie to stop duplicates in db
        identifier = a, b, c, d, e, f, g, j, k, l, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value
        # check if the riven is in the db already
        if str(identifier) not in str(db):
            if b in grading_data.rifle_dispos or grading_data.melee_dispos or grading_data.pistol_dispos or grading_data.archgun_dispos or grading_data.shotgun_dispos:
                con.execute("INSERT OR IGNORE INTO rivens (usernames, weapon, prefix, price, rank, mr, polarity, rerolls, stat1name, stat1stats, stat2name, stat2stats, stat3name, stat3stats, stat4name, stat4stats, identifier, date) values( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (a, b, c, d, f, g, l, h, pos_stat_1, pos_val_1, pos_stat_2, pos_val_2, pos_stat_3, pos_val_3, neg_stat, neg_value, str(identifier),todays_date))
                con.commit()
                try:
                    #call filters
                    #blacklist filter
                    if a.lower() not in str(blacklist.blacklist).lower():
                        await tonkor_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here* , pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await lanka_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await paris_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await ogris_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await dread_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await paris_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await base_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await neg_mag_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await cedo_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await ogris_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await neg_cc_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await tonkor_3_mag(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        if grade1 == "S grade" and grade2 == "S grade" and grade3 == "S grade":
                            await any_role(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        if grade1 == "F grade" and grade2 == "F grade" and grade3 == "F grade":
                            await any_role(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                    #blacklsited
                    else:
                        await tonkor_3_mag(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await tonkor_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await lanka_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await paris_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await ogris_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await dread_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await paris_vintage_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await base_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await neg_mag_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await cedo_filter(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await ogris_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        await neg_cc_filters(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)   
                        if grade1 == "S grade" and grade2 == "S grade" and grade3 == "S grade":
                            await any_role(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                        if grade1 == "F grade" and grade2 == "F grade" and grade3 == "F grade":
                            await any_role(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                    if b != None:
                        await send_to_trash(a, m, g, h, d, e, l, f, b,c, pos_stats, *channel id goes here*, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3)
                except:
                    print('empty data')

#filters
async def cedo_filter(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'cedo':
        if neg_stat in filters.negative_filter:
            for x in filters.cedo_filters:
                test = all(item in pos_stats for item in x)
                if test == True:
                    pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
                    neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
                    pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
                    pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
                    #set the channel id to good rolls
                    channel = client.get_channel(id)
                    #print it into the channel
                    embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
                    embed.set_author(name= user)
                    embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
                    message = await channel.send(embed=embed)
async def base_filters(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if neg_stat in filters.negative_filter:
        #positive stat filter
        for v in filters.filters:                              
            test = all(item in pos_stats for item in v)
            if test == True:    
                pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
                pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
                pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
                neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
                pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
                pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
                pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
                #set the channel id to good rolls
                channel = client.get_channel(id)
                #print it into the channel
                embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
                embed.set_author(name= user)
                embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
                message = await channel.send(embed=embed)
async def ogris_filters(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    #ogris filters
    if weapon == 'ogris':
        if neg_stat in filters.negative_filter:
            for x in filters.ogris_filters:
                test = all(item in pos_stats for item in x)
                if test == True:
                    #set the channel id 
                    channel = client.get_channel(id)
                    #print it into the channel
                    embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
                    embed.set_author(name= user)
                    embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
                    message = await channel.send(embed=embed)
async def neg_cc_filters(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon in filters.neg_cc_weapons:
        if neg_stat in filters.neg_cc_filter_neg:
            for x in filters.neg_cc_filter_pos:
                test = all(item in pos_stats for item in x)
                if test == True:
                    pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
                    neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
                    pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
                    pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
                    #set the channel id 
                    channel = client.get_channel(id)
                    #print it into the channel
                    embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
                    embed.set_author(name= user)
                    embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
                    message = await channel.send(embed=embed)
async def neg_mag_filters(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    #neg mag weapon filter(bows,epitaph,vectis)
    if neg_stat == "magazine capacity":
        if weapon in filters.neg_mag_weapons:
            for x in filters.filters:                            
                test = all(item in pos_stats for item in x)
                if test == True:
                    pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
                    neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
                    pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
                    pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
                    pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
                    #set the channel id to good rolls
                    channel = client.get_channel(id)
                    #print it into the channel
                    embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
                    embed.set_author(name= user)
                    embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
                    message = await channel.send(embed=embed)
async def dread_vintage_filter(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'dread':
        if neg_stat == 'impact damage' or neg_stat == 'puncture damage':
            pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
            neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
            pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
            pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
            #set the channel id to good rolls
            channel = client.get_channel(id)
            #print it into the channel
            embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
            embed.set_author(name= user)
            embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
            message = await channel.send(embed=embed)
async def paris_vintage_filter(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'paris':
        if neg_stat == 'impact damage':
            pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
            neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
            pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
            pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
            #set the channel id to good rolls
            channel = client.get_channel(id)
            #print it into the channel
            embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
            embed.set_author(name= user)
            embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
            message = await channel.send(embed=embed)
async def ogris_vintage_filter(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'ogris':
        if neg_stat == 'impact damage':
            pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
            neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
            pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
            pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
            #set the channel id to good rolls
            channel = client.get_channel(id)
            #print it into the channel
            embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
            embed.set_author(name= user)
            embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
            message = await channel.send(embed=embed)
async def paris_vintage_filter(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'panthera':
        if neg_stat == 'impact damage':
            pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
            neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
            pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
            pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
            #set the channel id to good rolls
            channel = client.get_channel(id)
            #print it into the channel
            embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
            embed.set_author(name= user)
            embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
            message = await channel.send(embed=embed)
async def lanka_vintage_filter(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'lanka':
        if neg_stat == 'impact damage':
            pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
            neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
            pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
            pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
            #set the channel id to good rolls
            channel = client.get_channel(id)
            #print it into the channel
            embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
            embed.set_author(name= user)
            embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
            message = await channel.send(embed=embed)
async def tonkor_vintage_filter(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'tonkor':
        if neg_stat == 'impact damage':
            pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
            neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
            pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
            pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
            #set the channel id to good rolls
            channel = client.get_channel(id)
            #print it into the channel
            embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
            embed.set_author(name= user)
            embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
            message = await channel.send(embed=embed)
async def send_to_trash(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
    pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
    pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
    neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
    pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
    pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
    pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
    #set the channel id to trash
    channel = client.get_channel(id)
    #print it into the channel
    embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
    embed.set_author(name= user)
    embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
    message = await channel.send(embed=embed)
async def any_role(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
    pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
    pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
    neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
    pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
    pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
    pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
    #set the channel id
    channel = client.get_channel(id)
    #print it into the channel
    embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
    embed.set_author(name= user)
    embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
    message = await channel.send(embed=embed)
async def tonkor_3_mag(user, wfm_url, mr, rerolls, start_price, bo_price, polarity, rank, weapon,prefix, pos_stats, id, pos_val_1, pos_stat_1, pos_val_2, pos_stat_2, pos_val_3, pos_stat_3, neg_stat, neg_value, grade1, grade2, grade3):
    if weapon == 'tonkor':                       
        test = all(item in pos_stats for item in filters.tonkor_3)
        if test == True:
            pos_stat_1= pos_stat_1.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_2 = pos_stat_2.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_3 = pos_stat_3.replace("channeling efficiency","heavy attack efficiency")
            neg_stat = neg_stat.replace("channeling efficiency","heavy attack efficiency")
            pos_stat_1 = pos_stat_1.replace("channeling damage", "intial combo")
            pos_stat_2 = pos_stat_2.replace("channeling damage", "intial combo")
            pos_stat_3 = pos_stat_3.replace("channeling damage", "intial combo")
            #set the channel id to good rolls
            channel = client.get_channel(id)
            #print it into the channel
            embed = discord.Embed(title=weapon + " "+ prefix + " " + start_price + "-" + bo_price,url="https://warframe.market/auction/"+wfm_url, description=pos_val_1+ " "+ pos_stat_1+ grade1 + " \n"+ pos_val_2+ " "+ pos_stat_2 + grade2 + " \n"+ pos_val_3+ " "+ pos_stat_3+   grade3 +" \n"+ neg_value+ " "+ neg_stat + "")
            embed.set_author(name= user)
            embed.set_footer(text="Mastery: " + mr + " Roll Count: " + rerolls + " Polarity: " + polarity + " Rank: " + rank)
            message = await channel.send(embed=embed)


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} has connectred to Discord!'
        f'{guild.name}(id: {guild.id})'
    )
    wfm_snipe_loop.start()
client.run(TOKEN)