from discord.ext import commands
import pyjokes
import discord
import random
import asyncio

emoji_list = [letter for letter in "😀😁😂🤣😃😄😅😆😗🥰😘😍😎😋😊😉😙☺😚🙂🤗🤩🤔🤨😮😣😥😏🙄😶😑😐🤐😯😪😫🥱😴😌😛🙃😕😔😓😒🤤😝😜🤑😲☹🙁😖😞😟😤😬🤯😩😨😧😦😭😢😰😱🥵🥶😳🤪😵🥴🤮🤢🤕🤒😷😡🤬😠❤🧡💛💚💙💜🤎🖤💖💗💓💞💕❣💔🤍💘💝💟💌💢💥💤💦💨💫🕳🚛🚜🚲🦼🚕🚗🚑🦼🚜🚙🛹⛰🧭🗺🌏🏗🏘🌆🌅🌄🌃🌁⛺💈🛎🧳🌩🌦☁🌀🌬🌡🌚🌔🌖🌟🌞☀🌜🌛🌙⛄☃❄⚡⛱🔥💧🌊☔🌠☄🌡🌬👨‍👩‍👦‍👦👩‍❤️‍👩👨‍❤️‍👨💑🦿🦾🧠⛷🦴👀👁👥👤👩🏽‍🤝‍🧑🏿🎏🎎🎍🎗🎭🎁🎪🎨🧶🎑🎊👡👠🖊🖋📂📁✏🗒📤✒📦🖊📬🖌📆📍📋✂📐📇🖇⌚⏱🥠🥙🍚🍗🧇🥙🌮🍱🍤🍶🥂🥄🍺🍴🍽🧃🍨🍵🍶🍯🍾🍻🥃🍍🌿🌴🍃🌳🍁🍂🌲"]

def generate_emoji():
  return random.choice(emoji_list)

class Board():
      def init_board(self):
          self.board = """
   | |         
   | | 
   | | 
  
                  """
          self.filled = list()
         
      def print_board(self):
          def r():
            return random.randint(0,255)
          def generate_embed(desc):
            return discord.Embed(description=desc, color=discord.Color.from_rgb(r(), r(), r()))
          slots = list()
          for i in range(1,10):
            slots.append(self.get_slot(str(i)))
          string = f'''{slots[0]}|{slots[1]}|{slots[2]}\n{slots[3]}|{slots[4]}|{slots[5]}\n{slots[6]}|{slots[7]}|{slots[8]}'''
          final_string = ''
          for i in string:
            if i == 'X' or i == 'O':
              final_string += '**'+i+'**'
            else:
              final_string += i
  

          return generate_embed(final_string)
      def input_(self,player,coords,bold=False):
          board_coords = {'1': '1',
           '2': '3',
           '3': '5',
           '4': '15',
           '5': '17',
           '6': '19',
           '7': '21',
           '8': '23',
           '9': '25'}
          temp = list(self.board)
          if bold:
            temp[int(board_coords[str(coords)])] = '**' + player.upper() + '**'
          else:
            temp[int(board_coords[str(coords)])] = player.upper()

          self.board = ''.join(temp)
          self.filled.append(int(coords))
      def get_slot(self,number):
        board_coords = {'1': '1',
           '2': '3',
           '3': '5',
           '4': '15',
           '5': '17',
           '6': '19',
           '7': '21',
           '8': '23',
           '9': '25'}
        return self.board[int(board_coords[number])]
    
      def check_game(self):
          rows = [[self.board[1], self.board[3], self.board[5]], [self.board[15], self.board[17], self.board[19]],
                  [self.board[21], self.board[23], self.board[25]]]
          columns = [[self.board[1], self.board[15], self.board[21]], [self.board[3], self.board[17], self.board[23]],
                     [self.board[5], self.board[19], self.board[25]]]
          horizontal_columns = [[self.board[1], self.board[17], self.board[25]],
                                [self.board[5], self.board[17], self.board[21]]]
          for i in rows:
              if all(v == "X" for v in i):
                  return 'X'
              if all(v == "O" for v in i):
                  return 'O'
          for i in columns:
              if all(v == "X" for v in i):
                  return 'X'
              if all(v == "O" for v in i):
                  return 'O'
  
          for i in horizontal_columns:
              if all(v == "X" for v in i):
                  return 'X'
              if all(v == "O" for v in i):
                  return 'O'
  
          if len(self.board.filled) == 9:
              return 'Draw'
  
def run_game():
  pass

