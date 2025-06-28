
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

### 🛠️ Coming Soon

* GUI version (Tkinter or PyQt)
* `.exe` standalone builder
* Progress bar integration
* Smart auto-quality selector (best merged + size optimized)

---

### ❤️ Credits

* Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
* Terminal vibes by `colorama`
* Coded with ☕ & 🔥 by [@AIwolfie](https://github.com/AIwolfie)

---

### 📸 Screenshot (Optional)

> Add a terminal screenshot here if you want — looks dope in README.

---

### 📜 License

MIT — free to modify, use, and share. Just don't sell it without flexing me 😉

````

---

Let me know if you'd like:
- A GUI app version of this
- A terminal screenshot banner for the README
- GitHub Actions to auto-lint or test this repo

You're good to commit this as `README.md`:

```bash
echo "<paste above markdown>" > README.md
git add README.md
git commit -m "Add project README"
git push origin main
````
