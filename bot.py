import discord
from discord.ext import commands
import aiohttp  # Thay requests bằng aiohttp

# Token của bot
bot_token = 'MTM3MDYyMTA1MTcxNzAyNTgxMw.Gc3lWS.Y-Wkrp-PXnaawq39XkPUDCzGl2nywUlWhEP6no'  # Thay bằng token bot thực tế của bạn

# Cấu hình intents cho bot
intents = discord.Intents.default()
intents.message_content = True  # Đảm bảo bot có quyền đọc nội dung tin nhắn

# Khởi tạo bot với intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Lệnh gửi tin nhắn vào nhiều channel bằng user token
@bot.command()
async def send(ctx, user_token: str, message: str, *channel_ids: str):
    """
    Lệnh: !send <user_token> <message> <channel_id1> <channel_id2> ...
    - Bot sẽ gửi tin nhắn từ user token vào các kênh chỉ định.
    - Bạn có thể truyền nhiều channel IDs sau message.
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

        # Sử dụng aiohttp để gửi yêu cầu HTTP bất đồng bộ
        async with aiohttp.ClientSession() as session:
            for channel_id in channel_ids:
                url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        await ctx.send(f"Đã gửi tin nhắn vào kênh {channel_id}: {message}")
                    else:
                        await ctx.send(f"Lỗi gửi tin nhắn vào kênh {channel_id}: {response.status} - {await response.text()}")
    
    except Exception as e:
        await ctx.send(f"Lỗi: {e}")

# Khởi tạo bot
bot.run(bot_token)
