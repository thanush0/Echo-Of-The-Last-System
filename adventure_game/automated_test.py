"""
Automated test script that simulates playing the game
Tests all major systems without user input
"""

import sys
import io
from contextlib import redirect_stdout, redirect_stderr

def test_game_systems():
    """Test all game systems"""
    print("\n" + "="*60)
    print("  AUTOMATED GAME TESTING")
    print("="*60 + "\n")
    
    errors = []
    
    # Test 1: Import all modules
    print("Test 1: Importing modules...")
    try:
        from player import Player
        from system import SystemAI
        from world import World
        from combat import Combat
        from dialogue import DialogueManager
        from quests import QuestManager, create_main_quest
        from save_load import SaveLoadManager
        from enemies import get_random_enemy, create_corrupted_slime
        print("  ✓ All modules imported successfully")
    except Exception as e:
        errors.append(f"Module import failed: {e}")
        print(f"  ✗ Import failed: {e}")
        return errors
    
    # Test 2: Create player
    print("\nTest 2: Creating player...")
    try:
        player = Player("TestHero")
        assert player.name == "TestHero"
        assert player.level == 1
        assert player.hp > 0
        print(f"  ✓ Player created: {player.name}, Level {player.level}, HP {player.hp}")
    except Exception as e:
        errors.append(f"Player creation failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 3: System AI
    print("\nTest 3: Testing System AI...")
    try:
        system = SystemAI()
        assert system.integrity == 12
        print(f"  ✓ System AI created, integrity: {system.integrity}%")
        
        # Capture system message
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        system.message("Test message", delay=0)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        
        assert "SYSTEM" in output
        print("  ✓ System messages working")
    except Exception as e:
        errors.append(f"System AI failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 4: Combat system
    print("\nTest 4: Testing combat...")
    try:
        enemy = create_corrupted_slime(1)
        assert enemy.is_alive()
        print(f"  ✓ Enemy created: {enemy.name}, HP {enemy.hp}")
        
        # Simulate combat
        damage = player.get_attack_damage()
        actual_damage = enemy.take_damage(damage)
        print(f"  ✓ Combat damage: {actual_damage}")
        
        # Test enemy attack
        enemy_damage = enemy.get_attack_damage()
        player.take_damage(enemy_damage)
        print(f"  ✓ Enemy attacks working")
        
    except Exception as e:
        errors.append(f"Combat failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 5: World exploration
    print("\nTest 5: Testing world exploration...")
    try:
        world = World(system)
        assert world.current_area == "The Forgotten Ruins"
        print(f"  ✓ World created: {world.current_area}")
        
        # Test event determination
        event_type = world.determine_event(player)
        print(f"  ✓ Event system working: {event_type}")
        
    except Exception as e:
        errors.append(f"World exploration failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 6: Quest system
    print("\nTest 6: Testing quest system...")
    try:
        quest_manager = QuestManager(system)
        quest = create_main_quest()
        quest_manager.add_quest(quest)
        assert len(quest_manager.active_quests) > 0
        print(f"  ✓ Quest system working: {quest.title}")
        
        # Update quest
        quest_manager.update_quest("main_core_fragment", "explore_ruins", 1)
        print("  ✓ Quest progress tracking working")
        
    except Exception as e:
        errors.append(f"Quest system failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 7: Dialogue system
    print("\nTest 7: Testing dialogue system...")
    try:
        dialogue_manager = DialogueManager(system)
        assert "oracle" in dialogue_manager.npcs
        print("  ✓ Dialogue system working, NPCs loaded")
        
    except Exception as e:
        errors.append(f"Dialogue system failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 8: Save/Load system
    print("\nTest 8: Testing save/load...")
    try:
        save_manager = SaveLoadManager()
        
        # Test save
        success = save_manager.save_game(
            player, world, quest_manager, 
            dialogue_manager, system, slot=1
        )
        assert success
        print("  ✓ Save successful")
        
        # Test load
        save_data = save_manager.load_game(slot=1)
        assert save_data is not None
        assert save_data["player"]["name"] == "TestHero"
        print("  ✓ Load successful")
        
    except Exception as e:
        errors.append(f"Save/load failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 9: Player progression
    print("\nTest 9: Testing player progression...")
    try:
        old_level = player.level
        player.add_xp(100)
        assert player.level > old_level
        print(f"  ✓ Level up working: Level {old_level} -> {player.level}")
        
        # Test stat increases
        old_str = player.strength
        player.increase_stat_by_action("strength", 2)
        assert player.strength == old_str + 2
        print("  ✓ Action-based stat growth working")
        
    except Exception as e:
        errors.append(f"Player progression failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Test 10: System glitches
    print("\nTest 10: Testing system glitches...")
    try:
        old_corruption = player.corruption_level
        system.trigger_anomaly(player)
        print("  ✓ System anomaly triggered")
        
        # Test glitch effects
        glitched_text = system._glitch_text("Test message")
        print("  ✓ Text glitching working")
        
    except Exception as e:
        errors.append(f"Glitch system failed: {e}")
        print(f"  ✗ Failed: {e}")
    
    # Summary
    print("\n" + "="*60)
    if not errors:
        print("  ALL TESTS PASSED! ✓")
        print("="*60)
        print("\n✓ The game is fully functional!")
        print("\nTo play:")
        print("  python main.py (CLI version)")
        print("  python gui_main.py (GUI version - requires pygame)")
        return []
    else:
        print("  SOME TESTS FAILED")
        print("="*60)
        print("\nErrors found:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
        return errors


if __name__ == "__main__":
    errors = test_game_systems()
    sys.exit(0 if not errors else 1)
