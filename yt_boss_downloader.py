import subprocess
import sys
import shutil
import os
import threading
import time
from colorama import init, Fore, Style

init(autoreset=True)

spinner_running = False

def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""                                                        
 __ __ _____     ____                _           _           
|  |  |_   _|___|    \ ___ _ _ _ ___| |___ ___ _| |___ ___   
|_   _| | | |___|  |  | . | | | |   | | . | .'| . | -_|  _|  
  |_|   |_|     |____/|___|_____|_|_|_|___|__,|___|___|_|    
                                                             
    """ + Fore.MAGENTA + "🔥 YouTube Boss Downloader 🔥\n" + Style.RESET_ALL)

def spinner(msg):
    global spinner_running
    spinner_running = True
    chars = ['|', '/', '-', '\\']
    idx = 0
    while spinner_running:
        print(Fore.YELLOW + f'\r{msg} ' + chars[idx % len(chars)], end='', flush=True)
        idx += 1
        time.sleep(0.1)

def stop_spinner():
    global spinner_running
    spinner_running = False
    print('\r', end='', flush=True)

def is_yt_dlp_installed():
    return shutil.which("yt-dlp") is not None

def is_ffmpeg_installed():
    return shutil.which("ffmpeg") is not None

def install_yt_dlp():
    print(Fore.YELLOW + "[!] yt-dlp not found. Installing with winget... 💾")
    try:
        subprocess.run(["winget", "install", "--id", "yt-dlp.yt-dlp", "-e", "--accept-source-agreements", "--accept-package-agreements"], check=True)
        print(Fore.GREEN + "[+] yt-dlp installed successfully.\n")
    except subprocess.CalledProcessError:
        print(Fore.RED + "[-] Installation failed. Install manually.")
        sys.exit(1)

def get_formats(url, allow_unplayable=False):
    print(Fore.CYAN + "[*] Fetching available formats...\n")
    cmd = ["yt-dlp", "-F", url]
    if allow_unplayable:
        cmd.append("--allow-unplayable-formats")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return ""

def parse_formats(output, audio_only=False):
    formats = []
    lines = output.splitlines()
    for line in lines:
        if line.strip().startswith("format code"):
            continue
        if "audio only" in line and audio_only:
            parts = line.split()
            if len(parts) > 2 and parts[0].isdigit():
                formats.append((parts[0], " ".join(parts[1:])))
        elif not audio_only and "video" in line:
            parts = line.split()
            if len(parts) > 2 and parts[0].isdigit():
                formats.append((parts[0], " ".join(parts[1:])))
    return formats

def is_video_only(format_desc):
    return "video only" in format_desc.lower()

def show_formats(formats, audio_only=False):
    if not formats:
        return
    print(Fore.MAGENTA + ("🎵 Available Audio Formats:\n" if audio_only else "📺 Available Video Formats:\n"))
    for i, (fid, desc) in enumerate(formats):
        print(Fore.CYAN + f"[{i}] " + Fore.YELLOW + f"Format ID: {fid}" + Fore.GREEN + f" | {desc}")

def get_output_directory():
    path = input(Fore.BLUE + "\n📁 Enter directory to save the file (leave blank for current directory): ").strip()
    if not path:
        return os.getcwd()
    os.makedirs(path, exist_ok=True)
    return os.path.abspath(path)

def download(url, format_id, output_path, audio_only=False, merge_with_audio=False):
    print(Fore.YELLOW + f"\n🚀 Starting download (Format ID: {format_id})...\n")
    template = os.path.join(output_path, "%(title)s.%(ext)s")

    # Merge audio if needed
    if merge_with_audio:
        format_selector = f"{format_id}+bestaudio"
    else:
        format_selector = format_id

    cmd = [
        "yt-dlp",
        "-f", format_selector,
        "-o", template,
        url  # 🔥 FIXED: This was missing!
    ]

    if not audio_only or merge_with_audio:
        cmd += ["--merge-output-format", "mp4"]

    if merge_with_audio and not is_ffmpeg_installed():
        print(Fore.RED + "\n❌ ffmpeg is required to merge video and audio. Please install ffmpeg.")
        sys.exit(1)

    thread = threading.Thread(target=spinner, args=("⏳ Downloading",))
    thread.start()

    try:
        subprocess.run(cmd, check=True)
        stop_spinner()
        print(Fore.GREEN + "\n✅ Download completed and merged successfully!")
    except subprocess.CalledProcessError:
        stop_spinner()
        print(Fore.RED + "\n❌ Download failed.")
        sys.exit(1)

def fallback_download(url, output_path):
    print(Fore.YELLOW + "\n⚠️ No regular formats found. Trying DASH/live fallback...\n")
    template = os.path.join(output_path, "%(title)s.%(ext)s")
    thread = threading.Thread(target=spinner, args=("📡 Attempting to record live stream",))
    thread.start()

    try:
        subprocess.run(["yt-dlp", "--allow-unplayable-formats", "-o", template, url], check=True)
        stop_spinner()
        print(Fore.GREEN + "\n✅ Live stream recorded or fallback download complete!")
    except subprocess.CalledProcessError:
        stop_spinner()
        print(Fore.RED + "❌ Could not download the stream.")
        sys.exit(1)

def main():
    banner()

    if not is_yt_dlp_installed():
        install_yt_dlp()

    url = input(Fore.BLUE + "🔗 Enter YouTube video or playlist URL: ").strip()
    audio_only = input(Fore.YELLOW + "\n🎧 Do you want to download audio only? (y/n): ").strip().lower() == 'y'

    raw_output = get_formats(url)
    formats = parse_formats(raw_output, audio_only=audio_only)

    if not formats:
        print(Fore.RED + "\n❌ No downloadable formats found.")
        choice = input(Fore.YELLOW + "⚙️  Try fallback recording mode? (for live streams) [y/n]: ").strip().lower()
        if choice == 'y':
            output_path = get_output_directory()
            fallback_download(url, output_path)
            return
        else:
            print(Fore.RED + "\n💡 Try again later. The stream may still be processing.")
            sys.exit(0)

    show_formats(formats, audio_only=audio_only)

    try:
        idx = int(input(Fore.BLUE + f"\n🎯 Choose format [0-{len(formats)-1}]: "))
        if not (0 <= idx < len(formats)):
            raise ValueError
    except ValueError:
        print(Fore.RED + "❌ Invalid selection.")
        sys.exit(1)

    format_id, format_desc = formats[idx]
    output_path = get_output_directory()

    merge_audio = is_video_only(format_desc)
    if merge_audio:
        print(Fore.YELLOW + "\n🔗 Selected format is video-only. Auto-adding best audio stream for merging.\n")

    download(url, format_id, output_path, audio_only=audio_only, merge_with_audio=merge_audio)

if __name__ == "__main__":
    main()
