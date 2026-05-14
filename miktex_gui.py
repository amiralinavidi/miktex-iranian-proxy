#!/usr/bin/env python3
"""
MiKTeX Iranian Mirror Proxy - GUI Application

A graphical interface for managing MiKTeX packages through the Iranian CTAN mirror.
"""

import os
import sys
import json
import time
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from pathlib import Path
from datetime import datetime
import re

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    import requests
except ImportError:
    print("Error: requests library not installed. Run: pip install requests")
    sys.exit(1)


class MiKTeXProxyGUI:
    """Main GUI application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MiKTeX Iranian Mirror Proxy v2.0")
        self.root.geometry("900x700")
        
        # Configuration
        self.mirror_url = "http://ctan.yazd.ac.ir/systems/win32/miktex/tm/packages/"
        self.local_repo = Path("D:/miktex_local_repo")
        self.config_file = self.local_repo / "config.json"
        
        # State
        self.is_running = False
        self.current_process = None
        
        # Setup UI
        self.setup_ui()
        
        # Load config
        self.load_config()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Compile & Fetch
        self.compile_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.compile_tab, text="📄 Compile & Fetch")
        self.setup_compile_tab()
        
        # Tab 2: Manual Fetch
        self.fetch_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fetch_tab, text="📦 Manual Fetch")
        self.setup_fetch_tab()
        
        # Tab 3: Update Packages
        self.update_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.update_tab, text="🔄 Update Packages")
        self.setup_update_tab()
        
        # Tab 4: Settings
        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="⚙️ Settings")
        self.setup_settings_tab()
        
        # Tab 5: About
        self.about_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.about_tab, text="ℹ️ About")
        self.setup_about_tab()
        
        # Status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def setup_compile_tab(self):
        """Setup compile and auto-fetch tab"""
        
        # File selection
        file_frame = ttk.LabelFrame(self.compile_tab, text="LaTeX Document", padding=10)
        file_frame.pack(fill='x', padx=10, pady=5)
        
        self.tex_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.tex_file_var, width=60).pack(side='left', padx=5)
        ttk.Button(file_frame, text="Browse...", command=self.browse_tex_file).pack(side='left')
        
        # Options
        options_frame = ttk.LabelFrame(self.compile_tab, text="Options", padding=10)
        options_frame.pack(fill='x', padx=10, pady=5)
        
        self.auto_fetch_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Auto-fetch missing packages", 
                       variable=self.auto_fetch_var).pack(anchor='w')
        
        self.compile_after_fetch_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Compile after fetching packages", 
                       variable=self.compile_after_fetch_var).pack(anchor='w')
        
        # Compiler selection
        compiler_frame = ttk.Frame(options_frame)
        compiler_frame.pack(fill='x', pady=5)
        ttk.Label(compiler_frame, text="Compiler:").pack(side='left', padx=5)
        
        self.compiler_var = tk.StringVar(value="pdflatex")
        compilers = ["pdflatex", "xelatex", "lualatex", "latex"]
        ttk.Combobox(compiler_frame, textvariable=self.compiler_var, 
                    values=compilers, width=15, state='readonly').pack(side='left')
        
        # Action buttons
        button_frame = ttk.Frame(self.compile_tab)
        button_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(button_frame, text="🔍 Check Packages", 
                  command=self.check_packages).pack(side='left', padx=5)
        ttk.Button(button_frame, text="📥 Fetch Missing Packages", 
                  command=self.fetch_missing_packages).pack(side='left', padx=5)
        ttk.Button(button_frame, text="▶️ Compile Document", 
                  command=self.compile_document).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🚀 Fetch & Compile", 
                  command=self.fetch_and_compile).pack(side='left', padx=5)
        
        # Output
        output_frame = ttk.LabelFrame(self.compile_tab, text="Output", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.compile_output = scrolledtext.ScrolledText(output_frame, height=20, wrap=tk.WORD)
        self.compile_output.pack(fill='both', expand=True)
        
    def setup_fetch_tab(self):
        """Setup manual package fetch tab"""
        
        # Package input
        input_frame = ttk.LabelFrame(self.fetch_tab, text="Package Name", padding=10)
        input_frame.pack(fill='x', padx=10, pady=5)
        
        self.package_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.package_var, width=40).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Fetch Package", 
                  command=self.fetch_single_package).pack(side='left', padx=5)
        
        # Common packages
        common_frame = ttk.LabelFrame(self.fetch_tab, text="Common Packages", padding=10)
        common_frame.pack(fill='x', padx=10, pady=5)
        
        common_packages = [
            "latex", "amsmath", "geometry", "hyperref", "graphicx",
            "xcolor", "fontspec", "babel", "tikz", "beamer",
            "biblatex", "natbib", "listings", "algorithm2e", "booktabs"
        ]
        
        # Create grid of buttons
        for i, pkg in enumerate(common_packages):
            row = i // 5
            col = i % 5
            ttk.Button(common_frame, text=pkg, width=12,
                      command=lambda p=pkg: self.fetch_package(p)).grid(row=row, column=col, padx=2, pady=2)
        
        # Batch fetch
        batch_frame = ttk.LabelFrame(self.fetch_tab, text="Batch Fetch", padding=10)
        batch_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(batch_frame, text="Enter package names (one per line):").pack(anchor='w')
        self.batch_packages = scrolledtext.ScrolledText(batch_frame, height=5, wrap=tk.WORD)
        self.batch_packages.pack(fill='x', pady=5)
        
        ttk.Button(batch_frame, text="Fetch All", 
                  command=self.fetch_batch_packages).pack()
        
        # Output
        output_frame = ttk.LabelFrame(self.fetch_tab, text="Output", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.fetch_output = scrolledtext.ScrolledText(output_frame, height=15, wrap=tk.WORD)
        self.fetch_output.pack(fill='both', expand=True)
        
    def setup_update_tab(self):
        """Setup package update tab"""
        
        # Info
        info_frame = ttk.Frame(self.update_tab)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(info_frame, text="Update all installed MiKTeX packages from the Iranian mirror.",
                 wraplength=800).pack(anchor='w')
        
        # Actions
        action_frame = ttk.LabelFrame(self.update_tab, text="Actions", padding=10)
        action_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(action_frame, text="📋 List Installed Packages", 
                  command=self.list_installed_packages).pack(side='left', padx=5)
        ttk.Button(action_frame, text="🔄 Update All Packages", 
                  command=self.update_all_packages).pack(side='left', padx=5)
        ttk.Button(action_frame, text="🔄 Sync Metadata", 
                  command=self.sync_metadata).pack(side='left', padx=5)
        
        # Output
        output_frame = ttk.LabelFrame(self.update_tab, text="Output", padding=10)
        output_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.update_output = scrolledtext.ScrolledText(output_frame, height=20, wrap=tk.WORD)
        self.update_output.pack(fill='both', expand=True)
        
    def setup_settings_tab(self):
        """Setup settings tab"""
        
        # Repository settings
        repo_frame = ttk.LabelFrame(self.settings_tab, text="Repository Settings", padding=10)
        repo_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(repo_frame, text="Mirror URL:").grid(row=0, column=0, sticky='w', pady=5)
        self.mirror_url_var = tk.StringVar(value=self.mirror_url)
        ttk.Entry(repo_frame, textvariable=self.mirror_url_var, width=60).grid(row=0, column=1, padx=5)
        
        ttk.Label(repo_frame, text="Local Repository:").grid(row=1, column=0, sticky='w', pady=5)
        self.local_repo_var = tk.StringVar(value=str(self.local_repo))
        ttk.Entry(repo_frame, textvariable=self.local_repo_var, width=60).grid(row=1, column=1, padx=5)
        
        ttk.Button(repo_frame, text="Save Settings", 
                  command=self.save_settings).grid(row=2, column=1, sticky='e', pady=10)
        
        # Status
        status_frame = ttk.LabelFrame(self.settings_tab, text="Status", padding=10)
        status_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=15, wrap=tk.WORD)
        self.status_text.pack(fill='both', expand=True)
        
        ttk.Button(status_frame, text="Refresh Status", 
                  command=self.show_status).pack(pady=5)
        
        # Show initial status
        self.show_status()
        
    def setup_about_tab(self):
        """Setup about tab"""
        
        about_text = """
