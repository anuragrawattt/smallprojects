import random
import copy
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

# ==================== LORE / STORY TEXT ====================

LORE_TEXT = (
    "The Shattered Crown\n"
    "--------------------\n"
    "Long ago, King Vaelion sought to cheat death with the Rite of Shattering—"
    "a forbidden spell to split his soul among primal beings. His fire became the Firebird, "
    "his shadow became the Shadow Serpent, and his will was sealed in the Ancient Dragon.\n\n"
    "The ritual backfired. Vaelion perished—but a flicker of his essence survived, trapped in a vessel that would awaken centuries later...\n\n"
    "That vessel is you.\n\n"
    "Guided by Auron—the last court mage, now a spirit—you must retrieve the three echoes of your soul, "
    "craft a mysterious key with Gorin the Blacksmith, and face the Sealed Gate. "
    "Opening it may free the world from your ancient curse—but it will cost you everything."
)

# ==================== WORLD DATA (rooms, items, spells, player) ====================

rooms = {
    "entrance": {
        "description": "The dark entrance of the dungeon. The air smells musty and cold.",
        "exits": {"north": "hallway"},
        "items": []
    },
    "hallway": {
        "description": "A dim corridor with flickering torches on the walls.",
        "exits": {"south": "entrance", "east": "armory", "west": "library", "north": "crossroads"},
        "items": []
    },
    "armory": {
        "description": "Old weapon racks filled with rusty swords and shields.",
        "exits": {"west": "hallway", "east": "forge"},
        "items": ["rusty sword", "wooden shield"]
    },
    "forge": {
        "description": "The forge room with an anvil and glowing coals. You feel you could craft something here.",
        "exits": {"west": "armory", "north": "blacksmith_shop"},
        "items": []
    },
    "blacksmith_shop": {
        "description": "A friendly blacksmith is here, hammering on a sword.",
        "exits": {"south": "forge"},
        "items": [],
        "npc": {
            "name": "Gorin the Blacksmith",
            "quest_given": False,
            "quest_completed": False,
            "first_reward_given": False,
            "key_crafted": False
        }
    },
    "library": {
        "description": "Shelves filled with dusty books and scrolls.",
        "exits": {"east": "hallway", "north": "wizard_tower_entrance"},
        "items": ["spellbook"]
    },
    "wizard_tower_entrance": {
        "description": "A spiral staircase leads up the wizard's tower.",
        "exits": {"south": "library", "up": "wizard_tower_top", "west": "underground_lake"},
        "items": []
    },
    "wizard_tower_top": {
        "description": "The top of the wizard's tower, glowing with magical energy. A soft, shimmering presence lingers.",
        "exits": {"down": "wizard_tower_entrance", "north": "phoenix_nest"},
        "items": [],
        "npc": {
            "name": "Auron the Spirit Mage",
            "spells_given": False,
            "wand_given": False
        }
    },
    "crossroads": {
        "description": "A crossroad with paths in all directions.",
        "exits": {"south": "hallway", "north": "goblin_den", "east": "treasure_room", "west": "prison"},
        "items": []
    },
    "goblin_den": {
        "description": "A foul-smelling den inhabited by goblins.",
        "exits": {"south": "crossroads"},
        "items": ["goblin dagger"],
        "monster": {
            "name": "Goblin Chief",
            "hp": 25,
            "attack": (5, 8),
            "drop": None
        }
    },
    "prison": {
        "description": "A cold prison cell with iron bars. A prisoner is chained here.",
        "exits": {"east": "crossroads", "south": "prisoners_quarters"},
        "items": [],
        "npc": {
            "name": "Prisoner Alaric",
            "quest_given": False,
            "quest_completed": False
        },
        # Optional: no monster here; keep it an NPC space
    },
    "treasure_room": {
        "description": "A glittering treasure room filled with gold and jewels.",
        "exits": {"west": "crossroads", "north": "trap_room"},
        "items": ["golden crown", "ruby amulet"],
        "monster": {
            "name": "Treasure Guardian",
            "hp": 30,
            "attack": (6, 10),
            "drop": None
        }
    },
    "trap_room": {
        "description": "A room full of traps. There’s a locked door to the north.",
        "exits": {"south": "treasure_room", "north": "riddle_room"},
        "items": []
    },
    "riddle_room": {
        "description": "A quiet chamber with ancient inscriptions. A stone pedestal holds a riddle.",
        "exits": {"south": "trap_room", "north": "secret_passage"},
        "items": []
    },
    "secret_passage": {
        "description": "A hidden passage behind a wall, leading deeper underground.",
        "exits": {"south": "riddle_room", "east": "dragon_lair", "west": "hidden_chamber", "north": "sealed_gate"},
        "items": []
    },
    "dragon_lair": {
        "description": "The lair of a mighty dragon. Flames flicker along the walls.",
        "exits": {"west": "secret_passage"},
        "items": [],
        "monster": {
            "name": "Ancient Dragon",
            "hp": 60,
            "attack": (10, 18),
            "drop": "dragon scale"
        }
    },
    "prisoners_quarters": {
        "description": "Living quarters for prisoners. It looks abandoned.",
        "exits": {"north": "prison"},
        "items": ["healing potion"],
        "monster": {
            "name": "Skeleton Warrior",
            "hp": 20,
            "attack": (4, 7),
            "drop": None
        }
    },
    "underground_lake": {
        "description": "A vast underground lake with a small boat dock.",
        "exits": {"east": "wizard_tower_entrance", "west": "abandoned_camp"},
        "items": []
    },
    "abandoned_camp": {
        "description": "An old adventurer’s camp, now deserted.",
        "exits": {"east": "underground_lake"},
        "items": ["fire spell scroll"],
        "monster": {
            "name": "Orc Brute",
            "hp": 24,
            "attack": (6, 9),
            "drop": None
        }
    },
    "hidden_chamber": {
        "description": "A small chamber with a hidden lever on the wall.",
        "exits": {"south": "secret_passage", "west": "shadow_cavern"},
        "items": [],
        "monster": {
            "name": "Skeleton Sentinel",
            "hp": 22,
            "attack": (5, 8),
            "drop": None
        }
    },
    "shadow_cavern": {
        "description": "A cavern swallowed by darkness; something slithers just beyond sight.",
        "exits": {"east": "hidden_chamber"},
        "items": [],
        "monster": {
            "name": "Shadow Serpent",
            "hp": 28,
            "attack": (7, 11),
            "drop": "shadow fragment"
        }
    },
    "phoenix_nest": {
        "description": "A lofty perch blazing with embers. A radiant Firebird watches you.",
        "exits": {"south": "wizard_tower_top"},
        "items": [],
        "monster": {
            "name": "Firebird",
            "hp": 32,
            "attack": (8, 12),
            "drop": "phoenix feather"
        }
    },
    "sealed_gate": {
        "description": "An immense stone door etched with runes—the Sealed Gate. A keyhole gleams faintly.",
        "exits": {"south": "secret_passage", "east": "sunlit_exit"},
        "items": []
    },
    "sunlit_exit": {
        "description": "Sunlight pours through an opening to the outside world.",
        "exits": {"west": "sealed_gate"},
        "items": []
    }
}

