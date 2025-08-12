@echo off
set /p wait_seconds=Enter wait time in seconds: 
python "C:\xampp\htdocs\bot project\League-tft-bot\tft_queue.py" --seconds %wait_seconds% --img-dir "C:\xampp\htdocs\bot project\League-tft-bot\imgs" --confidence 0.8
pause