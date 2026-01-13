"""
Combat Engine - Turn-based Combat System
Handles all combat logic, turn management, and special effects
"""

import random
import time


class Combat:
    def __init__(self, player, enemy, system_ai):
        self.player = player
        self.enemy = enemy
        self.system = system_ai
        self.turn_count = 0
        self.combat_log = []
        self.player_fled = False
        
    def start_combat(self):
        """Initialize and run combat"""
        self.system.message(f"COMBAT INITIATED: {self.enemy.name} [Level {self.enemy.level}]")
        print(f"\n{'='*50}")
        print(f"  {self.enemy.name} appears!")
        print(f"  Enemy HP: {self.enemy.hp}/{self.enemy.max_hp}")
        print(f"{'='*50}\n")
        
        # Random glitch during combat start
        if random.randint(1, 100) <= 15:
            self.system.warning("Combat parameters unstable...")
            if random.choice([True, False]):
                self.enemy.glitch_evolution()
                self.system.error_message(f"{self.enemy.name} has EVOLVED!")
        
        # Main combat loop
        while self.player.is_alive() and self.enemy.is_alive() and not self.player_fled:
            self.turn_count += 1
            self.player_turn()
            
            if self.enemy.is_alive() and not self.player_fled:
                self.enemy_turn()
            
            # Random mid-combat glitch
            if self.turn_count > 3 and random.randint(1, 100) <= 10:
                self.trigger_combat_glitch()
        
        # Combat end
        return self.end_combat()
    
    def player_turn(self):
        """Handle player's turn"""
        print(f"\n--- Turn {self.turn_count} ---")
        print(f"Your HP: {self.player.hp}/{self.player.max_hp} | MP: {self.player.mp}/{self.player.max_mp}")
        print(f"Enemy HP: {self.enemy.hp}/{self.enemy.max_hp}")
        
        action = self.get_player_action()
        
        if action == "attack":
            self.player_attack()
        elif action == "analyze":
            self.player_analyze()
        elif action == "skill":
            self.player_use_skill()
        elif action == "flee":
            self.player_flee()
    
    def get_player_action(self):
        """Get player's combat action"""
        while True:
            print("\nActions:")
            print("  1. Attack")
            print("  2. Analyze (reveals enemy info)")
            print("  3. Use Skill")
            print("  4. Flee")
            
            choice = input("\nChoose action: ").strip()
            
            if choice in ["1", "attack", "a"]:
                return "attack"
            elif choice in ["2", "analyze", "an"]:
                return "analyze"
            elif choice in ["3", "skill", "s"]:
                return "skill"
            elif choice in ["4", "flee", "f"]:
                return "flee"
            else:
                print("Invalid action. Try again.")
    
    def player_attack(self):
        """Player attacks enemy"""
        damage = self.player.get_attack_damage()
        actual_damage = self.enemy.take_damage(damage)
        
        print(f"\n> You attack {self.enemy.name}!")
        print(f"  Dealt {actual_damage} damage!")
        
        # Increase strength slightly
        if random.randint(1, 100) <= 30:
            self.player.increase_stat_by_action("strength", 1)
        
        self.player.actions_taken["attacks"] += 1
        self.combat_log.append(f"Player dealt {actual_damage} damage")
        
        if not self.enemy.is_alive():
            print(f"\n*** {self.enemy.name} has been defeated! ***")
    
    def player_analyze(self):
        """Player analyzes enemy"""
        print(f"\n> Analyzing {self.enemy.name}...")
        time.sleep(0.5)
        
        info = self.enemy.analyze_info()
        
        print("\n--- Enemy Analysis ---")
        for key, value in info.items():
            print(f"  {key}: {value}")
        print("----------------------")
        
        # Increase intelligence
        if random.randint(1, 100) <= 40:
            self.player.increase_stat_by_action("intelligence", 1)
        
        self.player.actions_taken["analyzes"] += 1
        self.combat_log.append("Player analyzed enemy")
    
    def player_use_skill(self):
        """Player uses a skill"""
        if len(self.player.skills) == 0:
            print("\n> No skills available!")
            return
        
        print("\n--- Your Skills ---")
        for i, skill in enumerate(self.player.skills, 1):
            print(f"  {i}. {skill}")
        print("  0. Cancel")
        
        choice = input("\nChoose skill: ").strip()
        
        if choice == "0":
            return
        
        try:
            skill_index = int(choice) - 1
            if 0 <= skill_index < len(self.player.skills):
                skill_name = self.player.skills[skill_index]
                self.execute_skill(skill_name)
            else:
                print("Invalid skill choice.")
        except ValueError:
            print("Invalid input.")
    
    def execute_skill(self, skill_name):
        """Execute a specific skill"""
        skill_executed = False
        
        if skill_name == "Basic Attack":
            # Just a regular attack
            self.player_attack()
            skill_executed = True
            
        elif skill_name == "Void Strike":
            if self.player.use_mp(15):
                damage = int(self.player.get_attack_damage() * 1.5)
                actual_damage = self.enemy.take_damage(damage)
                print(f"\n> VOID STRIKE!")
                print(f"  Dealt {actual_damage} VOID damage!")
                self.player.corruption_level += 2
                skill_executed = True
            else:
                print("\n> Not enough MP!")
                
        elif skill_name == "System Hack":
            if self.player.use_mp(20):
                print(f"\n> Hacking enemy systems...")
                self.enemy.defense = max(0, self.enemy.defense - 5)
                self.enemy.attack = max(1, self.enemy.attack - 3)
                print(f"  Enemy stats reduced!")
                self.player.corruption_level += 5
                skill_executed = True
            else:
                print("\n> Not enough MP!")
                
        elif skill_name == "Reality Tear":
            if self.player.use_mp(25):
                damage = int(self.player.intelligence * 2)
                actual_damage = self.enemy.take_damage(damage)
                print(f"\n> REALITY TEAR!")
                print(f"  Reality itself damages the enemy: {actual_damage} damage!")
                self.system.degrade_integrity(1)
                self.player.corruption_level += 8
                skill_executed = True
            else:
                print("\n> Not enough MP!")
                
        elif skill_name == "Memory Drain":
            if self.player.use_mp(18):
                damage = self.player.intelligence
                actual_damage = self.enemy.take_damage(damage)
                heal_amount = actual_damage // 2
                self.player.heal(heal_amount)
                print(f"\n> MEMORY DRAIN!")
                print(f"  Dealt {actual_damage} damage and healed {heal_amount} HP!")
                skill_executed = True
            else:
                print("\n> Not enough MP!")
                
        elif skill_name == "Corrupted Healing":
            if self.player.use_mp(12):
                heal = random.randint(20, 40)
                self.player.heal(heal)
                print(f"\n> CORRUPTED HEALING!")
                print(f"  Healed {heal} HP... but at what cost?")
                self.player.corruption_level += 3
                skill_executed = True
            else:
                print("\n> Not enough MP!")
        
        if skill_executed:
            self.player.actions_taken["skills_used"] += 1
            self.combat_log.append(f"Player used {skill_name}")
    
    def player_flee(self):
        """Player attempts to flee"""
        flee_chance = 50 + (self.player.agility - self.enemy.level * 5)
        flee_chance = max(20, min(80, flee_chance))
        
        if random.randint(1, 100) <= flee_chance:
            print("\n> You successfully fled from combat!")
            self.player_fled = True
            self.player.actions_taken["flees"] += 1
            
            # Increase agility
            if random.randint(1, 100) <= 35:
                self.player.increase_stat_by_action("agility", 1)
        else:
            print("\n> Failed to escape!")
            
        self.combat_log.append("Player attempted to flee")
    
    def enemy_turn(self):
        """Handle enemy's turn"""
        print(f"\n> {self.enemy.name} attacks!")
        time.sleep(0.3)
        
        damage = self.enemy.get_attack_damage()
        actual_damage = self.player.take_damage(damage)
        
        print(f"  You took {actual_damage} damage!")
        print(f"  Your HP: {self.player.hp}/{self.player.max_hp}")
        
        self.combat_log.append(f"Enemy dealt {actual_damage} damage")
        
        if not self.player.is_alive():
            print("\n*** You have been defeated! ***")
    
    def trigger_combat_glitch(self):
        """Trigger a random combat glitch"""
        glitch_type = random.choice([
            "enemy_evolve",
            "stat_swap",
            "hp_drain",
            "mp_surge",
            "reality_break"
        ])
        
        if glitch_type == "enemy_evolve":
            if not self.enemy.is_glitched:
                self.system.error_message("Enemy data corrupting...")
                self.enemy.glitch_evolution()
                print(f"\n!!! {self.enemy.name} has EVOLVED !!!")
                
        elif glitch_type == "stat_swap":
            self.system.warning("Combat parameters shifting...")
            old_player_hp = self.player.hp
            old_enemy_hp = self.enemy.hp
            
            # Swap percentages
            player_percent = self.player.hp / self.player.max_hp
            enemy_percent = self.enemy.hp / self.enemy.max_hp
            
            self.player.hp = int(self.player.max_hp * enemy_percent)
            self.enemy.hp = int(self.enemy.max_hp * player_percent)
            
            print("\n!!! HP percentages swapped !!!")
            
        elif glitch_type == "hp_drain":
            drain = random.randint(5, 15)
            self.player.take_damage(drain)
            self.system.error_message(f"System drain: {drain} HP lost")
            
        elif glitch_type == "mp_surge":
            surge = random.randint(10, 20)
            self.player.restore_mp(surge)
            self.system.message(f"Energy surge: {surge} MP restored")
            
        elif glitch_type == "reality_break":
            self.system.error_message("Reality fracturing...")
            self.player.corruption_level += 10
            print("\n!!! Reality becomes unstable !!!")
        
        self.player.add_system_error()
    
    def end_combat(self):
        """End combat and return results"""
        result = {
            "victory": False,
            "fled": self.player_fled,
            "xp_gained": 0,
            "loot": None
        }
        
        if self.player_fled:
            self.system.message("Combat aborted. You live to fight another day.")
            return result
        
        if not self.player.is_alive():
            return result
        
        if not self.enemy.is_alive():
            result["victory"] = True
            result["xp_gained"] = self.enemy.xp_reward
            
            print(f"\n{'='*50}")
            print(f"  VICTORY!")
            print(f"{'='*50}")
            
            # Award XP
            leveled_up = self.player.add_xp(self.enemy.xp_reward)
            print(f"\n  Gained {self.enemy.xp_reward} XP!")
            
            if leveled_up:
                self.system.message(f"LEVEL UP! You are now level {self.player.level}!")
                print(f"\n  *** LEVEL UP! You are now Level {self.player.level}! ***")
            
            # Loot
            loot = self.enemy.get_loot()
            if loot:
                self.player.add_item(loot)
                result["loot"] = loot
                print(f"  Found: {loot}")
            
            print(f"\n{'='*50}\n")
        
        return result