items_info = {
    "rusty sword": {"name": "Rusty Sword", "attack": 5, "description": "An old, rusty sword. Better than nothing."},
    "wooden shield": {"name": "Wooden Shield", "defense": 3, "description": "A worn wooden shield."},
    "goblin dagger": {"name": "Goblin Dagger", "attack": 6, "description": "A sharp, small dagger used by goblins."},
    "spellbook": {"name": "Spellbook", "description": "A book containing various spells."},
    "magic wand": {"name": "Magic Wand", "attack": 8, "description": "A wand to channel magical power."},
    "fire spell scroll": {"name": "Fire Spell Scroll", "description": "Scroll containing a fireball spell."},
    "healing potion": {"name": "Healing Potion", "heal": 20, "description": "Restores 20 HP when used."},
    "golden crown": {"name": "Golden Crown", "description": "A crown encrusted with jewels."},
    "ruby amulet": {"name": "Ruby Amulet", "description": "An amulet glowing with a red light."},
    "dragon scale": {"name": "Dragon Scale", "description": "A scale from the ancient dragon."},
    "shadow fragment": {"name": "Shadow Fragment", "description": "A shard of bound shadow, cold to the touch."},
    "phoenix feather": {"name": "Phoenix Feather", "description": "A feather that never cools."},
    "mysterious key": {"name": "Mysterious Key", "description": "Forged to open the Sealed Gate."}
}

spells = {
    "fireball": {
        "name": "Fireball",
        "damage": (12, 22),
        "mana_cost": 10,
        "description": "Throws a fiery ball that burns enemies."
    },
    "heal": {
        "name": "Heal",
        "heal": (15, 30),
        "mana_cost": 8,
        "description": "Restores health."
    },
    "ice shard": {
        "name": "Ice Shard",
        "damage": (8, 18),
        "mana_cost": 9,
        "description": "Hurls a shard of ice to pierce enemies."
    },
    "lightning bolt": {
        "name": "Lightning Bolt",
        "damage": (15, 25),
        "mana_cost": 12,
        "description": "Strikes enemies with lightning."
    }
}

