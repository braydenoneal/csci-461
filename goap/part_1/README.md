# GOAP Project Part 1

1. The program currently selects a single goal and searches for any set of actions that meet the goal. Improve the search to return an optimal -- or at least shorter -- result.

The `next_actions` function in `worldmodel.py` was modified to return the valid action with the lowest cost.

```diff
diff --git goap/worldmodel.py goap/worldmodel.py
index 1977ec2..c0a218f 111111
--- goap/worldmodel.py
+++ goap/worldmodel.py
@@ -46,12 +46,23 @@ def get_total_cost(self):
     # select the next action that applies
     def next_action(self):
         self.current_action_index += 1
+
+        valid_actions = []
+
         for a in self.action_list:
-            if not a.requires:
-                return a
+            preconditions_met_quantity = 0
+
             for precondition in a.requires:
                 if precondition in self.current_state:
-                    return a
+                    preconditions_met_quantity += 1
+
+            if preconditions_met_quantity >= len(a.requires):
+                valid_actions.append(a)
+
+        if valid_actions:
+            valid_actions = sorted(valid_actions, key=lambda x: x.cost)
+            return valid_actions[0]
+
         return None
         
 # Remove an action from our action list
```

The best plan is now:

```
goto_target
goto_node
idle
get_axe
melee_attack
```

with a total cost of 5, instead of the previous:

```
get_axe
chop_log
collect_branches
melee_attack
```

with a total cost of 16.
