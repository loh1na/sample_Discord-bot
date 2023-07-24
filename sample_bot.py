import math

import discord, aiosqlite, asyncio
from discord.ext import commands

class Main(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        #if desired you can uncomment this line in order to display activity status on your discord bot page
        #await bot.change_presence(activity=discord.Game(name="MGE server on Team Fortress 2"))

    async def setup_hook(self):
        #await self.wait_until_ready()
        global bot_db
        bot_db = await aiosqlite.connect("levels.db")
        await bot_db.execute("CREATE TABLE IF NOT EXISTS levels (guild_id INTEGER, usr_id INTEGER, exp INTEGER, PRIMARY KEY (guild_id, usr_id))")
        self.commands()

    async def on_message(self, message):
        global lvl
        if not message.author.bot:
            cursor = await bot_db.execute("INSERT OR IGNORE INTO levels (guild_id, usr_id, exp) VALUES (?, ?, ?)",
                                          (message.guild.id, message.author.id, 1))

            if cursor.rowcount == 0:
                await bot_db.execute("UPDATE levels SET exp = exp + 1 WHERE guild_id = ? AND usr_id = ?",
                                     (message.guild.id, message.author.id))
                curs = await bot_db.execute("SELECT exp FROM levels WHERE guild_id = ? AND usr_id = ?",
                                            (message.guild.id, message.author.id))
                data = await curs.fetchone()
                exp = data[0]
                lvl = math.sqrt(exp) / 2
                #print(lvl)

                if lvl.is_integer():
                    await message.channel.send(f"Good job <@{message.author.id}>! You are now have level {int(lvl)}")

        await bot_db.commit()
        print(f'Message from {message.author}: {message.content}')
        await self.process_commands(message)

    def commands(self):
        @self.command(name='test')
        async def test(ctx):
            await ctx.send("ebi kashtan 16 na 9")

        @self.command(name='stat')
        async def stat(ctx):
            progress = (lvl - int(lvl)) / 1 * 100
            await ctx.send(f"current lvl of user <@{ctx.author.id}> is {int(lvl)} progress to the next level is: {int(progress)}%")
            #print (progress)

        @self.command(name='leaderboard')
        async def leaderboard(ctx):
            i = 0
            print(ctx.guild.id)
            userdb = await bot_db.execute("SELECT * FROM levels WHERE guild_id = ? ORDER BY exp DESC"
                                          , (ctx.guild.id, ))
            for users in await userdb.fetchall():
                i += 1
                print(users[2])
                await ctx.send(f"{i} place:<@{users[1]}> with level {int(math.sqrt(users[2]) / 2)}")










bot = Main()
bot.run('YOUR_TOKEN_HERE')












