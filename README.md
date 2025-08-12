League TFT Bot 🎯
A simple Python bot that queues up for TFT Ranked in the League of Legends client after a timer delay, and automatically accepts the match when the popup appears.

📦 Installation
Make sure you have Python 3 installed.
Install the required packages:

bash
Kopiëren
Bewerken
pip install pyautogui pillow pygetwindow opencv-python
▶️ Running the Bot Directly (Without .bat File)
From the terminal (inside this project folder), run:

bash
Kopiëren
Bewerken
python tft_queue.py --minutes 0.1 --img-dir "./imgs" --confidence 0.8
--minutes 0.1 → Waits 0.1 minutes (6 seconds) before starting clicks

--img-dir "./imgs" → Path to your screenshots folder

--confidence 0.8 → Image match confidence (lower if matches are missed)

⚡ Using the Bot with a .bat File (Recommended)
This method prompts you for the wait time in seconds every time you run it.

1️⃣ Create the .bat File
Open Notepad

Paste this code (update paths if needed):

bat
Kopiëren
Bewerken
@echo off
set /p wait_seconds=Enter wait time in seconds: 
python "C:\xampp\htdocs\bot project\League-tft-bot\tft_queue.py" --seconds %wait_seconds% --img-dir "C:\xampp\htdocs\bot project\League-tft-bot\imgs" --confidence 0.8
pause
💡 If Python isn’t on your PATH, replace python with the full path to your python.exe.

2️⃣ Save the File
File → Save As…

Save as type: All Files

File name: start_bot.bat

Location: C:\xampp\htdocs\bot project\League-tft-bot

3️⃣ Run It
Double-click start_bot.bat

Enter your desired wait time (in seconds) when prompted

The bot will start after that delay

📌 Pinning to Taskbar
Windows doesn’t allow pinning .bat files directly, so:

Right-click start_bot.bat → Create shortcut

Right-click the shortcut → Properties

Target:

bash
Kopiëren
Bewerken
C:\Windows\System32\cmd.exe /k "C:\xampp\htdocs\bot project\League-tft-bot\start_bot.bat"
Start in:

makefile
Kopiëren
Bewerken
C:\xampp\htdocs\bot project\League-tft-bot
(Optional) Change the icon to something TFT-themed

Pin the shortcut to your taskbar

🖼 Image Setup
All .png files in /imgs must match your League client resolution and scale

Recommended sequence:

1_play.png – Play button

2_tft.png – TFT mode

3_ranked.png – Ranked mode

4_confirm.png – Confirm button

5_find_match.png – Find Match button

6_accept.png – Accept match popup

⚠️ Disclaimer
This bot simulates mouse clicks based on screen images.
Use at your own risk — automation in online games may be against the terms of service.