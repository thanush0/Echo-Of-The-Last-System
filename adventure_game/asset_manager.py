"""
Asset Manager Module
Handles loading and caching of images for the game.
Provides fallback mechanisms if assets are missing.
"""

import os
from pathlib import Path
from typing import Optional, Dict
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: PIL/Pillow not available. Image features disabled.")

try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class AssetManager:
    """
    Manages game assets (images) with caching and fallback support.
    
    Features:
    - Automatic image caching to avoid repeated disk reads
    - Graceful fallback if images are missing
    - Support for different image categories
    - Dynamic image resizing
    """
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize the asset manager.
        
        Args:
            base_path: Root directory for assets. Defaults to ./assets/
        """
        if base_path is None:
            # Default to assets directory next to this module
            module_dir = Path(__file__).parent
            base_path = module_dir / "assets"
        
        self.base_path = Path(base_path)
        self.image_cache: Dict[str, any] = {}  # Cache loaded images
        self.photoimage_cache: Dict[tuple, any] = {}  # Cache PhotoImage objects with size
        
        # Create default directory structure if it doesn't exist
        self._create_asset_directories()
    
    def _create_asset_directories(self):
        """Create the standard asset directory structure."""
        directories = [
            self.base_path / "scenes",
            self.base_path / "characters",
            self.base_path / "ui",
            self.base_path / "enemies"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_image_path(self, category: str, name: str, extension: str = "png") -> Optional[Path]:
        """
        Get the full path to an image file.
        
        Args:
            category: Image category (scenes, characters, ui, enemies)
            name: Image filename without extension
            extension: File extension (default: png)
        
        Returns:
            Path object if file exists, None otherwise
        """
        path = self.base_path / category / f"{name}.{extension}"
        
        # Try alternate extensions if primary not found
        if not path.exists():
            for alt_ext in ["jpg", "jpeg", "png", "gif"]:
                alt_path = self.base_path / category / f"{name}.{alt_ext}"
                if alt_path.exists():
                    return alt_path
        
        return path if path.exists() else None
    
    def load_image(self, category: str, name: str, size: Optional[tuple] = None) -> Optional[any]:
        """
        Load an image from disk with optional resizing.
        Uses PIL/Pillow for image loading.
        
        Args:
            category: Image category
            name: Image filename without extension
            size: Optional tuple (width, height) to resize image
        
        Returns:
            PIL Image object or None if not available
        """
        if not PIL_AVAILABLE:
            return None
        
        # Create cache key
        cache_key = f"{category}/{name}"
        if size:
            cache_key += f"_{size[0]}x{size[1]}"
        
        # Check cache first
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        # Load from disk
        path = self.get_image_path(category, name)
        if path is None:
            return None
        
        try:
            img = Image.open(path)
            
            # Resize if requested
            if size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Cache and return
            self.image_cache[cache_key] = img
            return img
        
        except Exception as e:
            print(f"Warning: Failed to load image {path}: {e}")
            return None
    
    def get_photoimage(self, category: str, name: str, size: Optional[tuple] = None) -> Optional[any]:
        """
        Get a Tkinter PhotoImage object ready for display.
        
        Args:
            category: Image category
            name: Image filename without extension
            size: Optional tuple (width, height) to resize image
        
        Returns:
            PhotoImage object or None if not available
        """
        if not PIL_AVAILABLE or not TKINTER_AVAILABLE:
            return None
        
        # Create cache key
        cache_key = (category, name, size)
        
        # Check PhotoImage cache
        if cache_key in self.photoimage_cache:
            return self.photoimage_cache[cache_key]
        
        # Load PIL image
        pil_img = self.load_image(category, name, size)
        if pil_img is None:
            return None
        
        try:
            # Convert to PhotoImage
            photo_img = ImageTk.PhotoImage(pil_img)
            
            # Cache and return
            self.photoimage_cache[cache_key] = photo_img
            return photo_img
        
        except Exception as e:
            print(f"Warning: Failed to create PhotoImage: {e}")
            return None
    
    def get_scene_image(self, scene_name: str, size: Optional[tuple] = None) -> Optional[any]:
        """
        Get a scene image (location, combat, event).
        
        Args:
            scene_name: Name of the scene (e.g., "nexus_hub", "combat_glitch")
            size: Optional size tuple
        
        Returns:
            PhotoImage or None
        """
        return self.get_photoimage("scenes", scene_name, size)
    
    def get_character_image(self, character_name: str, size: Optional[tuple] = None) -> Optional[any]:
        """
        Get a character portrait image.
        
        Args:
            character_name: Name of character (e.g., "oracle", "player")
            size: Optional size tuple
        
        Returns:
            PhotoImage or None
        """
        return self.get_photoimage("characters", character_name, size)
    
    def get_enemy_image(self, enemy_name: str, size: Optional[tuple] = None) -> Optional[any]:
        """
        Get an enemy image.
        
        Args:
            enemy_name: Name of enemy (e.g., "glitch", "virus", "firewall")
            size: Optional size tuple
        
        Returns:
            PhotoImage or None
        """
        return self.get_photoimage("enemies", enemy_name, size)
    
    def get_ui_image(self, ui_element: str, size: Optional[tuple] = None) -> Optional[any]:
        """
        Get a UI element image (glitch effects, overlays).
        
        Args:
            ui_element: Name of UI element
            size: Optional size tuple
        
        Returns:
            PhotoImage or None
        """
        return self.get_photoimage("ui", ui_element, size)
    
    def clear_cache(self):
        """Clear all cached images to free memory."""
        self.image_cache.clear()
        self.photoimage_cache.clear()
    
    def preload_common_assets(self, size: Optional[tuple] = None):
        """
        Preload commonly used assets into cache.
        Call this during game initialization to reduce loading delays.
        
        Args:
            size: Size to preload images at
        """
        # Common scenes
        common_scenes = [
            "nexus_hub", "data_crypt", "memory_canyon", "core_chamber",
            "combat_default", "glitch_event"
        ]
        
        # Common characters
        common_characters = ["oracle", "player"]
        
        # Common enemies
        common_enemies = ["glitch", "virus", "firewall", "corrupted_ai", "system_warden"]
        
        print("Preloading assets...")
        
        for scene in common_scenes:
            self.get_scene_image(scene, size)
        
        for char in common_characters:
            self.get_character_image(char, size)
        
        for enemy in common_enemies:
            self.get_enemy_image(enemy, size)
        
        print(f"Assets preloaded: {len(self.image_cache)} images cached")


# Singleton instance for global access
_asset_manager_instance: Optional[AssetManager] = None


def get_asset_manager() -> AssetManager:
    """
    Get the global AssetManager instance.
    Creates one if it doesn't exist.
    
    Returns:
        Global AssetManager instance
    """
    global _asset_manager_instance
    if _asset_manager_instance is None:
        _asset_manager_instance = AssetManager()
    return _asset_manager_instance


# Convenience functions for quick access
def get_scene_image(scene_name: str, size: Optional[tuple] = None) -> Optional[any]:
    """Quick access to scene images."""
    return get_asset_manager().get_scene_image(scene_name, size)


def get_character_image(character_name: str, size: Optional[tuple] = None) -> Optional[any]:
    """Quick access to character images."""
    return get_asset_manager().get_character_image(character_name, size)


def get_enemy_image(enemy_name: str, size: Optional[tuple] = None) -> Optional[any]:
    """Quick access to enemy images."""
    return get_asset_manager().get_enemy_image(enemy_name, size)


if __name__ == "__main__":
    # Test the asset manager
    print("Testing Asset Manager...")
    manager = AssetManager()
    print(f"Base path: {manager.base_path}")
    print(f"Directories created: {list(manager.base_path.iterdir())}")