MiKTeX Iranian Mirror Proxy v2.0
================================

A comprehensive tool for managing MiKTeX packages through the Iranian CTAN mirror.

Features:
• Compile-time package detection and installation
• Automatic missing package fetching
• Manual package management
• Batch package operations
• Package update management
• Clean graphical interface

How to Use:
1. Go to "Compile & Fetch" tab
2. Select your .tex file
3. Click "Fetch & Compile"
4. The app will automatically detect missing packages, fetch them, and compile your document

Requirements:
• Python 3.7+
• MiKTeX installed
• Internet access to Iranian CTAN mirror

Mirror: http://ctan.yazd.ac.ir
Repository: D:/miktex_local_repo

Created for Iranian LaTeX users who cannot access international repositories.

Version: 2.0
Last Updated: May 2025
        """
        
        text_widget = scrolledtext.ScrolledText(self.about_tab, wrap=tk.WORD, 
                                               font=('Courier', 10))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', about_text)
        text_widget.config(state='disabled')
        
    # Helper methods
    
    def log(self, message, output_widget=None):
        """Log message to output widget and status bar"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_msg = f"[{timestamp}] {message}\n"
        
        if output_widget:
            output_widget.insert(tk.END, formatted_msg)
            output_widget.see(tk.END)
            output_widget.update()
        
        self.status_bar.config(text=message)
        self.root.update()
        
    def browse_tex_file(self):
        """Browse for .tex file"""
        filename = filedialog.askopenfilename(
            title="Select LaTeX Document",
            filetypes=[("LaTeX files", "*.tex"), ("All files", "*.*")]
        )
        if filename:
            self.tex_file_var.set(filename)
            
    def load_config(self):
        """Load configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.mirror_url = config.get('mirror_url', self.mirror_url)
                    self.mirror_url_var.set(self.mirror_url)
            except Exception as e:
                self.log(f"Error loading config: {e}")
                
    def save_settings(self):
        """Save settings"""
        self.mirror_url = self.mirror_url_var.get()
        self.local_repo = Path(self.local_repo_var.get())
        
        config = {
            'mirror_url': self.mirror_url,
            'local_repo': str(self.local_repo),
            'last_updated': datetime.now().isoformat()
        }
        
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            messagebox.showinfo("Success", "Settings saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
            
    def show_status(self):
        """Show repository status"""
        self.status_text.delete('1.0', tk.END)
        
        status_info = f"""Repository Status
