#                    Copyright (c) 2021 discli.
#                
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



from rich.console import Console
from rich.progress import track
import requests
from rich.prompt import Prompt, Confirm
import os
import time
import json
import shutil
import sys

class Variables:
    BANNER = """[cyan]
            █████  ███                   ████   ███ 
            ░░███  ░░░                   ░░███  ░░░  
        ███████  ████   █████   ██████  ░███  ████ 
        ███░░███ ░░███  ███░░   ███░░███ ░███ ░░███ 
        ░███ ░███  ░███ ░░█████ ░███ ░░░  ░███  ░███ 
        ░███ ░███  ░███  ░░░░███░███  ███ ░███  ░███ 
        ░░████████ █████ ██████ ░░██████  █████ █████
        ░░░░░░░░ ░░░░░ ░░░░░░   ░░░░░░  ░░░░░ ░░░░░ """

    
    r = requests.get("https://raw.githubusercontent.com/zenqii/discli/main/version.json").json()
    VERSION = r["version"]
    UPDATE = r["update"]
    RELEASENOTE = r["release_note"]

class DiscordCLI:
    def __init__(self, folder_name = None):
        os.system("cls")
        self.console = Console()
        self.folder_name = folder_name

        if self.folder_name != None:
            os.system("mkdir {}".format(folder_name))
            os.chdir(os.getcwd() + f"\\{folder_name}")
            

        # check for update

        if Variables.UPDATE:
            self.console.print(f"New version is released please install via [red]pip install discli [/red], {Variables.VERSION}: {Variables.RELEASENOTE}")
            sys.exit()
    
        
        self.console.print(Variables.BANNER)
        self.console.print(f"\nDiscord Bot CLI v{Variables.VERSION} for creating projects")
        self.console.print("Copyright (c) 2020, [link=https://github.com/zenqii][magenta]Zenqi[/magenta][/link]. All rights reserved.")

        user_name = os.path.expanduser("~").split("\\")[2] +"'s bot"
        config = {}
        bot_token = ""


        bot_name = Prompt.ask("\n[green]»[yellow] Enter your desire bot name", default=user_name)        

        while bot_token == "":
            bot_token = Prompt.ask("[green]»[yellow] Enter your bot token [red](required)")

        prefix = Prompt.ask("[green]»[yellow] Enter bot prefix", default="!")
        is_herouku = Confirm.ask("\n[green]»[magenta] Would you like to add heroku support?")

        

        config["name"] = bot_name
        config["token"] = bot_token
        config["prefix"] = prefix
        config["heroku"] = is_herouku
        
        for _ in track(range(50), description="[green]»[cyan] Initializing discli.."):
            time.sleep(.1)

        work = True
        with self.console.status("[green]»[bold magenta] Creating ext folder...",) as status:
            while work:

                self.console.log("[green]»[cyan] Config file created: [blue]{}".format(config))
                self.create_config(os.getcwd(), config)
                self.create_main_file(os.getcwd())
                self.copy_extension(os.getcwd())
                work = False
                time.sleep(1)
                break




    def create_config(self, path, config):
        with open(path + "\\config.json", 'w') as f:
            return json.dump(config, f, indent=5)
        
        


    def copy_extension(self, path):
        abs_path = os.path.dirname(os.path.realpath(__file__))
        try:
            os.mkdir(path + "\\ext")
        except FileExistsError:
            self.console.log("[magenta]» ext folder already exist, skipping the creation of new one")
        
        copying = True

        try:
            self.console.log(f"[cyan]» Copying {abs_path}\\ext\\moderation.py to {path}\\ext")
            shutil.copy(f"{abs_path}\\_ext\\moderation.py", f"{path}\\ext")
        
        except FileNotFoundError:
            self.console.log("[red]» _ext folder is missing, skipping this")

    def create_main_file(self, path):
        
        _ = """\n\n#                    Copyright (c) 2021 <your_name>.\n#                 This project was created by Discord CLI\n# \n# Permission is hereby granted, free of charge, to any person obtaining a copy\n# of this software and associated documentation files (the "Software"), to deal\n# in the Software without restriction, including without limitation the rights\n# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n# copies of the Software, and to permit persons to whom the Software is\n# furnished to do so, subject to the following conditions:\n# The above copyright notice and this permission notice shall be included in all\n# copies or substantial portions of the Software.\n# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n# SOFTWARE.\n\n\nfrom discord.ext import commands\nimport discord\nimport json\nimport os\n\ntry:\n\n    with open("config.json", "r") as f:\n        data = json.load(f)\n\nexcept FileNotFoundError:\n    print("config.json is missing")\n\nbot = commands.Bot(command_prefix="{}".format(data["prefix"]))\n\n\ndef get_cogs(bot):\n    try:\n        print("cogs found")\n        for filename in os.listdir("./ext"):\n            if filename.endswith(".py"):\n                bot.load_extension(f"ext.%s"%(filename[:-3]))\n            else:\n                print("unable to load %s"%(filename[:-3]))\n    except FileNotFoundError:\n        print("cogs not found")\n\n@bot.event\nasync def on_ready():\n\n    print("Discord Bot template by discli")\n    print("-"*50)\n    print("Logged in as: %s" %(bot.user.name)) \n\n    serverlist = []\n    for server in bot.guilds:\n        serverlist.append(server.name)\n\n    # set the presence of the bot\n\n    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="%s servers"%(len(serverlist))))\n\nprint("-"*50)\nprint("Loading Cogs")\nget_cogs(bot)\nbot.run("{}".format(data["token"]))\n"""
        with open(path + "\\main.py", "w") as f:
            f.write(_)

        self.console.log("[green]»[cyan] main file file created")


if __name__ == "__main__":
    if sys.argv[1] == "create":
        if sys.argv[2] != None:
            DiscordCLI(sys.argv[2])
        else:
            DiscordCLI()
