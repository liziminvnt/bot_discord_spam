import discord
from discord import app_commands
import requests

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'Bot đã đăng nhập thành: {self.user}')
        await self.tree.sync()

client = MyClient()

@client.tree.command(name="send", description="Gửi tin nhắn tới nhiều kênh bằng user token")
@app_commands.describe(
    user_token="Token của user",
    channel_ids="Danh sách channel IDs, cách nhau bởi dấu phẩy",
    message="Nội dung tin nhắn cần gửi"
)
async def send(interaction: discord.Interaction, user_token: str, channel_ids: str, message: str):
    await interaction.response.defer(thinking=True)

    ids = [cid.strip() for cid in channel_ids.split(',')]
    headers = {
        'Authorization': user_token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }

    result = ""
    for channel_id in ids:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        payload = {'content': message}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result += f'✅ Gửi thành công đến `{channel_id}`\n'
        elif response.status_code == 429:
            result += f'⚠️ Bị giới hạn gửi tại `{channel_id}`. Chờ retry.\n'
        else:
            result += f'❌ Lỗi khi gửi đến `{channel_id}`: {response.status_code}\n'

    await interaction.followup.send(result)

# Nhớ thay bằng token bot thật
client.run("MTM3MDYzNTMwMTk1Njg4MjU2Mw.GLe_PV.G1tf4U3_-x4EuyeAZGpIsKCtDnReEwHU8860qc")
