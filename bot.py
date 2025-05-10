# bot.py
import discord
from discord.ext import commands
import requests

bot_token = 'MTM3MDYyMTA1MTcxNzAyNTgxMw.Gc3lWS.Y-Wkrp-PXnaawq39XkPUDCzGl2nywUlWhEP6no'  # Thay bằng Bot Token chính thức

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Lệnh gửi tin nhắn vào nhiều channel bằng user token
@bot.command()
async def send(ctx, user_token: str, *channel_ids: str, *, message: str):
    """
    Lệnh: !send <user_token> <channel_id1> <channel_id2> ... <message>
    - Bot sẽ gửi tin nhắn từ user token vào các kênh chỉ định.
    - Bạn có thể truyền nhiều channel IDs.
    """
    try:
        headers = {
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }

        # Tạo payload với nội dung tin nhắn
        payload = {
            'content': message
        }

        # Gửi yêu cầu POST để gửi tin nhắn vào mỗi kênh
        for channel_id in channel_ids:
            url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                await ctx.send(f"Đã gửi tin nhắn vào kênh {channel_id}: {message}")
            else:
                await ctx.send(f"Lỗi gửi tin nhắn vào kênh {channel_id}: {response.status_code} - {response.text}")
    
    except Exception as e:
        await ctx.send(f"Lỗi: {e}")

# Khởi tạo bot
bot.run(bot_token)
