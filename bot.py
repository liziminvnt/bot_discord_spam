import requests
import time
import random

# ====== CẤU HÌNH ======
TOKEN = 'YOUR_USER_TOKEN_HERE'  # Thay bằng token thật của tài khoản bạn
CHANNEL_IDS = [
    '123456789012345678',  # Thay bằng ID thật của các kênh
    '234567890123456789',
    '345678901234567890'
]

MESSAGES = [
    'Mình là Xuân Anh đây!',
    'Có ai online không?',
    'Lướt chơi tí nè!',
    'Spam nhẹ nhẹ cho vui!',
    'Có thấy tin mình không vậy?'
]

# ====== HEADER BẮT BUỘC ======
headers = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'  # Giả lập trình duyệt thật
}

# ====== VÒNG LẶP ======
while True:
    for channel_id in CHANNEL_IDS:
        url = f'https://discord.com/api/v9/channels/{channel_id}/messages'
        message = random.choice(MESSAGES)
        payload = {'content': message}

        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                print(f'Đã gửi tới {channel_id}: "{message}"')
            elif response.status_code == 429:
                print('==> Bị rate limited! Dừng lại tạm thời.')
                retry_after = response.json().get('retry_after', 10)
                time.sleep(retry_after)
            else:
                print(f'Lỗi gửi tới {channel_id}: {response.status_code} - {response.text}')
        except Exception as e:
            print(f'Lỗi mạng hoặc kết nối: {e}')

    time.sleep(60)  # Gửi 1 phút 1 lần
