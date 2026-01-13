"""
Build Script for Creating Standalone Executables
Creates .exe files for Windows (or equivalent for other platforms)
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and show progress"""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=False)
        print(f"\n✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} - FAILED")
        print(f"Error: {e}")
        return False

def clean_build_folders():
    """Clean up old build artifacts"""
    print("\nCleaning up old build files...")
    
    folders_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"  Removed: {folder}/")
    
    # Remove .spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            os.remove(file)
            print(f"  Removed: {file}")
    
    print("✓ Cleanup complete\n")

def build_cli_version():
    """Build CLI version executable"""
    print("\n" + "="*60)
    print("  BUILDING CLI VERSION")
    print("="*60)
    
    command = (
        'pyinstaller '
        '--onefile '
        '--name="EchoOfTheLastSystem-CLI" '
        '--icon=NONE '
        '--console '
        '--add-data="saves;saves" '
        '--hidden-import=player '
        '--hidden-import=system '
        '--hidden-import=world '
        '--hidden-import=combat '
        '--hidden-import=enemies '
        '--hidden-import=dialogue '
        '--hidden-import=quests '
        '--hidden-import=save_load '
        'main.py'
    )
    
    return run_command(command, "Building CLI executable")

def build_tkinter_version():
    """Build Tkinter GUI version executable"""
    print("\n" + "="*60)
    print("  BUILDING TKINTER GUI VERSION")
    print("="*60)
    
    command = (
        'pyinstaller '
        '--onefile '
        '--name="EchoOfTheLastSystem-GUI" '
        '--icon=NONE '
        '--windowed '
        '--add-data="saves;saves" '
        '--hidden-import=player '
        '--hidden-import=system '
        '--hidden-import=world '
        '--hidden-import=combat '
        '--hidden-import=enemies '
        '--hidden-import=dialogue '
        '--hidden-import=quests '
        '--hidden-import=save_load '
        '--hidden-import=tkinter '
        '--hidden-import=tkinter.scrolledtext '
        'gui_tkinter.py'
    )
    
    return run_command(command, "Building Tkinter GUI executable")

def create_distribution_package():
    """Create distribution folder with all necessary files"""
    print("\n" + "="*60)
    print("  CREATING DISTRIBUTION PACKAGE")
    print("="*60 + "\n")
    
    # Create distribution folder
    dist_folder = "EchoOfTheLastSystem_Distribution"
    
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    os.makedirs(os.path.join(dist_folder, "saves"))
    os.makedirs(os.path.join(dist_folder, "docs"))
    
    # Copy executables
    print("Copying executables...")
    if os.path.exists("dist/EchoOfTheLastSystem-CLI.exe"):
        shutil.copy("dist/EchoOfTheLastSystem-CLI.exe", dist_folder)
        print("  ✓ CLI executable")
    
    if os.path.exists("dist/EchoOfTheLastSystem-GUI.exe"):
        shutil.copy("dist/EchoOfTheLastSystem-GUI.exe", dist_folder)
        print("  ✓ GUI executable")
    
    # Copy documentation
    print("\nCopying documentation...")
    docs_to_copy = [
        "README.md",
        "QUICKSTART.md",
        "PLAY_NOW.md",
        "WALKTHROUGH.md",
        "README_TKINTER.md"
    ]
    
    for doc in docs_to_copy:
        if os.path.exists(doc):
            shutil.copy(doc, os.path.join(dist_folder, "docs"))
            print(f"  ✓ {doc}")
    
    # Create README for distribution
    create_distribution_readme(dist_folder)
    
    print(f"\n✓ Distribution package created: {dist_folder}/")
    
    return dist_folder

def create_distribution_readme(dist_folder):
    """Create README for distribution package"""
    readme_content = """# ECHO OF THE LAST SYSTEM - Standalone Distribution

## Quick Start

### Windows

**GUI Version (Recommended):**
Double-click: `EchoOfTheLastSystem-GUI.exe`

**CLI Version:**
Double-click: `EchoOfTheLastSystem-CLI.exe`

### What's Included

- `EchoOfTheLastSystem-GUI.exe` - Graphical interface version
- `EchoOfTheLastSystem-CLI.exe` - Classic terminal version
- `saves/` - Your save files will be stored here
- `docs/` - Complete game documentation

### First Time Playing

1. Double-click `EchoOfTheLastSystem-GUI.exe`
2. Click "NEW GAME"
3. Enjoy your adventure!

### Save Files

Your progress is automatically saved to the `saves/` folder.
You can backup this folder to preserve your saves.

### Documentation

See the `docs/` folder for:
- Complete walkthrough
- Quick start guide
- Game manual

### System Requirements

- Windows 7 or later (10/11 recommended)
- 100 MB free disk space
- 512 MB RAM
- No additional software needed!

### Troubleshooting

**Antivirus Warning:**
Some antivirus software may flag the executable. This is a false positive
because PyInstaller-created executables are sometimes flagged. The game is
safe - you can check the source code at the original repository.

**Game Won't Start:**
- Try running as administrator
- Check Windows Defender hasn't blocked it
- Ensure you extracted all files from the zip

**Save Files Not Working:**
- Make sure the `saves/` folder exists in the same directory
- Check folder permissions

### About

Echo of the Last System is a dark fantasy adventure RPG where you awaken
in a ruined world with no memories. A broken System manages reality at
12% integrity. Your choices determine the fate of this dying world.

**Features:**
- Turn-based combat
- Multiple endings (5+)
- NPC dialogue system
- Quest system (with glitches!)
- Save/load functionality
- Deep narrative

### Credits

Created as a complete, standalone adventure RPG.
No internet connection required to play.

Enjoy your journey through the broken world!

---

For more information, see the docs folder.
"""
    
    with open(os.path.join(dist_folder, "README.txt"), 'w') as f:
        f.write(readme_content)
    
    print("  ✓ Distribution README.txt")

def main():
    """Main build process"""
    print("\n" + "="*60)
    print("  ECHO OF THE LAST SYSTEM - BUILD SCRIPT")
    print("="*60)
    
    # Clean up old builds
    clean_build_folders()
    
    # Build CLI version
    cli_success = build_cli_version()
    
    # Build Tkinter GUI version
    gui_success = build_tkinter_version()
    
    # Create distribution package
    if cli_success or gui_success:
        dist_folder = create_distribution_package()
        
        print("\n" + "="*60)
        print("  BUILD COMPLETE!")
        print("="*60)
        
        if cli_success:
            print("\n✓ CLI Version: dist/EchoOfTheLastSystem-CLI.exe")
        if gui_success:
            print("✓ GUI Version: dist/EchoOfTheLastSystem-GUI.exe")
        
        print(f"\n✓ Distribution Package: {dist_folder}/")
        
        print("\n" + "="*60)
        print("  NEXT STEPS")
        print("="*60)
        print(f"\n1. Test the executables in: {dist_folder}/")
        print("2. Zip the folder for distribution")
        print("3. Share with others!")
        
        print("\n" + "="*60)
        
    else:
        print("\n" + "="*60)
        print("  BUILD FAILED")
        print("="*60)
        print("\nSome executables failed to build.")
        print("Check the error messages above.")

if __name__ == "__main__":
    main()
