```bat
@echo off
set /p wait_seconds=Enter wait time in seconds: 
set /a wait_minutes=%wait_seconds%/60
python "C:\xampp\htdocs\bot project\League-tft-bot\tft_queue.py" --minutes %wait_minutes% --img-dir "C:\xampp\htdocs\bot project\League-tft-bot\imgs" --confidence 0.8
pause
```