def ball_gen(question):
    responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.", "My sources say no.",
                "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.",
                "Yes.", "Yes – definitely.", "You may rely on it."]
    return f"Question: {question}\nAnswer: {random.choice(responses)}"

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.board = Board()
        self.board.init_board()
    
        self.db = {}
        self.db['turn'] = 0
        self.db['started'] = False

    @commands.command()
    async def emoji(self, ctx):
        """Give a random emoji"""
        await ctx.message.channel.send(generate_emoji())

    @commands.command()
    async def joke(self, ctx):
        """A random nerdy joke"""
        joke = pyjokes.get_joke(language='en', category= 'neutral')
        await ctx.reply(f"{joke}")
        
    @commands.command()
    async def rps(self, ctx):
        """Play a Rock Paper Scissors game with the bot"""
        
        await ctx.message.add_reaction("🟢")
  
        msg = await ctx.send("Choose :rock: for Rock, :roll_of_paper: for Paper, and :scissors: for Scissors")
  
        for emoji in ['🪨',"🧻", "✂️"]:
            await msg.add_reaction(emoji)
      
        check = lambda r, u: u == ctx.author and str(r.emoji) in "🪨✂️🧻" and r.message.id == msg.id # r=reaction, u=user, m=message
  
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await msg.edit(content="Game cancelled.")
            return

        win_response = ["You win this time!", "I will get you next time!", "Gosh darn it!", 'Thank you for winning...', "Do you like the trophy?"]
        lose_response = ["Hah, good luck next time!", "I am the best!", "Tough luck!", "Try and try again... to fail.", "The champion is me!"]
        draw_response = ["Keep in mind that I will win", "Another round?", "Let's go another round!"]

        def win():
            return f"You picked {str(reaction.emoji)} and I picked {comp_choice}. {random.choice(win_response)}"
        def lose():
            return f"You picked {str(reaction.emoji)} and I picked {comp_choice}. {random.choice(lose_response)}"
        def draw():
            return f"You and I picked {comp_choice}. {random.choice(draw_response)}"
  
        comp_choice = random.choice(["🪨","🧻","✂️"])
        if str(reaction.emoji) == comp_choice:
            await msg.edit(content=draw())
        elif str(reaction.emoji) == "🪨":
            if comp_choice == "✂️":
                await msg.edit(content=win())
                await ctx.message.add_reaction("👑")
                await msg.add_reaction("🥉")
            elif comp_choice == "🧻":
                await msg.edit(content=lose())
                await msg.add_reaction("👑")
                await ctx.message.add_reaction("🥉")
        elif str(reaction.emoji) == "🧻":
            if comp_choice == "🪨":
                await msg.edit(content=win())
                await ctx.message.add_reaction("👑")
                await msg.add_reaction("🥉")
            elif comp_choice == "✂️":
                await msg.edit(content=lose())
                await msg.add_reaction("👑")
                await ctx.message.add_reaction("🥉")
        elif str(reaction.emoji) == "✂️":
            if comp_choice == "🧻":
                await msg.edit(content=win())
                await ctx.message.add_reaction("👑")
                await msg.add_reaction("🥉")
            elif comp_choice == "🪨":
                await msg.edit(content=lose())
                await msg.add_reaction("👑")
                await ctx.message.add_reaction("🥉")
        else:
            await msg.edit(content="Game cancelled!")
        for emoji in ['🪨',"🧻", "✂️"]:
            await msg.clear_reaction(emoji)
        await ctx.message.clear_reaction("🟢")
        
    @commands.command()
    async def tttoe(self, ctx, p2=None):
        """Tic Tac Toe with a friend!"""
        p2 = p2 or ctx.message.author.mention
        if self.db['started'] == True:
            await ctx.send(f' A game is ongoing between {self.db["p1"]} and {self.db["p2"]}')  
        else:
            self.db['started'] = True
            self.db['p1'] = '<@!' + str(ctx.message.author.id) + '>'
            self.db['p2'] = str(p2)
            slots = list()
            for i in range(1, 10):
                slots.append(self.board.get_slot(str(i)))
            slots[0] = self.board.input_(str(1),str(1))
            slots[1] = self.board.input_(str(2),str(2))
            slots[2] = self.board.input_(str(3),str(3))
            slots[3] = self.board.input_(str(4),str(4))
            slots[4] = self.board.input_(str(5),str(5))
            slots[5] = self.board.input_(str(6),str(6))
            slots[6] = self.board.input_(str(7),str(7))
            slots[7] = self.board.input_(str(8),str(8))
            slots[8] = self.board.input_(str(9),str(9))
            self.board.filled = list()
            self.db['cp'] = "X"
            await ctx.send(f'{self.db["p1"]} is X. ')
            await ctx.send(f'{self.db["p2"]} is O. ')
            await ctx.send('''```1|2|3\n4|5|6\n7|8|9```''')
            await ctx.send('''```Use .i choice to input your choice.\nUse .kill_game to kill the game.```''')
            await ctx.send(f"Its player X's turn. Enter a number: ")
            
    @commands.command(hidden=True)
    async def i(self, ctx, choice):
        if self.db['cp'] == 'X':
            if str(ctx.message.author.id) in self.db['p1']:  
                if self.db['started']:      
                    if int(choice) in self.board.filled:
                        await ctx.send('Please select an empty slot. ')
                    else:
                        turn = self.db['turn']
                        if turn % 2 == 0:
                            player = 'x'
                        else:
                            player = 'o'
                        self.db['cp'] = player.upper()
                        self.db['turn'] += 1
                        self.board.input_(player,int(choice))
                        await ctx.send(embed=self.board.print_board())
      
                        if self.board.check_game() == None:
                            pass
                        
                        elif self.board.check_game() == 'O':
                            await ctx.send('Player O is the winner! ')
                            self.db['started'] = False
                            self.board.init_board()
                            self.board.filled = []
                            self.db['turn'] = 0
                            self.db['cp'] = 'X'
                
                        elif self.board.check_game() == 'X':
                            await ctx.send('Player X is the winner! ')
                            self.db['started'] = False
                            self.board.filled = []
                            self.board.init_board()
                            self.db['turn'] = 0
                            self.db['cp'] = 'X'
                
                        elif self.board.check_game() == 'Draw':
                            await ctx.send('The game is a draw!')
                            self.db['started'] = False
                            self.board.init_board()
                            self.board.filled = []
                            self.db['turn'] = 0
                            self.db['cp'] = 'X'
                
                        if self.db['started']:
                            turn = self.db['turn']
                            if turn % 2 == 0:
                                player = 'x'
                            else:
                                player = 'o'
                            self.db['cp'] = player.upper()
                
                            await ctx.send(f"Its player {player.upper()}'s turn. Enter a number: ")
                else:
                    await ctx.send('No games have been started yet. ')
            else:
                await ctx.send("It's not your turn / you aren't in the game")
        else:
            if str(ctx.message.author.id) in self.db['p2']:
                if self.db['started']:      
   
                    if int(choice) in self.board.filled:
                        await ctx.send('Please select an empty slot. ')
                    else:
                        turn = self.db['turn']
                        if turn % 2 == 0:
                            player = 'x'
                        else:
                            player = 'o'
                        self.db['cp'] = player.upper()
                        self.db['turn'] += 1
                        self.board.input_(player,int(choice))
                        await ctx.send(embed=self.board.print_board())
        
                        if self.board.check_game() == None:
                            pass
                        elif self.board.check_game() == 'O':
                            await ctx.send('Player O is the winner! ')
                            self.db['started'] = False
                            self.board.init_board()
                            self.board.filled = []
                            self.db['turn'] = 0
                  
                        elif self.board.check_game() == 'X':
                            await ctx.send('Player X is the winner! ')
                            self.db['started'] = False
                            self.board.filled = []
                            self.board.init_board()
                            self.db['turn'] = 0
                        elif self.board.check_game() == 'Draw':
                            await ctx.send('The game is a draw!')
                            self.db['started'] = False
                            self.board.init_board()
                            self.board.filled = []
                            self.self.db['turn'] = 0
        
                        if self.db['started']:
                            turn = self.db['turn']
                        if turn % 2 == 0:
                            player = 'x'
                        else:
                            player = 'o'
                        self.db['cp'] = player.upper()
                  
                        await ctx.send(f"Its player {player.upper()}'s turn. Enter a number: ")
                else:
                        await ctx.send('No games have been started yet. ')
            else:
                await ctx.send("It's not your turn / you aren't in the game")
                
    @commands.command(hidden=True)
    async def kill_game(self, ctx):
        await ctx.send('Killed the game. ')
        self.db['started'] = False
        self.board.init_board()
        self.board.filled = []
        self.db['turn'] = 0
        self.db['cp'] = 'X'
        
    @commands.command(aliases=['8ball','eightball'])
    async def _8ball(self, ctx,*,question):
        await ctx.send(ball_gen(question))

        
def setup(bot):
    bot.add_cog(Fun(bot))