================

Local Repository: {self.local_repo}
Mirror URL: {self.mirror_url}

Repository exists: {self.local_repo.exists()}
Config file exists: {self.config_file.exists()}

"""
        
        if self.local_repo.exists():
            try:
                total_size = sum(f.stat().st_size for f in self.local_repo.rglob('*') if f.is_file())
                status_info += f"Repository size: {total_size / (1024**2):.2f} MB\n"
                
                package_count = len(list(self.local_repo.glob('*.tar.lzma')))
                status_info += f"Downloaded packages: {package_count}\n"
            except Exception as e:
                status_info += f"Error reading repository: {e}\n"
        
        self.status_text.insert('1.0', status_info)
        
    # Main functionality
    
    def extract_packages_from_tex(self, tex_file):
        """Extract package names from .tex file"""
        packages = set()
        
        try:
            with open(tex_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Remove comments
            lines = content.split('\n')
            cleaned_lines = []
            for line in lines:
                comment_pos = -1
                i = 0
                while i < len(line):
                    if line[i] == '%' and (i == 0 or line[i-1] != '\\'):
                        comment_pos = i
                        break
                    i += 1
                
                if comment_pos >= 0:
                    cleaned_lines.append(line[:comment_pos])
                else:
                    cleaned_lines.append(line)
            
            content = '\n'.join(cleaned_lines)
            
            # Extract packages
            patterns = [
                r'\\usepackage(?:\[.*?\])?\{([^}]+)\}',
                r'\\RequirePackage(?:\[.*?\])?\{([^}]+)\}'
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    for pkg in match.split(','):
                        pkg = pkg.strip()
                        if pkg:
                            packages.add(pkg)
            
            return packages
            
        except Exception as e:
            self.log(f"Error reading file: {e}", self.compile_output)
            return set()
    
    def check_package_installed(self, package):
        """Check if package is installed"""
        try:
            result = subprocess.run(
                ['kpsewhich', f'{package}.sty'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0 and result.stdout.strip()
        except:
            return False
    
    def fetch_package(self, package_name):
        """Fetch a single package"""
        try:
            if not package_name.endswith('.tar.lzma'):
                package_name = f"{package_name}.tar.lzma"
            
            url = self.mirror_url + package_name
            local_path = self.local_repo / package_name
            
            self.log(f"Downloading {package_name}...", self.fetch_output)
            
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.log(f"✓ Successfully downloaded {package_name}", self.fetch_output)
            return True
            
        except Exception as e:
            self.log(f"✗ Failed to download {package_name}: {e}", self.fetch_output)
            return False
    
    def compile_latex(self, tex_file, compiler="pdflatex"):
        """Compile LaTeX document and return missing packages"""
        try:
            self.log(f"Compiling with {compiler}...", self.compile_output)
            
            result = subprocess.run(
                [compiler, '-interaction=nonstopmode', tex_file],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=Path(tex_file).parent
            )
            
            # Parse output for missing packages
            missing_packages = set()
            
            # Pattern 1: ! LaTeX Error: File `package.sty' not found
            pattern1 = r"File `([^']+\.sty)' not found"
            matches1 = re.findall(pattern1, result.stdout + result.stderr)
            for match in matches1:
                pkg = match.replace('.sty', '')
                missing_packages.add(pkg)
            
            # Pattern 2: ! Package X Error
            pattern2 = r"! Package (\w+) Error"
            matches2 = re.findall(pattern2, result.stdout + result.stderr)
            missing_packages.update(matches2)
            
            # Log output
            self.log("Compilation output:", self.compile_output)
            self.compile_output.insert(tk.END, result.stdout)
            self.compile_output.insert(tk.END, result.stderr)
            
            if result.returncode == 0:
                self.log("✓ Compilation successful!", self.compile_output)
                return True, missing_packages
            else:
                self.log("✗ Compilation failed", self.compile_output)
                return False, missing_packages
                
        except subprocess.TimeoutExpired:
            self.log("✗ Compilation timeout", self.compile_output)
            return False, set()
        except Exception as e:
            self.log(f"✗ Compilation error: {e}", self.compile_output)
            return False, set()
    
    # Button handlers
    
    def check_packages(self):
        """Check packages in .tex file"""
        tex_file = self.tex_file_var.get()
        if not tex_file:
            messagebox.showwarning("Warning", "Please select a .tex file first")
            return
        
        self.compile_output.delete('1.0', tk.END)
        self.log("Checking packages...", self.compile_output)
        
        packages = self.extract_packages_from_tex(tex_file)
        
        if not packages:
            self.log("No packages found in file", self.compile_output)
            return
        
        self.log(f"Found {len(packages)} packages:", self.compile_output)
        
        missing = []
        for pkg in sorted(packages):
            if self.check_package_installed(pkg):
                self.log(f"  ✓ {pkg} - installed", self.compile_output)
            else:
                self.log(f"  ✗ {pkg} - NOT INSTALLED", self.compile_output)
                missing.append(pkg)
        
        if missing:
            self.log(f"\n{len(missing)} packages need to be installed", self.compile_output)
        else:
            self.log("\nAll packages are installed!", self.compile_output)
    
    def fetch_missing_packages(self):
        """Fetch missing packages"""
        tex_file = self.tex_file_var.get()
        if not tex_file:
            messagebox.showwarning("Warning", "Please select a .tex file first")
            return
        
        self.compile_output.delete('1.0', tk.END)
        self.log("Fetching missing packages...", self.compile_output)
        
        packages = self.extract_packages_from_tex(tex_file)
        missing = [pkg for pkg in packages if not self.check_package_installed(pkg)]
        
        if not missing:
            self.log("All packages are already installed!", self.compile_output)
            return
        
        self.log(f"Fetching {len(missing)} packages...", self.compile_output)
        
        success = 0
        for pkg in missing:
            if self.fetch_package(pkg):
                success += 1
        
        self.log(f"\nFetched {success}/{len(missing)} packages", self.compile_output)
    
    def compile_document(self):
        """Compile document"""
        tex_file = self.tex_file_var.get()
        if not tex_file:
            messagebox.showwarning("Warning", "Please select a .tex file first")
            return
        
        self.compile_output.delete('1.0', tk.END)
        compiler = self.compiler_var.get()
        
        success, missing = self.compile_latex(tex_file, compiler)
        
        if missing:
            self.log(f"\nMissing packages detected: {', '.join(missing)}", self.compile_output)
    
    def fetch_and_compile(self):
        """Fetch missing packages and compile (with retry)"""
        tex_file = self.tex_file_var.get()
        if not tex_file:
            messagebox.showwarning("Warning", "Please select a .tex file first")
            return
        
        self.compile_output.delete('1.0', tk.END)
        compiler = self.compiler_var.get()
        
        max_iterations = 10
        for iteration in range(max_iterations):
            self.log(f"\n=== Iteration {iteration + 1}/{max_iterations} ===", self.compile_output)
            
            # Try to compile
            success, missing = self.compile_latex(tex_file, compiler)
            
            if success:
                self.log("\n✓ Compilation successful!", self.compile_output)
                messagebox.showinfo("Success", "Document compiled successfully!")
                return
            
            if not missing:
                self.log("\n✗ Compilation failed but no missing packages detected", self.compile_output)
                break
            
            # Fetch missing packages
            self.log(f"\nFetching {len(missing)} missing packages...", self.compile_output)
            for pkg in missing:
                self.fetch_package(pkg)
        
        self.log("\n✗ Could not compile after fetching packages", self.compile_output)
        messagebox.showwarning("Warning", "Compilation failed. Check the output for details.")
    
    def fetch_single_package(self):
        """Fetch single package"""
        package = self.package_var.get().strip()
        if not package:
            messagebox.showwarning("Warning", "Please enter a package name")
            return
        
        self.fetch_output.delete('1.0', tk.END)
        self.fetch_package(package)
    
    def fetch_batch_packages(self):
        """Fetch batch packages"""
        packages_text = self.batch_packages.get('1.0', tk.END).strip()
        if not packages_text:
            messagebox.showwarning("Warning", "Please enter package names")
            return
        
        packages = [p.strip() for p in packages_text.split('\n') if p.strip()]
        
        self.fetch_output.delete('1.0', tk.END)
        self.log(f"Fetching {len(packages)} packages...", self.fetch_output)
        
        success = 0
        for pkg in packages:
            if self.fetch_package(pkg):
                success += 1
        
        self.log(f"\nFetched {success}/{len(packages)} packages", self.fetch_output)
    
    def list_installed_packages(self):
        """List installed packages"""
        self.update_output.delete('1.0', tk.END)
        self.log("Listing installed packages...", self.update_output)
        
        try:
            result = subprocess.run(
                ['mpm', '--list'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                self.update_output.insert(tk.END, result.stdout)
            else:
                self.log("Could not list packages", self.update_output)
                
        except Exception as e:
            self.log(f"Error: {e}", self.update_output)
    
    def update_all_packages(self):
        """Update all packages"""
        if not messagebox.askyesno("Confirm", "Update all installed packages? This may take a while."):
            return
        
        self.update_output.delete('1.0', tk.END)
        self.log("Updating packages...", self.update_output)
        
        # This would call the update script
        messagebox.showinfo("Info", "Update functionality - use command line for now")
    
    def sync_metadata(self):
        """Sync repository metadata"""
        self.update_output.delete('1.0', tk.END)
        self.log("Syncing metadata...", self.update_output)
        
        metadata_files = [
            "miktex-zzdb1-2.9.tar.lzma",
            "miktex-zzdb2-2.9.tar.lzma",
            "miktex-zzdb3-2.9.tar.lzma",
            "pr.ini"
        ]
        
        success = 0
        for file in metadata_files:
            if self.fetch_package(file.replace('.tar.lzma', '')):
                success += 1
        
        self.log(f"\nSynced {success}/{len(metadata_files)} metadata files", self.update_output)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = MiKTeXProxyGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
