import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot đang chạy: {bot.user}')

@bot.command()
async def send(ctx, user_token: str, channel_id: str, *, message: str):
    headers = {
        'Authorization': user_token,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0'
    }

    payload = {'content': message}
    url = f'https://discord.com/api/v9/channels/{channel_id}/messages'

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            await ctx.send(f'Đã gửi: "{message}" tới {channel_id}')
        elif response.status_code == 429:
            await ctx.send('Rate limited! Thử lại sau.')
        else:
            await ctx.send(f'Lỗi gửi: {response.status_code} - {response.text}')
    except Exception as e:
        await ctx.send(f'Lỗi kết nối: {e}')

bot.run('MTM3MDYyMTA1MTcxNzAyNTgxMw.Gc3lWS.Y-Wkrp-PXnaawq39XkPUDCzGl2nywUlWhEP6no')  # Thay bằng bot token thật
