import discord
from discord.ext import tasks, commands
import datetime
from datetime import time, date, datetime
import calendar
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

description = "Helen Bot - https://github.com/0ak0/RentReminderDiscordBot"

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="h!", intents=intents, description=description)
bootDay = datetime.now()


@bot.event
async def on_ready():
    print(f"Bot Online! Logged in as {bot.user} on " + bootDay.strftime("%H:%M:%S - %A %d %B (%m) %Y"))
    with open("daysBeforeWarn") as x:
        warnDays = x.read()
        x.close
    print("\ndaysBeforeWarn has been set to " + warnDays)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="h!help"))
    await bot.add_cog(dateChecker(bot))

@bot.command(description='Days until rent')
async def days(ctx):
    today = datetime.now()
    daysInMonth = calendar.monthrange(today.year, today.month)[1]
    daysLeft = daysInMonth - today.day

    await ctx.send("Rent is due in " + str(daysLeft) + " days.")

@bot.command(description='Check the warning set or reset it')
async def warn(ctx, *args):
    if len(args) == 1:
        if int(args[0]) > 0 and int(args[0]) < 31:
            with open("daysBeforeWarn", "r+") as x:
                x.seek(0)
                x.write(args[0])
                x.truncate()
                x.close
            with open ("daysBeforeWarn") as x:
                warnDays = x.read()
            print("\ndaysBeforeWarn has been set to " + warnDays)
            await ctx.send("I will now warn you " + warnDays + " days before rent is due.")
        elif int(args[0]) == 0:
            with open("daysBeforeWarn", "r+") as x:
                x.seek(0)
                x.write("-999999")
                warnDays = x.read()
                x.close
            await ctx.send("Disabled warning.")
        else:
            with open("daysBeforeWarn") as x:
                warnDays = x.read()
                x.close
            await ctx.send("I don't understand. Warning you " + warnDays + " days before rent is due.")
    else:
        with open("daysBeforeWarn") as x:
            warnDays = x.read()
            x.close
        await ctx.send("I will warn you " + warnDays + " days before rent is due.")

@bot.command(description='View Github Link')
async def git(ctx):
     await ctx.send("Make a pr on https://github.com/0ak0/RentReminderDiscordBot")

class dateChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeCheck.start()
        print("Date Checker Cog Started!")
        

    def cog_unload(self):
        self.timeCheck.cancel()

    @tasks.loop(hours=1)
    async def timeCheck(self):
        with open("channel") as x:
            chStr = x.read()
            x.close
        # with open("channel2") as x:
        #     ch2Str = x.read()
        #     x.close
        channel = bot.get_channel(int(chStr)) # This should be set to the id of #gamer-house in The Boys
        # channel2 = bot.get_channel(int(ch2Str)) # This should be set to the id of #general in test2
        today = datetime.now()
        with open("daysBeforeWarn") as x:
            warnDays = x.read()
            x.close
        dayToWarn = calendar.monthrange(today.year, today.month)[1] - int(warnDays)
        dayToWarnInt = int(dayToWarn)
        print("\nRunning Loop")
        todayStr = str(today.day)
        todayInt = int(today.day)
        timeStr = str(today.hour) + str(today.minute)
        timeInt = int(timeStr)
        print("Today is: " + todayStr)
        print("Warn Check is set to " + str(warnDays) + " days before the 1st.")
        print("Warning on: " + str(dayToWarn))
        print("Time Check: " + timeStr)
        if timeInt > 1159 or timeInt < 1301:
            print("Time Check Passed (11:59 - 13:01)")
            if todayInt == 1:
                    print("Check Success!")
                    print("Rent Check")
                    mentionBoys = "<@1030961835588984922>"
                    await channel.send(f"# RENT DUE - TODAY IS THE FIRST OF THE MONTH! {mentionBoys}")
            elif todayInt == dayToWarnInt:
                    print("Check Success!")
                    print("Warn Check")
                    mentionBoys = "<@1030961835588984922>"
                    await channel.send(f"### RENT REMINDER - " + str(warnDays) + " DAYS LEFT {mentionBoys}")
            else:
                    print("No need to send a message.")
        else:
             print("Time Check Failed")


with open("token") as x:
    tokenStr = x.read()
    x.close
bot.run(tokenStr)