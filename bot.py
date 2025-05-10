import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot đang chạy: {bot.user}')

@bot.command()
async def send(ctx, user_token: str, *args):
    try:
        if '--' not in args:
            await ctx.send("Thiếu dấu `--` để phân cách kênh và tin nhắn.")
            return

        split_index = args.index('--')
        channel_ids = args[:split_index]
        message = ' '.join(args[split_index + 1:])

        headers = {
            'Authorization': user_token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }

        for channel_id in channel_ids:
            url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
            payload = {"content": message}
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                await ctx.send(f"Đã gửi tới {channel_id}")
            elif response.status_code == 429:
                retry = response.json().get("retry_after", 10)
                await ctx.send(f"Rate limited, đợi {retry} giây")
            else:
                await ctx.send(f"Lỗi gửi {channel_id}: {response.status_code} - {response.text}")
    except Exception as e:
        await ctx.send(f"Lỗi: {e}")

bot.run("YOUR_BOT_TOKEN_HERE")  # <-- Thay bằng Bot Token thật