player = {
    "location": "entrance",
    "hp": 60,
    "max_hp": 60,
    "mana": 40,
    "max_mana": 40,
    "attack": (4, 8),
    "defense": 3,
    "inventory": [],
    "equipped_weapon": None,
    "equipped_shield": None,
    "spells_known": ["fireball", "heal"],  # starts with 2 spells
    "quest_active": False,
    "quest_completed": False,
    "riddle_solved": False,
    "gate_unlocked": False
}

# Keep deep copies to allow restart
DEFAULT_ROOMS = copy.deepcopy(rooms)
DEFAULT_PLAYER = copy.deepcopy(player)

# ==================== GAME GUI ====================

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dungeon Adventure – The Shattered Crown")

        # Text area
        self.text_area = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, width=90, height=28, state='disabled',
            bg="#1e1e1e", fg="#d4d4d4", font=("Consolas", 12)
        )
        self.text_area.grid(row=0, column=0, columnspan=9, padx=10, pady=10)

        # Status line
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(root, textvariable=self.status_var, font=("Consolas", 12), fg="#00ff00")
        self.status_label.grid(row=1, column=0, columnspan=9, sticky="w", padx=10)

        # Direction buttons
        self.btn_north = tk.Button(root, text="Go North", width=12, command=lambda: self.process_command("go north"))
        self.btn_north.grid(row=2, column=4)

        self.btn_west = tk.Button(root, text="Go West", width=12, command=lambda: self.process_command("go west"))
        self.btn_west.grid(row=3, column=3)

        self.btn_look = tk.Button(root, text="Look", width=12, command=lambda: self.process_command("look"))
        self.btn_look.grid(row=3, column=4)

        self.btn_east = tk.Button(root, text="Go East", width=12, command=lambda: self.process_command("go east"))
        self.btn_east.grid(row=3, column=5)

        self.btn_south = tk.Button(root, text="Go South", width=12, command=lambda: self.process_command("go south"))
        self.btn_south.grid(row=4, column=4)

        # Vertical movement
        self.btn_up = tk.Button(root, text="Go Up", width=12, command=lambda: self.process_command("go up"))
        self.btn_up.grid(row=2, column=6)

        self.btn_down = tk.Button(root, text="Go Down", width=12, command=lambda: self.process_command("go down"))
        self.btn_down.grid(row=4, column=6)

        # Action row 1
        self.btn_attack = tk.Button(root, text="Attack", width=12, command=lambda: self.process_command("attack"))
        self.btn_attack.grid(row=5, column=0, padx=2, pady=6)

        self.btn_pick = tk.Button(root, text="Pick Item", width=12, command=self.pick_item_prompt)
        self.btn_pick.grid(row=5, column=1, padx=2)

        self.btn_equip = tk.Button(root, text="Equip Item", width=12, command=self.equip_item_prompt)
        self.btn_equip.grid(row=5, column=2, padx=2)

        self.btn_use = tk.Button(root, text="Use Item", width=12, command=self.use_item_prompt)
        self.btn_use.grid(row=5, column=3, padx=2)

        self.btn_cast = tk.Button(root, text="Cast Spell", width=12, command=self.cast_spell_gui)
        self.btn_cast.grid(row=5, column=4, padx=2)

        self.btn_inventory = tk.Button(root, text="Inventory", width=12, command=self.show_inventory_window)
        self.btn_inventory.grid(row=5, column=5, padx=2)

        self.btn_status = tk.Button(root, text="Status", width=12, command=self.show_status)
        self.btn_status.grid(row=5, column=6, padx=2)

        self.btn_talk = tk.Button(root, text="Talk", width=12, command=lambda: self.process_command("talk"))
        self.btn_talk.grid(row=5, column=7, padx=2)

        self.btn_lore = tk.Button(root, text="Lore", width=12, command=lambda: self.process_command("lore"))
        self.btn_lore.grid(row=5, column=8, padx=2)

        # Footer row
        self.btn_help = tk.Button(root, text="Help", width=12, command=self.show_help)
        self.btn_help.grid(row=6, column=0, padx=2, pady=8)

        self.btn_restart = tk.Button(root, text="Restart", width=12, command=self.restart_game)
        self.btn_restart.grid(row=6, column=1, padx=2)

        self.btn_quit = tk.Button(root, text="Quit", width=12, command=root.quit)
        self.btn_quit.grid(row=6, column=8, padx=2)

        self.print_text("Welcome to The Shattered Crown!\nUse the buttons to explore. For the story, press 'Lore'.", "lightgreen")
        self.look_room()
        self.update_buttons_state()
        self.show_status()
        self.check_npc_interaction()  # in case initial room has one later

    # ---------- UI Utilities ----------

    def print_text(self, text, color="white"):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        # tag last line
        try:
            end_index = self.text_area.index("end-1c linestart")
            line_index = self.text_area.index("end-2l linestart")
            self.text_area.tag_add(color, line_index, end_index)
        except Exception:
            pass
        self.text_area.tag_config(color, foreground=color)
        self.text_area.see(tk.END)
        self.text_area.configure(state='disabled')

    def update_buttons_state(self):
        current_room = rooms[player["location"]]

        # Directions
        self.btn_north.config(state=tk.NORMAL if "north" in current_room["exits"] else tk.DISABLED)
        self.btn_south.config(state=tk.NORMAL if "south" in current_room["exits"] else tk.DISABLED)
        self.btn_east.config(state=tk.NORMAL if "east" in current_room["exits"] else tk.DISABLED)
        self.btn_west.config(state=tk.NORMAL if "west" in current_room["exits"] else tk.DISABLED)
        self.btn_up.config(state=tk.NORMAL if "up" in current_room["exits"] else tk.DISABLED)
        self.btn_down.config(state=tk.NORMAL if "down" in current_room["exits"] else tk.DISABLED)

        # Attack enabled only if monster present
        can_attack = "monster" in current_room
        self.btn_attack.config(state=tk.NORMAL if can_attack else tk.DISABLED)

        # Pick item enabled only if items present
        can_pick = bool(current_room.get("items"))
        self.btn_pick.config(state=tk.NORMAL if can_pick else tk.DISABLED)

        # Equip / Use enabled if inventory not empty
        has_inventory = len(player["inventory"]) > 0
        self.btn_equip.config(state=tk.NORMAL if has_inventory else tk.DISABLED)
        self.btn_use.config(state=tk.NORMAL if has_inventory else tk.DISABLED)

        # Cast spell button enabled if player knows spell + has mana + has spellbook
        can_cast = ("spellbook" in player["inventory"]) and player["mana"] > 0 and len(player["spells_known"]) > 0
        self.btn_cast.config(state=tk.NORMAL if can_cast else tk.DISABLED)

        # Talk enabled if NPC is present
        self.btn_talk.config(state=tk.NORMAL if "npc" in current_room else tk.DISABLED)

    # ---------- Command Routing ----------

    def process_command(self, command):
        command = command.strip().lower()
        if command.startswith("go "):
            direction = command[3:]
            self.move_player(direction)
        elif command == "look":
            self.look_room()
        elif command.startswith("pick "):
            item_name = command[5:]
            self.pick_up(item_name)
        elif command == "inventory":
            self.show_inventory_window()
        elif command.startswith("equip "):
            item_name = command[6:]
            self.equip_item(item_name)
        elif command == "attack":
            self.attack_monster()
        elif command.startswith("use "):
            item_name = command[4:]
            self.use_item(item_name)
        elif command == "cast":
            self.cast_spell_gui()
        elif command == "status":
            self.show_status()
        elif command == "help":
            self.show_help()
        elif command == "talk":
            self.talk_to_npc()
        elif command == "lore":
            self.show_lore()
        else:
            self.print_text("Unknown command. Use the buttons or press 'Help'.", "red")
        self.update_buttons_state()

    # ---------- Movement & Room Display ----------

    def move_player(self, direction):
        current_room = rooms[player["location"]]

        # Special gate: riddle gate check (door to north from trap_room)
        if player["location"] == "trap_room" and direction == "north" and not player.get("riddle_solved", False):
            self.print_text("The door to the north is locked by a strange mechanism. Solve the riddle first.", "red")
            return

        # Special gate: Sealed Gate requires unlocking to pass east
        if player["location"] == "sealed_gate" and direction == "east":
            if not player.get("gate_unlocked", False):
                self.print_text("The Sealed Gate is locked. A keyhole gleams. Perhaps you should use a key here.", "red")
                return

        if direction in current_room["exits"]:
            player["location"] = current_room["exits"][direction]
            self.print_text(f"You move {direction}.")
            self.look_room()

            # Check for NPC auto-interaction prompts where relevant
            self.check_npc_interaction()

            # Reaching the final exit triggers ending
            if player["location"] == "sunlit_exit":
                self.trigger_ending()
        else:
            self.print_text("You can't go that way.", "red")

        self.update_buttons_state()
        self.show_status()

    def look_room(self):
        current_room = rooms[player["location"]]
        self.print_text("\n" + current_room["description"], "cyan")

        # Show NPCs
        if "npc" in current_room:
            npc = current_room["npc"]
            self.print_text(f"You see {npc['name']} here.", "magenta")

        # Show Items
        if current_room.get("items"):
            self.print_text("You see the following items:", "yellow")
            for item in current_room["items"]:
                desc = items_info.get(item, {}).get("description", item)
                self.print_text(f" - {item}: {desc}", "yellow")

        # Show Monster
        if "monster" in current_room:
            monster = current_room["monster"]
            self.print_text(f"A hostile {monster['name']} is here!", "red")

    # ---------- Inventory & Equipment ----------

    def pick_up(self, item_name):
        current_room = rooms[player["location"]]
        if item_name in current_room.get("items", []):
            current_room["items"].remove(item_name)
            player["inventory"].append(item_name)
            self.print_text(f"You picked up the {item_name}.", "green")
        else:
            self.print_text(f"There is no {item_name} here.", "red")
        self.show_status()
        self.update_buttons_state()

    def show_inventory_window(self):
        inv_win = tk.Toplevel(self.root)
        inv_win.title("Inventory")
        inv_win.geometry("480x360")

        tk.Label(inv_win, text="Your Inventory:", font=("Consolas", 14, "bold")).pack(pady=5)

        listbox = tk.Listbox(inv_win, font=("Consolas", 12))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10)

        for item in player["inventory"]:
            desc = items_info.get(item, {}).get("description", "")
            listbox.insert(tk.END, f"{item} - {desc}")

        def equip_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showinfo("Info", "Select an item to equip.")
                return
            item = player["inventory"][sel[0]]
            self.equip_item(item)

        def use_selected():
            sel = listbox.curselection()
            if not sel:
                messagebox.showinfo("Info", "Select an item to use.")
                return
            item = player["inventory"][sel[0]]
            self.use_item(item)

        btn_frame = tk.Frame(inv_win)
        btn_frame.pack(pady=5)

        equip_btn = tk.Button(btn_frame, text="Equip", command=equip_selected, width=12)
        equip_btn.grid(row=0, column=0, padx=5)

        use_btn = tk.Button(btn_frame, text="Use", command=use_selected, width=12)
        use_btn.grid(row=0, column=1, padx=5)

    def equip_item(self, item_name):
        if item_name not in player["inventory"]:
            self.print_text(f"You don't have {item_name} in your inventory.", "red")
            return
        if item_name not in items_info:
            self.print_text(f"{item_name} cannot be equipped.", "red")
            return

        item = items_info[item_name]
        if "attack" in item:
            player["equipped_weapon"] = item_name
            self.print_text(f"You equipped the {item_name} as your weapon.", "green")
        elif "defense" in item:
            player["equipped_shield"] = item_name
            self.print_text(f"You equipped the {item_name} as your shield.", "green")
        else:
            self.print_text(f"You cannot equip the {item_name}.", "red")
        self.show_status()

    # ---------- Combat & Spells ----------

    def attack_monster(self):
        current_room = rooms[player["location"]]
        if "monster" not in current_room:
            self.print_text("There is no monster here.", "red")
            return

        monster = current_room["monster"]

        # Animate attack textual beat
        self.animate_attack(monster["name"])

        # Player attack
        base_damage = random.randint(*player["attack"])
        weapon_bonus = items_info[player["equipped_weapon"]]["attack"] if player["equipped_weapon"] and player["equipped_weapon"] in items_info else 0
        damage = base_damage + weapon_bonus
        monster["hp"] -= damage
        self.print_text(f"You attack the {monster['name']} for {damage} damage! (Monster HP: {max(monster['hp'], 0)})", "yellow")

        if monster["hp"] <= 0:
            self.handle_monster_defeat(current_room, monster)
            return

        # Monster counterattack
        shield_def = items_info[player["equipped_shield"]]["defense"] if player["equipped_shield"] and player["equipped_shield"] in items_info else 0
        monster_damage = random.randint(*monster["attack"]) - shield_def
        monster_damage = max(0, monster_damage)
        player["hp"] -= monster_damage
        self.print_text(f"The {monster['name']} attacks you for {monster_damage} damage! (Your HP: {max(player['hp'], 0)})", "red")

        if player["hp"] <= 0:
            self.game_over()
            return

        self.show_status()

    def animate_attack(self, monster_name):
        self.print_text(f"You prepare to attack the {monster_name}...", "white")

    def handle_monster_defeat(self, current_room, monster):
        self.print_text(f"You defeated the {monster['name']}!", "green")
        # Drop item if any
        drop = monster.get("drop")
        if drop:
            current_room.setdefault("items", []).append(drop)
            self.print_text(f"The {monster['name']} drops a {drop}.", "yellow")
        # Remove monster
        del current_room["monster"]
        self.show_status()
        self.update_buttons_state()

    def use_item(self, item_name):
        if item_name not in player["inventory"]:
            self.print_text(f"You don't have {item_name}.", "red")
            return
        if item_name not in items_info:
            self.print_text(f"{item_name} cannot be used.", "red")
            return

        # Special: using the mysterious key at the sealed gate unlocks it
        if item_name == "mysterious key":
            if player["location"] == "sealed_gate":
                if not player["gate_unlocked"]:
                    player["gate_unlocked"] = True
                    self.print_text("You insert the Mysterious Key. The Sealed Gate shudders and unlocks to the east.", "green")
                else:
                    self.print_text("The Sealed Gate is already unlocked.", "yellow")
            else:
                self.print_text("This key seems to fit only a very specific lock...", "yellow")
            return

        item = items_info[item_name]
        if "heal" in item:
            heal_amount = item["heal"]
            player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
            player["inventory"].remove(item_name)
            self.print_text(f"You used {item_name} and healed {heal_amount} HP. (Current HP: {player['hp']})", "green")
        else:
            self.print_text(f"You can't use {item_name} right now.", "red")

        self.show_status()
        self.update_buttons_state()

    def cast_spell_gui(self):
        if not player["spells_known"]:
            self.print_text("You don't know any spells yet.", "red")
            return
        if "spellbook" not in player["inventory"]:
            self.print_text("You need to have the spellbook to cast spells.", "red")
            return
        if player["mana"] <= 0:
            self.print_text("You don't have enough mana to cast spells.", "red")
            return

        spell = simpledialog.askstring("Cast Spell", f"Enter spell name ({', '.join(player['spells_known'])}):", parent=self.root)
        if not spell:
            return
        spell = spell.lower()

        if spell not in player["spells_known"]:
            self.print_text(f"You don't know the spell '{spell}'.", "red")
            return
        if spell not in spells:
            self.print_text(f"Spell '{spell}' data missing.", "red")
            return

        spell_data = spells[spell]
        if player["mana"] < spell_data["mana_cost"]:
            self.print_text("Not enough mana to cast this spell.", "red")
            return

        player["mana"] -= spell_data["mana_cost"]
        current_room = rooms[player["location"]]

        # Healing spell
        if spell == "heal":
            heal_amount = random.randint(*spell_data["heal"])
            player["hp"] = min(player["max_hp"], player["hp"] + heal_amount)
            self.print_text(f"You cast Heal and restore {heal_amount} HP! (HP: {player['hp']})", "green")
            self.show_status()
            self.update_buttons_state()
            return

        # Damage spell
        if "monster" in current_room:
            damage = random.randint(*spell_data["damage"])
            # Slight flavor: Firebird resists fire, Shadow Serpent takes extra lightning or ice? Keep simple for reliability
            monster = current_room["monster"]
            monster["hp"] -= damage
            self.print_text(f"You cast {spell_data['name']} and hit the {monster['name']} for {damage} damage! (Monster HP: {max(monster['hp'],0)})", "yellow")
            if monster["hp"] <= 0:
                self.handle_monster_defeat(current_room, monster)
                return
            else:
                # Monster counterattack
                shield_def = items_info[player["equipped_shield"]]["defense"] if player["equipped_shield"] and player["equipped_shield"] in items_info else 0
                monster_damage = random.randint(*monster["attack"]) - shield_def
                monster_damage = max(0, monster_damage)
                player["hp"] -= monster_damage
                self.print_text(f"The {monster['name']} attacks you for {monster_damage} damage! (Your HP: {max(player['hp'], 0)})", "red")
                if player["hp"] <= 0:
                    self.game_over()
                    return
        else:
            self.print_text("There is no monster here to cast that spell on.", "red")

        self.show_status()
        self.update_buttons_state()

    # ---------- Status / Help / Lore ----------

    def show_status(self):
        location_name = player['location'].replace('_', ' ').title()
        weapon = player['equipped_weapon'] if player['equipped_weapon'] else "None"
        shield = player['equipped_shield'] if player['equipped_shield'] else "None"
        status_text = (
            f"HP: {player['hp']}/{player['max_hp']}  |  Mana: {player['mana']}/{player['max_mana']}  |  "
            f"Location: {location_name}  |  Weapon: {weapon}  |  Shield: {shield}"
        )
        self.status_var.set(status_text)

    def show_help(self):
        help_text = (
            "Controls:\n"
            "- Movement: Go North/South/East/West/Up/Down\n"
            "- Look: Reprint room description\n"
            "- Pick Item: Take an item present in the room\n"
            "- Equip Item: Equip a weapon or shield from your inventory\n"
            "- Use Item: Use consumables (e.g., healing potion) or the Mysterious Key at the Sealed Gate\n"
            "- Attack: Manual attack against a monster in the room\n"
            "- Cast Spell: Requires Spellbook; choose one of your known spells\n"
            "- Inventory: View items and equip/use from a window\n"
            "- Status: Show HP/Mana/Location/Equipment\n"
            "- Talk: Speak to NPCs (Gorin or Auron)\n"
            "- Lore: Read the game's story\n"
            "- Restart: Reset the entire game"
        )
        messagebox.showinfo("Help", help_text)

    def show_lore(self):
        messagebox.showinfo("Lore – The Shattered Crown", LORE_TEXT)

    # ---------- Dialog Prompts ----------

    def pick_item_prompt(self):
        current_room = rooms[player["location"]]
        if not current_room.get("items"):
            self.print_text("No items to pick up here.", "red")
            return
        item = simpledialog.askstring("Pick Item", "Enter item name to pick:", parent=self.root)
        if item:
            self.pick_up(item.lower())

    def equip_item_prompt(self):
        if not player["inventory"]:
            self.print_text("No items in inventory to equip.", "red")
            return
        item = simpledialog.askstring("Equip Item", "Enter item name to equip:", parent=self.root)
        if item:
            self.equip_item(item.lower())

    def use_item_prompt(self):
        if not player["inventory"]:
            self.print_text("No items in inventory to use.", "red")
            return
        item = simpledialog.askstring("Use Item", "Enter item name to use:", parent=self.root)
        if item:
            self.use_item(item.lower())

    # ---------- NPCs / Quests / Riddles ----------

    def check_npc_interaction(self):
        current_room = rooms[player["location"]]
        # Auto prompt: announce NPC and hints
        if "npc" in current_room:
            npc = current_room["npc"]
            if npc["name"] == "Gorin the Blacksmith" and not npc.get("quest_given", False):
                self.print_text("\nGorin: 'Ho there! If you're braving the depths, bring me a Dragon Scale from the Dragon's Lair.'", "magenta")
                self.print_text("Gorin: 'And if you find a Shadow Fragment and a Phoenix Feather too... I might forge something special.'", "magenta")
                npc["quest_given"] = True
                player["quest_active"] = True

            if npc["name"] == "Auron the Spirit Mage" and not npc.get("spells_given", False):
                self.print_text("\nAuron: 'A familiar echo... You carry a shadow of the Crown. Take this knowledge.'", "magenta")
                self.print_text("Auron: 'Return if you wish to speak further.' (Use the 'Talk' button here.)", "magenta")

        # Riddle trigger when entering the riddle room
        if player["location"] == "riddle_room" and not player.get("riddle_solved", False):
            self.ask_riddle()

    def talk_to_npc(self):
        current_room = rooms[player["location"]]
        if "npc" not in current_room:
            self.print_text("There is no one to talk to.", "red")
            return

        npc = current_room["npc"]
        if npc["name"] == "Gorin the Blacksmith":
            self.talk_gorin(npc)
        elif npc["name"] == "Auron the Spirit Mage":
            self.talk_auron(npc)
        else:
            self.print_text("They have nothing more to say.", "magenta")

    def talk_gorin(self, npc):
        # Rewards: If player has dragon scale and hasn't been rewarded, give potion
        has_scale = "dragon scale" in player["inventory"]
        has_shadow = "shadow fragment" in player["inventory"]
        has_feather = "phoenix feather" in player["inventory"]
        has_key = "mysterious key" in player["inventory"]

        if has_scale and not npc.get("first_reward_given", False):
            self.print_text("\nGorin: 'By the coals—you got the Dragon Scale! Take this healing potion as thanks.'", "magenta")
            if "healing potion" not in player["inventory"]:
                player["inventory"].append("healing potion")
            npc["first_reward_given"] = True
            player["quest_completed"] = True
            self.show_status()
            return

        # Craft the mysterious key if player has all three components and key not yet crafted
        if has_scale and has_shadow and has_feather and not npc.get("key_crafted", False) and not has_key:
            self.print_text("\nGorin: 'You brought everything! The Scale, the Shadow, and the Feather... stand back!'", "magenta")
            self.print_text("Gorin begins forging—a glow, a scream of metal, and then silence.", "magenta")
            # Consume materials
            player["inventory"].remove("dragon scale")
            player["inventory"].remove("shadow fragment")
            player["inventory"].remove("phoenix feather")
            # Give key
            player["inventory"].append("mysterious key")
            npc["key_crafted"] = True
            self.print_text("Gorin: 'It's done—the Mysterious Key. Use it at the Sealed Gate.'", "magenta")
            self.show_status()
            return

        # Hints:
        missing = []
        if not has_scale:
            missing.append("Dragon Scale (Dragon Lair)")
        if not has_shadow:
            missing.append("Shadow Fragment (Shadow Cavern)")
        if not has_feather:
            missing.append("Phoenix Feather (Phoenix Nest)")

        if missing:
            self.print_text("\nGorin: 'You're still missing:'", "magenta")
            for m in missing:
                self.print_text(f" - {m}", "yellow")
        else:
            if has_key:
                self.print_text("\nGorin: 'You have the key already. The Sealed Gate waits to the north of the Secret Passage.'", "magenta")
            else:
                self.print_text("\nGorin: 'If you have all three, I can forge the key.'", "magenta")

    def talk_auron(self, npc):
        # Grant spells and wand on first proper talk
        if not npc.get("spells_given", False):
            # Teach Ice Shard and Lightning Bolt if not known
            taught = []
            for s in ("ice shard", "lightning bolt"):
                if s not in player["spells_known"]:
                    player["spells_known"].append(s)
                    taught.append(s)
            if taught:
                self.print_text(f"\nAuron: 'I share knowledge: {', '.join(taught)}.'", "magenta")
            else:
                self.print_text("\nAuron: 'You already know what I would teach. Good.'", "magenta")
            npc["spells_given"] = True

        if "spellbook" not in player["inventory"]:
            self.print_text("Auron: 'Seek the Spellbook in the Library to cast what you know.'", "magenta")

        if not npc.get("wand_given", False) and "magic wand" not in player["inventory"]:
            # Give wand once
            player["inventory"].append("magic wand")
            self.print_text("Auron: 'Take this wand to focus your power.' (Magic Wand acquired.)", "magenta")
            npc["wand_given"] = True

        # General guidance
        self.print_text("Auron: 'Three echoes: Shadow in the cavern, Fire in the nest, Will in the dragon. Return with their remnants.'", "magenta")

    def ask_riddle(self):
        riddle = (
            "I speak without a mouth and hear without ears. I have nobody, but I come alive with wind. What am I?"
        )
        answer = simpledialog.askstring("Riddle", riddle, parent=self.root)
        if answer:
            if answer.strip().lower() == "echo":
                self.print_text("The door clicks and opens! You solved the riddle!", "green")
                player["riddle_solved"] = True
            else:
                self.print_text("That is not the correct answer. Try again later.", "red")

    # ---------- Ending & Game Over ----------

    def trigger_ending(self):
        # Narrative ending when you step into sunlit_exit
        self.print_text("\nAs sunlight spills over you, memories surge—the Crown, the Rite, the breaking.\n", "lightgreen")
        self.print_text("You are Vaelion. This prison was your soul. Opening the Gate unmade the curse... and you.\n", "lightgreen")
        self.print_text("The light burns. The dungeon exhales. Somewhere, far above, a kingdom wakes from a nightmare.\n", "lightgreen")
        self.print_text("Your story ends. Their story begins.\n", "lightgreen")
        self.disable_all_buttons(end_reached=True)

    def game_over(self):
        self.print_text("You have been defeated! Game Over.", "red")
        self.disable_all_buttons()

    def disable_all_buttons(self, end_reached: bool = False):
        for btn in [self.btn_north, self.btn_south, self.btn_east, self.btn_west,
                    self.btn_up, self.btn_down, self.btn_attack, self.btn_pick,
                    self.btn_equip, self.btn_use, self.btn_cast, self.btn_look,
                    self.btn_inventory, self.btn_status, self.btn_help, self.btn_talk, self.btn_lore]:
            btn.config(state=tk.DISABLED)
        # Keep restart & quit always active
        self.btn_restart.config(state=tk.NORMAL)
        self.btn_quit.config(state=tk.NORMAL)
        if end_reached:
            self.print_text("You may 'Restart' to play again.", "yellow")

    # ---------- Restart ----------

    def restart_game(self):
        global rooms, player
        rooms = copy.deepcopy(DEFAULT_ROOMS)
        player = copy.deepcopy(DEFAULT_PLAYER)
        self.text_area.configure(state='normal')
        self.text_area.delete("1.0", tk.END)
        self.text_area.configure(state='disabled')
        self.print_text("Game reset. Welcome back to The Shattered Crown!", "lightgreen")
        self.look_room()
        self.update_buttons_state()
        self.show_status()

def main():
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
