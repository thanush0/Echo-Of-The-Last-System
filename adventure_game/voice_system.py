"""
Voice System Module
Provides offline text-to-speech functionality for game narration.
Supports multiple speaker profiles with different voice characteristics.
"""

import threading
import queue
from typing import Optional, Dict, Callable
from enum import Enum

# Try to import pyttsx3 (offline TTS)
try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Warning: pyttsx3 not available. Voice features disabled.")
    print("Install with: pip install pyttsx3")


class Speaker(Enum):
    """Enumeration of different speaker types with distinct voices."""
    SYSTEM = "system"
    NARRATOR = "narrator"
    ORACLE = "oracle"
    PLAYER = "player"
    ENEMY = "enemy"
    GLITCH = "glitch"


class VoiceSystem:
    """
    Manages text-to-speech output for the game.
    
    Features:
    - Offline TTS using pyttsx3
    - Multiple speaker profiles with different voice characteristics
    - Asynchronous playback (non-blocking)
    - Queue system for managing multiple speech requests
    - Global enable/disable toggle
    - Thread-safe operation
    """
    
    def __init__(self):
        """Initialize the voice system."""
        self.enabled = True
        self.tts_available = TTS_AVAILABLE
        self.engine = None
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.speech_thread = None
        self.stop_requested = False
        
        # Voice profiles for different speakers
        self.voice_profiles = self._create_voice_profiles()
        
        # Initialize TTS engine
        if self.tts_available:
            try:
                self._initialize_engine()
                # Start speech worker thread
                self._start_speech_worker()
            except Exception as e:
                print(f"Warning: Failed to initialize TTS engine: {e}")
                self.tts_available = False
    
    def _initialize_engine(self):
        """Initialize the pyttsx3 engine with default settings."""
        self.engine = pyttsx3.init()
        
        # Get available voices
        voices = self.engine.getProperty('voices')
        self.available_voices = voices
        
        # Store voice indices for different profiles
        self.male_voice_index = 0
        self.female_voice_index = 1 if len(voices) > 1 else 0
        
        # Set default properties
        self.engine.setProperty('rate', 175)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
    
    def _create_voice_profiles(self) -> Dict[Speaker, Dict]:
        """
        Create voice profiles for different speakers.
        Each profile defines voice characteristics.
        
        Returns:
            Dictionary mapping Speaker enum to profile settings
        """
        return {
            Speaker.SYSTEM: {
                'rate': 175,
                'volume': 0.85,
                'voice_index': 0,  # Male voice typically
                'pitch': 100
            },
            Speaker.NARRATOR: {
                'rate': 165,
                'volume': 0.9,
                'voice_index': 0,
                'pitch': 100
            },
            Speaker.ORACLE: {
                'rate': 150,  # Slower, more deliberate
                'volume': 0.95,
                'voice_index': 1,  # Female voice typically
                'pitch': 110
            },
            Speaker.PLAYER: {
                'rate': 180,
                'volume': 0.9,
                'voice_index': 0,
                'pitch': 105
            },
            Speaker.ENEMY: {
                'rate': 190,  # Faster, more aggressive
                'volume': 0.85,
                'voice_index': 0,
                'pitch': 90
            },
            Speaker.GLITCH: {
                'rate': 200,  # Very fast, distorted
                'volume': 0.8,
                'voice_index': 0,
                'pitch': 80
            }
        }
    
    def _apply_voice_profile(self, speaker: Speaker):
        """
        Apply voice settings for a specific speaker.
        
        Args:
            speaker: Speaker enum value
        """
        if not self.engine or speaker not in self.voice_profiles:
            return
        
        profile = self.voice_profiles[speaker]
        
        try:
            # Set rate and volume
            self.engine.setProperty('rate', profile['rate'])
            self.engine.setProperty('volume', profile['volume'])
            
            # Set voice (if available)
            if self.available_voices:
                voice_index = min(profile['voice_index'], len(self.available_voices) - 1)
                self.engine.setProperty('voice', self.available_voices[voice_index].id)
        
        except Exception as e:
            print(f"Warning: Failed to apply voice profile: {e}")
    
    def _start_speech_worker(self):
        """Start the background thread that processes speech requests."""
        if self.speech_thread is None or not self.speech_thread.is_alive():
            self.stop_requested = False
            self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
            self.speech_thread.start()
    
    def _speech_worker(self):
        """
        Background worker that processes the speech queue.
        Runs in a separate thread to avoid blocking the main UI.
        """
        while not self.stop_requested:
            try:
                # Wait for speech request (timeout to allow checking stop_requested)
                text, speaker, callback = self.speech_queue.get(timeout=0.5)
                
                if text is None:  # Poison pill to stop thread
                    break
                
                # Process the speech
                self._speak_internal(text, speaker)
                
                # Call callback if provided
                if callback:
                    callback()
                
                self.speech_queue.task_done()
            
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in speech worker: {e}")
    
    def _speak_internal(self, text: str, speaker: Speaker):
        """
        Internal method to perform actual speech synthesis.
        
        Args:
            text: Text to speak
            speaker: Speaker profile to use
        """
        if not self.engine or not text:
            return
        
        try:
            self.is_speaking = True
            
            # Apply voice profile
            self._apply_voice_profile(speaker)
            
            # Speak the text (blocking call)
            self.engine.say(text)
            self.engine.runAndWait()
            
            self.is_speaking = False
        
        except Exception as e:
            print(f"Error during speech synthesis: {e}")
            self.is_speaking = False
    
    def speak(self, text: str, speaker: Speaker = Speaker.NARRATOR,
              blocking: bool = False, callback: Optional[Callable] = None):
        """
        Speak text using the specified speaker profile.

        Notes:
        - Offline only (pyttsx3)
        - Non-blocking by default (queued on a background worker thread)
        - Long text is chunked to avoid long UI freezes and improve pacing

        Args:
            text: Text to speak
            speaker: Speaker profile to use (default: NARRATOR)
            blocking: If True, speak in the current thread (default: False)
            callback: Optional function to call when speech completes (called after final chunk)
        """
        if not self.enabled or not self.tts_available or not text:
            return

        # Clean text for better speech
        text = self._clean_text(text)
        if not text:
            return

        chunks = self._chunk_text(text, max_chars=320)

        if blocking:
            # Speak chunks immediately in current thread
            for chunk in chunks:
                self._speak_internal(chunk, speaker)
            if callback:
                callback()
        else:
            # Queue chunks for background processing. Attach callback only to final chunk.
            for i, chunk in enumerate(chunks):
                chunk_callback = callback if i == len(chunks) - 1 else None
                self.speech_queue.put((chunk, speaker, chunk_callback))
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text for better TTS output.

        Keeps this conservative: we only remove/replace things that commonly sound bad.
        """
        # Flatten newlines (engine does better with spaces)
        text = ' '.join(text.split('\n'))

        # Remove common formatting
        text = text.replace('**', '')
        text = text.replace('*', '')
        text = text.replace('_', '')

        # Remove ASCII dividers and similar UI-only lines
        stripped = text.strip()
        if stripped and all(c in "= -_~" for c in stripped):
            return ""

        # Replace common stat abbreviations
        text = text.replace('HP', 'health points')
        text = text.replace('MP', 'mana points')
        text = text.replace('ATK', 'attack')
        text = text.replace('DEF', 'defense')
        text = text.replace('SPD', 'speed')

        # Pacing tweaks
        text = text.replace('...', ', ')
        text = text.replace('..', '.')

        return text.strip()
    
    def _chunk_text(self, text: str, max_chars: int = 320) -> list[str]:
        """Split long text into smaller chunks for safer TTS playback."""
        if len(text) <= max_chars:
            return [text]

        # Basic sentence splitting; keeps punctuation.
        sentences: list[str] = []
        buf = ""
        for ch in text:
            buf += ch
            if ch in ".!?":
                sentences.append(buf.strip())
                buf = ""
        if buf.strip():
            sentences.append(buf.strip())

        # If no sentence boundaries were found, hard-slice.
        if len(sentences) == 1 and len(sentences[0]) > max_chars:
            s = sentences[0]
            return [s[i:i + max_chars].strip() for i in range(0, len(s), max_chars) if s[i:i + max_chars].strip()]

        # Pack sentences into chunks.
        chunks: list[str] = []
        current = ""
        for s in sentences:
            if not current:
                current = s
                continue
            if len(current) + 1 + len(s) <= max_chars:
                current = current + " " + s
            else:
                chunks.append(current)
                current = s
        if current:
            chunks.append(current)

        return chunks

    def speak_system(self, text: str, blocking: bool = False):
        """Convenience method for system messages."""
        self.speak(text, Speaker.SYSTEM, blocking)
    
    def speak_oracle(self, text: str, blocking: bool = False):
        """Convenience method for Oracle dialogue."""
        self.speak(text, Speaker.ORACLE, blocking)
    
    def speak_enemy(self, text: str, blocking: bool = False):
        """Convenience method for enemy dialogue."""
        self.speak(text, Speaker.ENEMY, blocking)
    
    def speak_glitch(self, text: str, blocking: bool = False):
        """Convenience method for glitch events."""
        self.speak(text, Speaker.GLITCH, blocking)
    
    def speak_narrator(self, text: str, blocking: bool = False):
        """Convenience method for narrative text."""
        self.speak(text, Speaker.NARRATOR, blocking)
    
    def stop(self):
        """Stop current speech and clear queue."""
        if not self.tts_available:
            return
        
        # Clear queue
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
                self.speech_queue.task_done()
            except queue.Empty:
                break
        
        # Stop engine
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        
        self.is_speaking = False
    
    def toggle(self) -> bool:
        """
        Toggle voice on/off.
        
        Returns:
            New state (True = enabled, False = disabled)
        """
        self.enabled = not self.enabled
        if not self.enabled:
            self.stop()
        return self.enabled
    
    def set_enabled(self, enabled: bool):
        """
        Set voice enabled state.
        
        Args:
            enabled: True to enable, False to disable
        """
        self.enabled = enabled
        if not enabled:
            self.stop()
    
    def is_enabled(self) -> bool:
        """Check if voice is enabled."""
        return self.enabled and self.tts_available
    
    def is_available(self) -> bool:
        """Check if TTS is available on this system."""
        return self.tts_available
    
    def shutdown(self):
        """Clean shutdown of voice system."""
        self.stop_requested = True
        self.stop()
        
        # Send poison pill to stop worker thread
        self.speech_queue.put((None, None, None))
        
        if self.speech_thread and self.speech_thread.is_alive():
            self.speech_thread.join(timeout=2.0)


# Singleton instance for global access
_voice_system_instance: Optional[VoiceSystem] = None


def get_voice_system() -> VoiceSystem:
    """
    Get the global VoiceSystem instance.
    Creates one if it doesn't exist.
    
    Returns:
        Global VoiceSystem instance
    """
    global _voice_system_instance
    if _voice_system_instance is None:
        _voice_system_instance = VoiceSystem()
    return _voice_system_instance


# Convenience functions for quick access
def speak(text: str, speaker: Speaker = Speaker.NARRATOR):
    """Quick access to speak function."""
    get_voice_system().speak(text, speaker)


def speak_oracle(text: str):
    """Quick access to Oracle speech."""
    get_voice_system().speak_oracle(text)


def speak_system(text: str):
    """Quick access to system speech."""
    get_voice_system().speak_system(text)


def toggle_voice() -> bool:
    """Quick access to toggle voice."""
    return get_voice_system().toggle()


def is_voice_enabled() -> bool:
    """Quick access to check if voice is enabled."""
    return get_voice_system().is_enabled()


if __name__ == "__main__":
    # Test the voice system
    print("Testing Voice System...")
    voice = VoiceSystem()
    
    if voice.is_available():
        print("Voice system available!")
        print("\nTesting different speakers...")
        
        voice.speak_system("System initialized.", blocking=True)
        voice.speak_narrator("Welcome to the Echo of the Last System.", blocking=True)
        voice.speak_oracle("I am the Oracle. I can guide you through this digital realm.", blocking=True)
        
        print("\nVoice test complete!")
    else:
        print("Voice system not available. Install pyttsx3 to enable.")
