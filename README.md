
# 🔥 YouTube Boss Downloader

A modern, terminal-based YouTube video/audio downloader built with **Python + yt-dlp**  
Supports **video**, **audio**, **playlists**, **live streams**, and even **DASH** formats.

> 💣 No nonsense. Just paste the link, pick the quality, and it's yours.

---

### ⚡ Features

- 🎥 Download YouTube videos in any resolution
- 🎵 Audio-only downloads (M4A/MP3)
- 📺 Playlist and Live stream support
- 🧠 Automatically merges video-only formats with best audio
- 📡 Handles DASH / m3u8 / live stream formats with fallback
- 🎯 Clean terminal UI with spinners and color
- ✅ Auto-detects `yt-dlp` and installs if missing
- 🛠️ Auto-warns if `ffmpeg` is not installed

---

### 🚀 Installation

**1. Clone the repo**

```bash
git clone https://github.com/AIwolfie/youtube-video-downloader.git
cd youtube-video-downloader
````

**2. Install dependencies**

```bash
pip install colorama
```

**3. Make sure these are installed on your system:**

* [yt-dlp](https://github.com/yt-dlp/yt-dlp) (auto-installs if missing via `winget`)
* [ffmpeg](https://ffmpeg.org/download.html) (required for merging audio+video)

```bash
winget install yt-dlp
winget install ffmpeg
```

---

### 💡 Usage

```bash
python yt_boss_downloader.py
```

🔗 Paste a YouTube URL (video or playlist)
🎧 Choose audio-only or full video
🎯 Select a format
📂 Choose a download location
⚡ Done!

---

### 🧠 Format Notes

* If you select a **video-only format**, the script auto-merges it with the best audio
* If **no formats are shown**, the video may be:

  * Still live or not processed yet
  * Using restricted DASH/m3u8
  * Behind age/geo-restrictions

In such cases, the script will offer a fallback using:

```bash
yt-dlp --allow-unplayable-formats <url>
```

---

### 📁 Output

Downloaded files will be saved in the folder you choose, in `.mp4` or `.m4a` format (based on type).

---


### ❤️ Credits

* Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* Terminal vibes by `colorama`
* Coded with ☕ & 🔥 by [@AIwolfie](https://github.com/AIwolfie)

---
