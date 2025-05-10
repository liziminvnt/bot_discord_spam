#!/bin/bash

while true
do
    echo "Khởi động bot.py..."
    python3 bot.py
    echo "bot.py đã dừng. Tự động khởi động lại sau 5 giây..."
    sleep 5
done
