import discord
from discord import app_commands
import requests

class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f"Bot đã đăng nhập: {self.user}")

client = MyClient()

@client.tree.command(name="send", description="Gửi tin nhắn đến các channel bằng user token")
@app_commands.describe(
    token="User token",
    channels="Danh sách ID channel cách nhau bởi khoảng trắng",
    content="Nội dung tin nhắn cần gửi"
)
async def send(interaction: discord.Interaction, token: str, channels: str, content: str):
    await interaction.response.defer()
    
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    channel_ids = channels.split()
    for cid in channel_ids:
        url = f"https://discord.com/api/v9/channels/{cid}/messages"
        payload = {"content": content}
        r = requests.post(url, headers=headers, json=payload)

        if r.status_code == 200:
            await interaction.followup.send(f"✅ Gửi thành công tới `{cid}`")
        elif r.status_code == 429:
            retry_after = r.json().get("retry_after", 5)
            await interaction.followup.send(f"⏳ Rate limit! Đợi {retry_after} giây cho kênh `{cid}`")
        else:
            await interaction.followup.send(f"❌ Lỗi gửi `{cid}`: {r.status_code} - {r.text}")

client.run("YOUR_BOT_TOKEN_HERE")
