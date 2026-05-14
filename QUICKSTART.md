# Quick Start Guide

Get up and running in 5 minutes!

## ⚡ Super Quick Start

```bash
# 1. Install dependency
pip install requests

# 2. Run GUI
python miktex_gui.py

# 3. In GUI:
#    - Go to "Compile & Fetch" tab
#    - Select your .tex file
#    - Click "Fetch & Compile"
#    - Done!
```

---

## 📋 Prerequisites

- ✅ Python 3.7+ installed
- ✅ MiKTeX installed
- ✅ Internet access to Iranian mirror

---

## 🚀 Installation

### Step 1: Install Python Package
```bash
pip install requests
```

### Step 2: Configure MiKTeX (One-time)
1. Open **MiKTeX Console**
2. Go to **Settings** > **Directories**
3. Click **+** (Add)
4. Browse to `D:\miktex_local_repo`
5. Click **OK**

### Step 3: Run GUI
**Windows:**
```bash
run_gui.bat
```

**Or:**
```bash
python miktex_gui.py
```

---

## 🎯 First Use

### Scenario 1: Compile a Document

1. **Open GUI**
2. **Go to "Compile & Fetch" tab**
3. **Click "Browse..."** and select your `.tex` file
4. **Click "🚀 Fetch & Compile"**
5. **Wait** - The app will:
   - Compile your document
   - Detect missing packages
   - Download them automatically
   - Retry compilation
   - Show success message

**That's it!** Your PDF is ready.

### Scenario 2: Fetch a Single Package

1. **Open GUI**
2. **Go to "Manual Fetch" tab**
3. **Enter package name** (e.g., "amsmath")
4. **Click "Fetch Package"**
5. **Done!**

### Scenario 3: Fetch Multiple Packages

1. **Open GUI**
2. **Go to "Manual Fetch" tab**
3. **Enter package names** (one per line):
   ```
   amsmath
   geometry
   hyperref
   graphicx
   ```
4. **Click "Fetch All"**
5. **Done!**

---

## 💡 Tips

### Tip 1: Use Common Packages Buttons
In "Manual Fetch" tab, click any of the 15 common package buttons for instant download.

### Tip 2: Check Before Fetching
Use "🔍 Check Packages" to see what's needed before downloading.

### Tip 3: Sync Metadata Weekly
Go to "Update Packages" tab and click "🔄 Sync Metadata" once a week.

### Tip 4: Choose Your Compiler
In "Compile & Fetch" tab, select your preferred compiler:
- pdflatex (default)
- xelatex (for Unicode/fonts)
- lualatex (modern)

---

## 🐛 Common Issues

### "Python not found"
**Fix:** Install Python from https://www.python.org

### "requests module not found"
**Fix:** Run `pip install requests`

### "MiKTeX not found"
**Fix:** Make sure MiKTeX is installed and in PATH

### "Cannot access mirror"
**Fix:** Check internet connection

### "Packages not installing"
**Fix:** Make sure MiKTeX Console has `D:\miktex_local_repo` added

---

## 📖 Next Steps

- Read [README.md](README.md) for detailed documentation
- Check [GITHUB_UPLOAD.md](GITHUB_UPLOAD.md) to upload to GitHub
- See [CHANGELOG.md](CHANGELOG.md) for version history

---

## 🎉 You're Ready!

Start compiling your LaTeX documents with automatic package management!

**Need help?** Check the "About" tab in the GUI or open an issue on GitHub.
