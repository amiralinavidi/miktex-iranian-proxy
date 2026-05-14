# MiKTeX Iranian Mirror Proxy - GUI Application

A comprehensive graphical application for managing MiKTeX packages through the Iranian CTAN mirror, with automatic compile-time package detection and installation.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🌟 Features

### 🚀 Compile-Time Package Detection
- **Automatic Detection**: Compiles your LaTeX document and detects missing packages in real-time
- **Auto-Fetch**: Automatically downloads missing packages from the Iranian mirror
- **Retry Logic**: Attempts compilation multiple times, fetching packages as needed
- **Smart Detection**: Parses compiler errors to identify exactly what's missing

### 📦 Package Management
- **Manual Fetch**: Download individual packages
- **Batch Operations**: Fetch multiple packages at once
- **Common Packages**: Quick access to frequently used packages
- **Update Management**: Update all installed packages

### 🎨 Clean GUI Interface
- **Tabbed Interface**: Organized into logical sections
- **Real-time Output**: See what's happening as it happens
- **Progress Tracking**: Visual feedback for all operations
- **Easy Navigation**: Intuitive design for all skill levels

### 🔧 Additional Features
- Repository status monitoring
- Configurable settings
- Comprehensive logging
- Support for multiple LaTeX compilers (pdflatex, xelatex, lualatex)

---

## 📋 Requirements

- **Python 3.7 or higher**
- **MiKTeX** installed and configured
- **Internet access** to Iranian CTAN mirror
- **Python packages**: `requests` (install with `pip install requests`)

---

## 🚀 Quick Start

### Installation

1. **Download or clone this repository**
   ```bash
   git clone https://github.com/yourusername/miktex-iranian-proxy.git
   cd miktex-iranian-proxy/final_version
   ```

2. **Install Python dependencies**
   ```bash
   pip install requests
   ```

3. **Run the GUI**
   - **Windows**: Double-click `run_gui.bat`
   - **Command line**: `python miktex_gui.py`

### First-Time Setup

1. **Configure MiKTeX** (one-time):
   - Open MiKTeX Console
   - Go to Settings > Directories
   - Add `D:\miktex_local_repo`
   - Click OK

2. **Sync Metadata**:
   - Open the GUI
   - Go to "Update Packages" tab
   - Click "Sync Metadata"

---

## 📖 How to Use

### Method 1: Automatic Compile & Fetch (Recommended)

This is the easiest way - the app handles everything automatically!

1. Go to **"Compile & Fetch"** tab
2. Click **"Browse..."** and select your `.tex` file
3. Click **"🚀 Fetch & Compile"**
4. The app will:
   - Compile your document
   - Detect any missing packages
   - Automatically download them
   - Retry compilation
   - Repeat until successful or max iterations reached

**Example:**
```
Iteration 1: Compile → Missing: amsmath, geometry
             Fetch amsmath, geometry
Iteration 2: Compile → Missing: hyperref
             Fetch hyperref
Iteration 3: Compile → Success! ✓
```

### Method 2: Check First, Then Fetch

1. Go to **"Compile & Fetch"** tab
2. Select your `.tex` file
3. Click **"🔍 Check Packages"** to see what's needed
4. Click **"📥 Fetch Missing Packages"** to download them
5. Click **"▶️ Compile Document"** to compile

### Method 3: Manual Package Fetch

1. Go to **"Manual Fetch"** tab
2. Enter package name or click a common package button
3. Package is downloaded automatically

### Method 4: Batch Fetch

1. Go to **"Manual Fetch"** tab
2. Enter package names (one per line) in the text area
3. Click **"Fetch All"**

---

## 🎯 Use Cases

### Use Case 1: New LaTeX Project

```
1. Create your document.tex
2. Open GUI → Compile & Fetch tab
3. Select document.tex
4. Click "Fetch & Compile"
5. Done! PDF is ready
```

### Use Case 2: Existing Project with Missing Packages

```
1. Open GUI → Compile & Fetch tab
2. Select your main.tex
3. Click "Fetch & Compile"
4. App detects and installs all missing packages
5. Document compiles successfully
```

### Use Case 3: Preparing for Offline Work

```
1. Open GUI → Manual Fetch tab
2. Enter all packages you'll need (one per line)
3. Click "Fetch All"
4. Work offline with cached packages
```

---

## 🖥️ GUI Overview

### Tab 1: Compile & Fetch
- **File Selection**: Browse for your `.tex` file
- **Options**: 
  - Auto-fetch missing packages
  - Compile after fetching
  - Compiler selection (pdflatex, xelatex, lualatex)
- **Actions**:
  - Check Packages: See what's needed
  - Fetch Missing: Download missing packages
  - Compile: Compile the document
  - Fetch & Compile: Do everything automatically
