Echo of the Last System - Assets

This game can run with NO assets installed.
Images and voice are optional, layered on top of the existing text-driven game.

Directory structure:
  adventure_game/assets/
    scenes/
      title.png
      opening.png
      forgotten_ruins.png
      nexus_hub.png
      data_crypt.png
      memory_canyon.png
      core_chamber.png
      combat_default.png
      glitch_event.png

    characters/
      player.png
      oracle.png
      glitch.png
      virus.png
      firewall.png
      corrupted_ai.png
      system_warden.png

    enemies/   (optional category if you want separate enemy art)
    ui/        (optional overlays)

Notes:
- Preferred format: PNG. JPG/JPEG/GIF will also load.
- Missing images are handled gracefully (the GUI will simply show no image).
- For Tkinter display, images are resized automatically by the AssetManager.

Voice (offline TTS):
- Install: pip install pyttsx3
- Voice is optional and can be toggled in the GUI via the 'Voice narration' checkbox.
- No internet connection is required.
