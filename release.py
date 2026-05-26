import os
import sys
import re
import json
import subprocess

def run_cmd(cmd, shell=True):
    print(f"\n> Executing: {cmd}")
    res = subprocess.run(cmd, shell=shell)
    if res.returncode != 0:
        print(f"[-] Command failed with exit code: {res.returncode}")
        return False
    return True

def main():
    print("======================================================")
    # Get current version from main.py
    if not os.path.exists("main.py"):
        print("[-] main.py not found. Please run this script in the root directory.")
        return
        
    with open("main.py", "r", encoding="utf-8") as f:
        main_content = f.read()
        
    match = re.search(r'VERSION\s*=\s*"([^"]+)"', main_content)
    if not match:
        print("[-] Could not parse VERSION from main.py")
        return
    old_version = match.group(1)
    print(f"[+] Current version is: {old_version}")
    
    # Prompt for new version
    new_version = input(f"Enter new version number (e.g. 1.7.1) [current: {old_version}]: ").strip()
    if not new_version:
        print("[-] Version cannot be empty.")
        return
        
    changelog = input("Enter release changelog: ").strip()
    if not changelog:
        changelog = f"Release version {new_version}."
        
    # 1. Update VERSION in main.py
    print(f"[+] Updating main.py version to: {new_version}...")
    new_main_content = re.sub(
        r'(VERSION\s*=\s*")[^"]+(")',
        rf'\g<1>{new_version}\g<2>',
        main_content
    )
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(new_main_content)
        
    # 2. Update version.json
    print("[+] Updating version.json...")
    if os.path.exists("version.json"):
        with open("version.json", "r", encoding="utf-8") as f:
            v_data = json.load(f)
    else:
        v_data = {}
        
    v_data["version"] = new_version
    v_data["download_url"] = f"https://github.com/auhsuai/Word-Pro/releases/download/v{new_version}/WordPro_Setup.exe"
    v_data["changelog"] = changelog
    
    with open("version.json", "w", encoding="utf-8") as f:
        json.dump(v_data, f, ensure_ascii=False, indent=2)
        
    # 3. Update setup.iss
    print("[+] Updating setup.iss version...")
    if os.path.exists("setup.iss"):
        with open("setup.iss", "r", encoding="utf-8") as f:
            iss_content = f.read()
        
        iss_content = re.sub(
            r'(AppVersion=).*',
            rf'\g<1>{new_version}',
            iss_content
        )
        iss_content = re.sub(
            r'(AppVerName=Word Pro ).*',
            rf'\g<1>{new_version}',
            iss_content
        )
        with open("setup.iss", "w", encoding="utf-8") as f:
            f.write(iss_content)
    else:
        print("[-] setup.iss not found. Skipping Inno Setup version bump.")

    # 4. Run PyArmor Obfuscation
    print("\n--- Step 1/3: Obfuscating source code using PyArmor ---")
    obfuscate_cmd = (
        "pyarmor gen -O obfuscated "
        "main.py logic.py auth.py data.py audio.py graph.py dialogs.py updater.py"
    )
    if not run_cmd(obfuscate_cmd):
        print("[-] PyArmor obfuscation failed. Stopping.")
        return
        
    # 5. Run PyInstaller
    print("\n--- Step 2/3: Compiling EXE using PyInstaller ---")
    pyinstaller_cmd = (
        'pyinstaller --noconfirm --onedir --windowed --icon "app_icon.ico" '
        '--name "WordPro" --paths "obfuscated" --collect-all customtkinter '
        '--collect-all ttkbootstrap --hidden-import data --hidden-import logic '
        '--hidden-import auth --hidden-import audio --hidden-import graph '
        '--hidden-import dialogs --hidden-import updater --add-data "app_icon.ico;." '
        '"obfuscated/main.py"'
    )
    if not run_cmd(pyinstaller_cmd):
        print("[-] PyInstaller compile failed. Stopping.")
        return

    # 6. Run Inno Setup Compiler
    print("\n--- Step 3/3: Compiling Setup Installer using Inno Setup ---")
    iscc_path = r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    if os.path.exists(iscc_path):
        iscc_cmd = f'"{iscc_path}" setup.iss'
        if not run_cmd(iscc_cmd):
            print("[-] Inno Setup installer compilation failed.")
            return
    else:
        print(f"[-] Inno Setup Compiler not found at: {iscc_path}. Please build setup manually.")
        
    print("\n======================================================")
    print(f"[+] BUILD SUCCESSFUL! Installer generated in Installer/WordPro_Setup.exe")
    print("======================================================")
    
    # 7. Git commit and push prompt
    push_git = input("\nDo you want to commit and push changes to GitHub? (y/n): ").strip().lower()
    if push_git == 'y':
        if not run_cmd("git add ."):
            return
        commit_msg = f"Release v{new_version}: {changelog.splitlines()[0]}"
        if not run_cmd(f'git commit -m "{commit_msg}"'):
            return
        if not run_cmd("git push"):
            return
        print("[+] GitHub repository updated successfully!")
        
    print(f"\n[!] REMINDER: Go to https://github.com/auhsuai/Word-Pro/releases")
    print(f"    Create a release with tag 'v{new_version}' and upload 'Installer/WordPro_Setup.exe'!")

if __name__ == "__main__":
    main()
