"""
Test configuration data for GOAP implementation.

Created: Chris Branton, 2023-05-07.

Note: not all values are used in initial implementation.
"""

goal_list = [
    {"name": "idle", "value": 1, "change": 0},
    {"name": "kill_enemy", "value": 20, "precondition": "attacking"},
    {"name": "make_fire", "value": 5, "precondition": "have_firewood", "change": 1}
]

action_list = [
    {"name": "get_axe", "cost": 2, "precondition": ["axe_available"], "satisfies": ["have_axe"]},
    {"name": "chop_log", "cost": 4, "precondition": ["have_axe"], "satisfies": ["have_firewood"]},
    {"name": "collect_branches", "cost": 8, "satisfies": ["have_firewood"]},
    {"name": "melee_attack", "cost": 2, "satisfies": ["attacking"], "precondition": ["equipped_melee", "at_target"]},
    {"name": "ranged_attack", "cost": 3, "satisfies": ["attacking"], "precondition": ["equipped_ranged", "have_ammo",
                                                                                      "near_target"]},
    {"name": "goto_target", "satisfies": ["at_target", "near_target"]},
    {"name": "equip_ranged", "cost": 2, "satisfies": ["equipped_ranged"]},
    {"name": "equip_melee", "cost": 2, "satisfies": ["equipped_melee"]},
    {"name": "goto_node", "satisfies": ["at_node"]},
    {"name": "idle", "satisfies": ["idle"], "cost": 1}
]

# Different types for state variables add complexity. Some implementations
# may choose to make all variables one type (e.g. float)
world_state = {"have_melee": True, "have_ranged": True, "have_ammo": True,
               "equipped_melee": True, "axe_available": True, "enemy_visible": True}