- **Output**: Real-time compilation and fetch logs

### Tab 2: Manual Fetch
- **Single Package**: Enter name and fetch
- **Common Packages**: Quick buttons for popular packages
- **Batch Fetch**: Enter multiple packages (one per line)
- **Output**: Download progress and results

### Tab 3: Update Packages
- **List Installed**: See all installed packages
- **Update All**: Update all packages from mirror
- **Sync Metadata**: Update repository metadata
- **Output**: Update progress and results

### Tab 4: Settings
- **Repository Settings**: Configure mirror URL and local path
- **Status**: View repository information
- **Save Settings**: Persist configuration

### Tab 5: About
- Version information
- Feature list
- Usage instructions

---

## ⚙️ Configuration

### Default Settings

- **Mirror URL**: `http://ctan.yazd.ac.ir/systems/win32/miktex/tm/packages/`
- **Local Repository**: `D:/miktex_local_repo`
- **Default Compiler**: `pdflatex`

### Changing Settings

1. Go to **Settings** tab
2. Modify Mirror URL or Local Repository path
3. Click **"Save Settings"**
4. Restart the application

---

## 🔍 How It Works

### Compile-Time Detection

The app uses a smart algorithm:

1. **Compile**: Runs your chosen LaTeX compiler
2. **Parse Output**: Analyzes compiler errors and warnings
3. **Extract Missing Packages**: Identifies packages that caused errors
4. **Fetch**: Downloads missing packages from Iranian mirror
5. **Retry**: Compiles again with new packages
6. **Repeat**: Continues until success or max iterations (3)

### Package Detection Patterns

The app detects missing packages from:
- `! LaTeX Error: File 'package.sty' not found`
- `! Package X Error`
- Compilation failures due to missing dependencies

### Automatic Retry Logic

```
Max Iterations: 10

Iteration 1:
  Compile → Detect missing → Fetch → Retry

Iteration 2:
  Compile → Detect missing → Fetch → Retry

Iteration 3:
  Compile → Success or Report Failure
```

---

## 📊 Advantages Over Command-Line Version

| Feature | Command-Line | GUI |
|---------|-------------|-----|
| Ease of Use | Moderate | Easy |
| Visual Feedback | Limited | Excellent |
| Compile-Time Detection | Manual | Automatic |
| Package Browsing | No | Yes |
| Real-time Output | Terminal only | Scrollable window |
| Settings Management | Edit files | GUI interface |
| Batch Operations | Scripts needed | Built-in |

---

## 🐛 Troubleshooting

### "Python not found"
**Solution**: Install Python 3.7+ from https://www.python.org

### "requests module not found"
**Solution**: Run `pip install requests`

### "MiKTeX not found"
**Solution**: Make sure MiKTeX is installed and in your PATH

### "Cannot access mirror"
**Solution**: Check your internet connection and verify mirror URL

### "Packages not installing"
**Solution**: 
1. Check Settings tab for repository status
2. Make sure MiKTeX Console has D:\miktex_local_repo added
3. Try syncing metadata first

### "Compilation fails repeatedly"
**Solution**:
1. Check the output log for specific errors
2. Some packages might not be on the mirror
3. Try fetching packages manually first

---

## 📁 File Structure

```
final_version/
├── miktex_gui.py          # Main GUI application
├── run_gui.bat            # Windows launcher
├── README.md              # This file
├── GITHUB_UPLOAD.md       # GitHub upload instructions
├── LICENSE                # MIT License
└── screenshots/           # Screenshots for documentation
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

- **Iranian CTAN Mirror**: Yazd University (http://ctan.yazd.ac.ir)
- **MiKTeX**: Christian Schenk
- **Python**: Python Software Foundation

---

## 📞 Support

For issues and questions:

1. Check the **Troubleshooting** section
2. Review the **About** tab in the GUI
3. Open an issue on GitHub

---

## 🔄 Version History

### v2.0 (Current)
- ✨ Added GUI interface
- ✨ Compile-time package detection
- ✨ Automatic retry logic
- ✨ Batch operations
- ✨ Settings management

### v1.0
- ✅ Command-line interface
- ✅ Manual package fetching
- ✅ Basic update functionality

---

## 🎯 Roadmap

Future improvements:
- [ ] Package dependency resolution
- [ ] Download progress bars
- [ ] Package search functionality
- [ ] Multiple mirror support
- [ ] Automatic MiKTeX configuration
- [ ] Package cache management
- [ ] Export/import package lists

---

## ⭐ Star This Project

If you find this useful, please star the repository on GitHub!

---

**Made with ❤️ for Iranian LaTeX users**
