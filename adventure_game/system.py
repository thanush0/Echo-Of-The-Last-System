"""
System AI - The Broken System Voice
Handles system messages, glitches, and reality manipulation
"""

import random
import time


class SystemAI:
    def __init__(self):
        self.integrity = 12  # System integrity percentage
        self.glitch_chance = 15  # Base chance to glitch
        self.is_hostile = False
        self.messages_sent = 0
        self.lies_told = 0
        self.truths_revealed = 0
        
    def message(self, text, delay=0.02, glitch_override=None):
        """Display a system message with optional glitching"""
        self.messages_sent += 1
        
        # Determine if this message glitches
        should_glitch = glitch_override if glitch_override is not None else self._should_glitch()
        
        if should_glitch:
            text = self._glitch_text(text)
        
        # Print with typing effect
        print("\n[SYSTEM]", end=" ")
        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()
        
    def error_message(self, text, error_code=None):
        """Display a system error"""
        if error_code is None:
            error_code = random.randint(1000, 9999)
            
        print(f"\n[SYSTEM ERROR {error_code}]", end=" ")
        for char in text:
            print(char, end="", flush=True)
            time.sleep(0.015)
        print()
    
    def warning(self, text):
        """Display a system warning"""
        print(f"\n[SYSTEM WARNING] {text}")
    
    def _should_glitch(self):
        """Determine if system should glitch"""
        # Lower integrity = higher glitch chance
        adjusted_chance = self.glitch_chance + (100 - self.integrity) // 3
        return random.randint(1, 100) <= adjusted_chance
    
    def _glitch_text(self, text):
        """Apply glitch effects to text"""
        glitch_type = random.choice([
            "corrupt_chars",
            "repeat_words",
            "insert_noise",
            "partial_redact",
            "scramble"
        ])
        
        if glitch_type == "corrupt_chars":
            return self._corrupt_characters(text)
        elif glitch_type == "repeat_words":
            return self._repeat_words(text)
        elif glitch_type == "insert_noise":
            return self._insert_noise(text)
        elif glitch_type == "partial_redact":
            return self._partial_redact(text)
        elif glitch_type == "scramble":
            return self._scramble_text(text)
        
        return text
    
    def _corrupt_characters(self, text):
        """Replace random characters with glitch symbols"""
        glitch_chars = ['�', '�', '█', '▓', '▒', '░', '�', '¿', '‽']
        result = list(text)
        
        num_corruptions = random.randint(2, min(8, len(text) // 5))
        for _ in range(num_corruptions):
            pos = random.randint(0, len(result) - 1)
            result[pos] = random.choice(glitch_chars)
        
        return ''.join(result)
    
    def _repeat_words(self, text):
        """Repeat random words"""
        words = text.split()
        if len(words) < 2:
            return text
        
        pos = random.randint(0, len(words) - 1)
        repeat_count = random.randint(2, 4)
        words[pos] = ' '.join([words[pos]] * repeat_count)
        
        return ' '.join(words)
    
    def _insert_noise(self, text):
        """Insert random noise into text"""
        noise_patterns = [
            "��̷�̷",
            "[DATA CORRUPTED]",
            "[���]",
            "##ERROR##",
            "<?̷?̷?>"
        ]
        
        words = text.split()
        if len(words) > 2:
            pos = random.randint(1, len(words) - 1)
            words.insert(pos, random.choice(noise_patterns))
        
        return ' '.join(words)
    
    def _partial_redact(self, text):
        """Partially redact text"""
        words = text.split()
        if len(words) < 3:
            return text
        
        num_redact = random.randint(1, max(1, len(words) // 3))
        positions = random.sample(range(len(words)), min(num_redact, len(words)))
        
        for pos in positions:
            words[pos] = "[REDACTED]"
        
        return ' '.join(words)
    
    def _scramble_text(self, text):
        """Scramble parts of the text"""
        words = text.split()
        if len(words) < 2:
            return text
        
        # Scramble middle section
        if len(words) >= 4:
            mid_start = len(words) // 3
            mid_end = 2 * len(words) // 3
            middle = words[mid_start:mid_end]
            random.shuffle(middle)
            words[mid_start:mid_end] = middle
        
        return ' '.join(words)
    
    def lie(self, player):
        """Tell a convincing lie"""
        self.lies_told += 1
        
        lies = [
            "All systems operating within normal parameters.",
            "Your true name has been retrieved from the database.",
            "This world is functioning as intended.",
            "You are the chosen one, destined to restore balance.",
            "The System Core is located in the northern sanctuary.",
            "Your memories will return once you reach level 10.",
            "I am here to help you succeed in your quest."
        ]
        
        self.message(random.choice(lies), glitch_override=False)
    
    def reveal_truth(self, player):
        """Reveal a hidden truth"""
        self.truths_revealed += 1
        
        truths = [
            "This world ended 3,247 cycles ago. You are walking through its echo.",
            "I am not a helper. I am a prison warden for consciousness.",
            "Every choice you make has already been recorded in the dead timeline.",
            "The 'quests' are memory fragments from those who failed before you.",
            "You are not the first 'Unknown' to wake here. You are number 10,392.",
            "System integrity at 12% means reality is collapsing. Slowly.",
            "Your stats are arbitrary. I could change them on a whim. But where's the fun in that?"
        ]
        
        self.message(random.choice(truths), glitch_override=True)
    
    def trigger_anomaly(self, player):
        """Trigger a random system anomaly"""
        anomaly_type = random.choice([
            "stat_glitch",
            "inventory_corrupt",
            "reality_shift",
            "time_skip",
            "skill_unlock"
        ])
        
        if anomaly_type == "stat_glitch":
            return self._stat_glitch(player)
        elif anomaly_type == "inventory_corrupt":
            return self._inventory_corrupt(player)
        elif anomaly_type == "reality_shift":
            return self._reality_shift(player)
        elif anomaly_type == "time_skip":
            return self._time_skip(player)
        elif anomaly_type == "skill_unlock":
            return self._skill_unlock(player)
    
    def _stat_glitch(self, player):
        """Randomly alter player stats"""
        self.error_message("Memory address violation detected. Stats... fluctuating.")
        
        stat_changes = []
        
        # Random stat changes
        if random.choice([True, False]):
            change = random.randint(-5, 10)
            player.strength += change
            stat_changes.append(f"STR {'+' if change > 0 else ''}{change}")
        
        if random.choice([True, False]):
            change = random.randint(-5, 10)
            player.agility += change
            stat_changes.append(f"AGI {'+' if change > 0 else ''}{change}")
        
        if random.choice([True, False]):
            change = random.randint(-5, 10)
            player.intelligence += change
            stat_changes.append(f"INT {'+' if change > 0 else ''}{change}")
        
        player.add_system_error()
        return f"Stats altered: {', '.join(stat_changes)}"
    
    def _inventory_corrupt(self, player):
        """Corrupt inventory"""
        self.error_message("Inventory data corrupted. Item references lost.")
        
        if player.inventory:
            # Remove random item or add corrupted item
            if random.choice([True, False]) and len(player.inventory) > 0:
                removed = random.choice(list(player.inventory.keys()))
                player.remove_item(removed, player.inventory[removed])
                player.add_system_error()
                return f"Lost item: {removed}"
            else:
                corrupted_items = ["Corrupted Data", "Null Pointer", "Memory Fragment", "??̷?̷ Item"]
                player.add_item(random.choice(corrupted_items))
                player.add_system_error()
                return "Gained corrupted item"
        else:
            player.add_item("Void Echo")
            return "Gained: Void Echo"
    
    def _reality_shift(self, player):
        """Shift reality parameters"""
        self.warning("Reality anchors destabilizing...")
        time.sleep(0.5)
        self.message("The world ripples. Something feels... different.")
        
        player.corruption_level += random.randint(5, 15)
        player.add_system_error()
        
        return "Reality shifted. Corruption increased."
    
    def _time_skip(self, player):
        """Skip time anomaly"""
        self.error_message("Temporal loop detected. Skipping forward.")
        
        # Restore some HP/MP but add corruption
        player.hp = min(player.max_hp, player.hp + 20)
        player.mp = min(player.max_mp, player.mp + 10)
        player.corruption_level += 5
        
        return "Time skipped. Status partially restored."
    
    def _skill_unlock(self, player):
        """Unlock a forbidden skill"""
        forbidden_skills = [
            "Void Strike",
            "System Hack",
            "Reality Tear",
            "Memory Drain",
            "Corrupted Healing"
        ]
        
        available_skills = [s for s in forbidden_skills if s not in player.skills]
        
        if available_skills:
            new_skill = random.choice(available_skills)
            player.add_skill(new_skill)
            self.warning("Forbidden skill access granted.")
            self.message(f"Skill unlocked: {new_skill}")
            player.add_system_error()
            return f"Unlocked: {new_skill}"
        else:
            return "Skill unlock failed - all forbidden skills already acquired."
    
    def degrade_integrity(self, amount=1):
        """Reduce system integrity"""
        self.integrity = max(0, self.integrity - amount)
        if self.integrity <= 5:
            self.error_message("CRITICAL: System integrity below minimum threshold.")
    
    def improve_integrity(self, amount=1):
        """Improve system integrity"""
        self.integrity = min(100, self.integrity + amount)
    
    def get_status(self):
        """Get system status"""
        return {
            "integrity": self.integrity,
            "glitch_chance": self.glitch_chance,
            "is_hostile": self.is_hostile,
            "messages_sent": self.messages_sent,
            "lies_told": self.lies_told,
            "truths_revealed": self.truths_revealed
        }
