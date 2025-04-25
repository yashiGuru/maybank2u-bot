# 🛠️ Build Instructions: Create Executable (.exe) from Python Script

This guide walks you through the steps to build a standalone Windows executable file (`.exe`) for the `maybank_bot.py` project using PyInstaller.

---

## ✅ Step 1: Install PyInstaller

Open your terminal or PowerShell and run:

```bash
py -m pip install pyinstaller
```

## Step 2: Clean Up Old Build Files

Remove unnecessary compiled files to avoid conflicts:

```bash
Get-ChildItem -Recurse -Include *.pyc, __pycache__ | Remove-Item -Force -Recurse
```

## ⚙️ Step 3: Build the Executable

Run either of the following commands:

### Basic Build

```bash
py -m PyInstaller --onefile maybank_bot.py
```

### Advanced Build (Recommended)

This includes assets and a custom app name:

```bash
py -m PyInstaller --onefile maybank_bot.py || py -m PyInstaller --onefile --name=maybankApp --add-data "settings.json;." --add-data "im_account_tool.png;." --add-data "im_captcha.png;." --add-data "im_login_green.png;." --add-data "im_login_yellow.png;." --add-data "im_logout_black.png;." --add-data "im_ok_green.png;." maybank_bot.py
```

### Note: On PowerShell, use backticks (`) for line continuation, and on CMD use ^.

## 📂 Step 4: Copy Required Files

Manually copy the following into the dist folder (next to maybankApp.exe):

-   settings.json
-   im_account_tool.png
-   im_captcha.png
-   im_login_green.png
-   im_login_yellow.png
-   im_logout_black.png
-   im_ok_green.png

## 🚀 Step 5: Run the App

Navigate to the dist folder and double-click maybankApp.exe to run the application.
