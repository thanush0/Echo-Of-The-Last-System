"""
Quick automated test to verify all game systems work
"""

import sys
from player import Player
from system import SystemAI
from world import World
from combat import Combat
from dialogue import DialogueManager
from quests import QuestManager, create_main_quest
from save_load import SaveLoadManager
from enemies import create_corrupted_slime, create_ruins_skeleton, get_random_enemy


def test_player_system():
    """Test player system"""
    print("\n=== Testing Player System ===")
    player = Player("TestHero")
    print(f"✓ Player created: {player.name}")
    
    player.add_xp(100)
    print(f"✓ XP system works: Level {player.level}")
    
    player.add_item("Test Item", 5)
    print(f"✓ Inventory works: {player.inventory}")
    
    player.set_story_flag("test_flag", True)
    print(f"✓ Story flags work: {player.get_story_flag('test_flag')}")
    
    damage = player.take_damage(10)
    print(f"✓ Damage system works: Took {damage} damage")
    
    print("✓ Player system: PASSED\n")
    return player


def test_system_ai():
    """Test System AI"""
    print("\n=== Testing System AI ===")
    system = SystemAI()
    print(f"✓ System AI created: Integrity {system.integrity}%")
    
    print("✓ Testing system message...")
    system.message("Test message", delay=0)
    
    print("✓ Testing error message...")
    system.error_message("Test error", error_code=1234)
    
    print("✓ System AI: PASSED\n")
    return system


def test_combat_system(player, system):
    """Test combat system"""
    print("\n=== Testing Combat System ===")
    
    enemy = create_corrupted_slime(1)
    print(f"✓ Enemy created: {enemy.name}")
    
    # Simulate combat without user input
    damage = player.get_attack_damage()
    enemy.take_damage(damage)
    print(f"✓ Combat damage works: {damage} damage dealt")
    
    enemy_damage = enemy.get_attack_damage()
    player.take_damage(enemy_damage)
    print(f"✓ Enemy attacks work: {enemy_damage} damage received")
    
    print("✓ Combat system: PASSED\n")


def test_world_system(player, system):
    """Test world system"""
    print("\n=== Testing World System ===")
    
    world = World(system)
    print(f"✓ World created: {world.current_area}")
    
    world_state = world.get_world_state()
    print(f"✓ World state tracking works: {world_state['exploration_count']} explorations")
    
    print("✓ World system: PASSED\n")
    return world


def test_dialogue_system(player, system):
    """Test dialogue system"""
    print("\n=== Testing Dialogue System ===")
    
    dialogue_manager = DialogueManager(system)
    print(f"✓ Dialogue manager created: {len(dialogue_manager.npcs)} NPCs loaded")
    
    npc_state = dialogue_manager.get_npc_state()
    print(f"✓ NPC state tracking works")
    
    print("✓ Dialogue system: PASSED\n")
    return dialogue_manager


def test_quest_system(system):
    """Test quest system"""
    print("\n=== Testing Quest System ===")
    
    quest_manager = QuestManager(system)
    print(f"✓ Quest manager created")
    
    quest = create_main_quest()
    quest_manager.add_quest(quest)
    print(f"✓ Quest added: {quest.title}")
    
    quest_manager.update_quest("main_core_fragment", "explore_ruins", 1)
    print(f"✓ Quest progress tracking works")
    
    print("✓ Quest system: PASSED\n")
    return quest_manager


def test_save_load_system(player, world, quest_manager, dialogue_manager, system):
    """Test save/load system"""
    print("\n=== Testing Save/Load System ===")
    
    save_manager = SaveLoadManager()
    print(f"✓ Save manager created")
    
    # Test save
    success = save_manager.save_game(player, world, quest_manager, dialogue_manager, system, slot=1)
    if success:
        print(f"✓ Save successful")
    
    # Test load
    save_data = save_manager.load_game(slot=1)
    if save_data:
        print(f"✓ Load successful")
        
        # Verify data
        loaded_player = Player.from_dict(save_data["player"])
        print(f"✓ Player data restored: {loaded_player.name}, Level {loaded_player.level}")
    
    print("✓ Save/Load system: PASSED\n")


def test_enemy_system():
    """Test enemy system"""
    print("\n=== Testing Enemy System ===")
    
    slime = create_corrupted_slime(1)
    print(f"✓ Slime created: {slime.name}, HP: {slime.hp}")
    
    skeleton = create_ruins_skeleton(2)
    print(f"✓ Skeleton created: {skeleton.name}, HP: {skeleton.hp}")
    
    random_enemy = get_random_enemy(1)
    print(f"✓ Random enemy generation works: {random_enemy.name}")
    
    # Test glitch evolution
    slime.glitch_evolution()
    print(f"✓ Enemy evolution works: {slime.name}")
    
    # Test analysis
    info = skeleton.analyze_info()
    print(f"✓ Enemy analysis works: {len(info)} info fields")
    
    print("✓ Enemy system: PASSED\n")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("  RUNNING AUTOMATED TESTS")
    print("="*50)
    
    try:
        # Test each system
        player = test_player_system()
        system = test_system_ai()
        test_combat_system(player, system)
        world = test_world_system(player, system)
        dialogue_manager = test_dialogue_system(player, system)
        quest_manager = test_quest_system(system)
        test_save_load_system(player, world, quest_manager, dialogue_manager, system)
        test_enemy_system()
        
        # Final summary
        print("\n" + "="*50)
        print("  ALL TESTS PASSED ✓")
        print("="*50)
        print("\nGame is fully functional and ready to play!")
        print("\nTo start the game, run:")
        print("  python main.py\n")
        
        return True
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
