import time
import argparse
import sys
import os
import pyautogui

pyautogui.FAILSAFE = True  # move mouse to a corner to abort

try:
    import pygetwindow as gw
except Exception:
    gw = None

# ---------- Helpers ----------

def locate_center(image_path, confidence=0.8, region=None):
    """Return center point if found, else None. Never raise on miss."""
    try:
        return pyautogui.locateCenterOnScreen(
            image_path, confidence=confidence, region=region
        )
    except Exception:
        # When OpenCV is installed, PyAutoGUI can raise ImageNotFoundException on misses.
        return None



def find_and_click(image_path, confidence=0.8, timeout=12, move_first=True, region=None):
    start = time.time()
    while time.time() - start < timeout:
        loc = locate_center(image_path, confidence, region)
        if loc:
            if move_first:
                pyautogui.moveTo(loc)
            pyautogui.click(loc)
            return True
        time.sleep(0.3)
    return False


def watch_and_click(image_path, confidence=0.8, poll=0.5, max_wait=30, region=None):
    start = time.time()
    while time.time() - start < max_wait:
        loc = locate_center(image_path, confidence, region)
        if loc:
            pyautogui.click(loc)
            return True
        time.sleep(poll)
    return False


def focus_league(window_hint="League of Legends"):
    if not gw:
        return False
    wins = [w for w in gw.getAllTitles() if window_hint.lower() in w.lower()]
    if not wins:
        return False
    for w in gw.getWindowsWithTitle(wins[0]):
        try:
            w.activate()
            time.sleep(0.3)
            return True
        except Exception:
            continue
    return False

# ---------- Main ----------

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--minutes", type=float, required=True, help="Delay before starting the click sequence")
    p.add_argument("--img-dir", type=str, default="./imgs")
    p.add_argument("--confidence", type=float, default=0.8)
    p.add_argument("--window-hint", type=str, default="League of Legends")
    p.add_argument("--accept-timeout", type=int, default=7200, help="Max seconds to wait for Accept popup")
    args = p.parse_args()

    # Expected images
    seq = [
        os.path.join(args.img_dir, "1_play.png"),
        os.path.join(args.img_dir, "2_tft.png"),
        os.path.join(args.img_dir, "3_ranked.png"),
        os.path.join(args.img_dir, "4_confirm.png"),
    ]
    find_match_img = os.path.join(args.img_dir, "5_find_match.png")
    accept_img = os.path.join(args.img_dir, "6_accept.png")

    for pth in seq + [find_match_img, accept_img]:
        if not os.path.exists(pth):
            sys.exit(f"Missing image: {pth}")

    # Countdown
    seconds = int(args.minutes * 60)
    print(f"Timer started for {args.minutes} minutes…")
    for s in range(seconds, 0, -1):
        if s % 10 == 0 or s <= 5:
            print(f"{s}s remaining")
        time.sleep(1)

    # Focus League
    if not focus_league(args.window_hint):
        print("Warning: couldn't focus League automatically. Ensure the client is visible on the same monitor used for screenshots.")

    # Click through PLAY → TFT → RANKED → CONFIRM
    for step, img in enumerate(seq, start=1):
        ok = find_and_click(img, confidence=args.confidence, timeout=15)
        if not ok:
            sys.exit(f"Couldn't find step {step} image: {img}")
        time.sleep(0.6)

    # Wait a bit before trying to click Find Match (handles the greyed-out state)
    print("Waiting 2.5 seconds for Find Match to enable…")
    time.sleep(2.5)  # Increase if your client enables slowly

    # Click Find Match in lower-center region
    screen_w, screen_h = pyautogui.size()
    lower_region = (int(screen_w*0.2), int(screen_h*0.55), int(screen_w*0.6), int(screen_h*0.4))
    fm_ok = watch_and_click(
        find_match_img,
        confidence=max(0.7, args.confidence - 0.05),
        poll=0.4,
        max_wait=25,
        region=lower_region,
    )
    if not fm_ok:
        sys.exit("Couldn't find the Find Match button after delay. Re-crop the image or lower --confidence.")

    # Watch for ACCEPT popup (center region)
    print("Queued. Watching for ACCEPT popup… (Ctrl+C to stop)")
    screen_w, screen_h = pyautogui.size()
    center_region = (int(screen_w*0.25), int(screen_h*0.2), int(screen_w*0.5), int(screen_h*0.6))

    start = time.time()
    accepted = False
    while time.time() - start < args.accept_timeout:
        loc = locate_center(accept_img, confidence=max(0.7, args.confidence - 0.05), region=center_region)
        if loc:
            pyautogui.click(loc)
            print("Accepted match!")
            accepted = True
            break
        # Heartbeat so you can see it's waiting
        if int(time.time() - start) % 5 == 0:
            print("…still waiting for Accept")
        time.sleep(0.5)

    if not accepted:
        print("Gave up waiting for Accept.")


if __name__ == "__main__":
    main()