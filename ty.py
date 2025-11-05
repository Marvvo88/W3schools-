import random
import time

# Character class to hold character attributes
class Character:
    def __init__(self, name, health, attack, defense, inventory=None):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.inventory = inventory if inventory else []

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0

    def attack_enemy(self, enemy):
        damage = max(self.attack - enemy.defense, 0)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

    def heal(self, amount):
        self.health += amount
        print(f"{self.name} heals for {amount} health!")

    def show_inventory(self):
        if not self.inventory:
            print(f"{self.name} has no items in their inventory.")
        else:
            print(f"{self.name}'s Inventory: {', '.join(self.inventory)}")

# Enemy class to hold enemy attributes
class Enemy(Character):
    def __init__(self, name, health, attack, defense, loot=None):
        super().__init__(name, health, attack, defense)
        self.loot = loot if loot else []

    def drop_loot(self):
        if self.loot:
            item = random.choice(self.loot)
            print(f"{self.name} drops {item}.")
            return item
        return None

# Player class inherits from Character, but with added quest functionality
class Player(Character):
    def __init__(self, name, health, attack, defense, inventory=None, level=1, experience=0):
        super().__init__(name, health, attack, defense, inventory)
        self.level = level
        self.experience = experience

    def gain_experience(self, amount):
        self.experience += amount
        print(f"{self.name} gains {amount} experience!")
        if self.experience >= 100:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience = 0
        self.health += 20
        self.attack += 5
        self.defense += 3
        print(f"{self.name} has leveled up to level {self.level}!")
        print(f"Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}")

# Function for simulating a battle between player and enemy
def battle(player, enemy):
    print(f"\nA wild {enemy.name} appears!\n")
    while player.is_alive() and enemy.is_alive():
        print(f"{player.name}: {player.health} HP | {enemy.name}: {enemy.health} HP")
        action = input("\nWhat would you like to do? (Attack / Heal / Inventory): ").lower()
        
        if action == "attack":
            player.attack_enemy(enemy)
            if enemy.is_alive():
                enemy.attack_enemy(player)
        elif action == "heal":
            heal_amount = random.randint(10, 20)
            player.heal(heal_amount)
            enemy.attack_enemy(player)
        elif action == "inventory":
            player.show_inventory()
            item_action = input("Use an item from your inventory? (Yes / No): ").lower()
            if item_action == "yes":
                item = input("Enter item name: ")
                if item in player.inventory:
                    player.inventory.remove(item)
                    if item == "Healing Potion":
                        heal_amount = random.randint(20, 50)
                        player.heal(heal_amount)
                    print(f"{player.name} used {item}.")
                    enemy.attack_enemy(player)
                else:
                    print(f"{item} is not in your inventory.")
            else:
                enemy.attack_enemy(player)
        else:
            print("Invalid action! You lose your turn.")
            enemy.attack_enemy(player)

        time.sleep(1)

    if player.is_alive():
        print(f"\n{player.name} has defeated {enemy.name}!")
        player.gain_experience(50)
        loot = enemy.drop_loot()
        if loot:
            player.inventory.append(loot)
    else:
        print(f"\n{player.name} has been defeated by {enemy.name}.")

# Main game loop
def main():
    print("Welcome to the RPG Game!")
    
    name = input("Enter your character's name: ")
    player = Player(name=name, health=100, attack=20, defense=5)

    print(f"\n{player.name} enters the world! Level: {player.level}, Health: {player.health}, Attack: {player.attack}, Defense: {player.defense}")
    print("Your adventure begins now...\n")

    # Example enemies
    enemies = [
        Enemy("Goblin", 50, 10, 3, loot=["Healing Potion", "Rusty Sword"]),
        Enemy("Orc", 80, 15, 5, loot=["Iron Shield", "Healing Potion"]),
        Enemy("Dragon Whelp", 120, 20, 10, loot=["Dragon Scale", "Healing Potion"])
    ]

    for enemy in enemies:
        battle(player, enemy)
        if not player.is_alive():
            print("Game Over!")
            break

    if player.is_alive():
        print(f"\nCongratulations, {player.name}! You survived all battles and emerged victorious!")

if __name__ == "__main__":
    main()
