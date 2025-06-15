# 🐍 Snake Game – Single-Threaded Version with Game Completion Flow

This project presents a clean and modular single-threaded implementation of the classic Snake Game using **SOLID principles** and **object-oriented design patterns**. It supports food consumption, rendering, directional input handling, and a defined game completion flow.

---

## ✅ Requirements (LLD Interview Style)

* The snake moves in a grid-based board and wraps around boundaries.
* The snake grows after consuming food.
* The system must be extensible to support multiple food types or tiles.
* The design should log key game events.
* The game should terminate cleanly after a defined condition (e.g., fixed steps).

## Logic

### Move with No Food
* [(1,1), (1,2), (1,3), (2,3)] to 
* [(1,2), (1,3), (2,3), (2,4)]
* we removed the tail of the window and added a new head to the window

### Move with No Food consumption
* [(1,1), (1,2), (1,3), (2,3)] to
* [(1,1), (1,2), (1,3), (2,3), (2,4)]
* we simply added a new head to the snake with the head being the cell (2,4).
*  The tail remained the same in this case.

A queue is an abstract data structure with some specified properties which meets our requirements

## Algorithm

1. Initialize a queue containing a single cell (0,0) which is the initial position of the snake at the beginning of the game. Note that we will be doing this in the constructor of the class and not in the move function.
2. The fist thing we need to do inside the move function is to compute the new head based on the direction of the move. As we saw in the intuition section, irrespective of the kind of move, we will always get a new head. We need the new head position to determine if the snake has hit a boundary and hence, terminate the game.
3. Let's first discuss the termination conditions before moving on to the modifications we would make to our queue data structure.
   a. The first condition is if the snake cross either of the boundaries of the grid after the mode, then we terminate. So for this, we simply check if the new head (new_head) satisfies new_head[0] < 0 or new_head[0] > height or new_head[1] < 0 or new_head[1] > width
   b. The second condition is if the snake bites itself after the move. An important thing to remember here is that the current tail of the snake is not a part of the snake's body. If the move doesn't involve a food, then the tail gets updated (removed) as we have seen. If this is a food move, then the snake cannot bite itself because the food cannot appear on any of the cells occupied by the snake (according to the problem statement).
  In order to check if the snake bites itself we need to check if the new head already exists in our queue or not. This can turn out to be an O(N) operation and that would be costly. So, at the expense of memory, we can also use an additional dictionary data structure to keep the positions of the snake. This dictionary will only be used for this particular check. We can't do with just a dictionary because a dictionary doesn't have an ordered list of elements and we need the ordering for our implementation.
4. f none of the termination conditions have been met, then we will continue to update our queue with the new head and potentially remove the old tail. If the new head lands on a position which contains food, then we simply add the new head to our queue representing the snake. We won't pop the tail in this case since the length of the snake has increased by 1
5. After each move, we return the length of the snake if this was a valid move. Else, we return -1 to indicate that the game is over.


---

## 🕰️ What is a Tick?

A tick is like a time step. During each tick, the following happens:

* Input is processed (e.g., direction change).
* Game state is updated (e.g., snake moves).
* Collisions are checked (e.g., food or wall).
* Rendering is done (updated board is displayed).
* The engine waits or immediately proceeds to the next tick (depending on timing logic, if any).

## 🔄 High-Level Game Flow

```
Main Thread
 └── Runs SnakeGameEngine.start_game()
       └── Loop (for N ticks):
             ├── Handle directional input via InputHandler
             ├── Move the snake (Snake.move)
             ├── Wrap snake position if needed (Board.wrap_position)
             ├── Check for food collision
             │     ├── If food is eaten:
             │     │     ├── Log the event
             │     │     ├── Grow the snake
             │     │     └── Spawn new food (FoodSpawner)
             ├── Render the updated board (Renderer)
             └── Check if termination condition met
```

---

## 🧠 Detailed Component Flow

### 1. Game Initialization

* Instantiate `SnakeGameEngine`.
* Components initialized: `Board`, `Snake`, `FoodSpawner`, `Renderer`, `GameLogger`, `InputHandler`.
* Food is spawned randomly using strategy.

### 2. Game Loop (`start_game`)

* Runs for a defined number of ticks.
* Each tick:

  * Accept directional input and update snake direction.
  * Move snake and wrap position.
  * If snake eats food:

    * Log event
    * Grow snake
    * Spawn new food
  * Render board with snake and food
  * Continue until tick limit is reached

### 3. Game Completion

* After the final tick:

  * Game loop exits cleanly
  * Final state is rendered (optional)
  * Can be extended to include: score summary, reset option, or collision-based termination

---

## 🧹 Design Patterns Used

| Pattern       | Role                                                          |
| ------------- | ------------------------------------------------------------- |
| **Strategy**  | `RandomFoodStrategy` injects food placement logic.            |
| **Singleton** | `GameLogger` ensures consistent logging instance.             |
| **Observer**  | `InputHandler` notifies the engine via callback registration. |
| **Factory**   | `FoodSpawner` uses strategy to generate new food positions.   |

---

## 🧱 UML Overview

```text
+---------------------+
|  SnakeGameEngine    |
+---------------------+
| - board             |
| - snake             |
| - food_spawner      |
| - renderer          |
| - logger            |
| - input_handler     |
| +start_game()       |
| +update()           |
+---------------------+
         |                          
         v
+----------------+
|     Snake      |
+----------------+
| - body         |
| - direction    |
| +move()        |
+----------------+
         |
         v
+----------------+
|    Board       |
+----------------+
| +wrap_position()|
+----------------+

+-----------------------+
|     FoodSpawner       |
+-----------------------+
| - strategy            |
| +spawn_food()         |
+-----------------------+

+----------------+
|  GameLogger    | (Singleton)
+----------------+
| +log_event()   |
+----------------+

+----------------+
|   Renderer     |
+----------------+
| +render()      |
+----------------+

+----------------+
| InputHandler   |
+----------------+
| +on_input()    |
+----------------+
```

---

## 🚀 Running the Game

```bash
python snake_game_lld.py
```

* The board updates after each directional input.
* Food is consumed and logged.
* Game ends after configured number of ticks.

---

## 🥺 Testing Ideas

* ✅ Snake movement logic
* ✅ Board wrapping logic
* ✅ Food spawn in empty cell
* ✅ Input handler callback working
* ✅ Food collision detection and snake growth
* ✅ Game completes after defined steps

---

## 📈 Extensibility

* Add different food types using `IFoodStrategy`
* Add `Tile` abstractions for obstacles or power-ups
* Add scoring, themes, or UI with minimal changes
* Add game over on self-collision or time-based score

---

## 🧠 Time Complexity
### ✅ Snake.move(grow=False)
* Deque appendleft and pop: O(1)

* Set add/remove: O(1)

* 👉 Total: O(1) per move

### ✅ Snake.hits_itself()
* body[0] in snake_set: O(1) (set lookup)

* body.count(head): O(n) worst-case (needed because head is already in the set, so we confirm it's duplicated)

* ⚠️ Worst-case O(n) (where n = length of the snake), but can be optimized further by not needing .count() (if you defer adding head until after checking)

### ✅ Board.is_out_of_bounds()
* Simple comparisons: O(1)

### ✅ FoodSpawner.spawn_food()
* Worst-case: if snake occupies almost the entire board, generating random positions can take O(k) retries, where k = number of empty cells

* 👉 Worst-case: O(board size) = O(W × H)

* Average case: O(1) if snake is small or food is placed quickly

### ✅ SnakeGameEngine.update()
Includes:

* snake.move() → O(1)

* snake.hits_itself() → O(n)

* is_out_of_bounds() → O(1)

* spawn_food() → O(k), k = # of free cells

* print_board() → O(W × H)

* 👉 Total per update() step:

* Best case: O(1)

* Worst case: O(n + W × H) (mostly due to printing and food placement retries)

## 🧠 Space Complexity
### ✅ Snake.body (deque of coordinates):
O(n), where n is snake length

### ✅ Snake.snake_set:
O(n), one entry per body part

### ✅ Board:
O(1), just stores width and height

### ✅ FoodSpawner:
O(1), only holds reference to a strategy

### ✅ InputHandler.callbacks:
O(c), where c = number of registered input callbacks (usually 1)

### ✅ Board Printing (in print_board):
Temporarily builds one row at a time → O(W) at most for row string

### 👉 Total space usage: O(n + W × H)
(where n = snake length, W × H = board size)

## 🧠 Time and Space Complexity Summary

| Component                     | Time Complexity        | Space Complexity       |
|------------------------------|------------------------|------------------------|
| `Snake.move()`               | O(1)                   | O(n) (body, set)       |
| `Snake.hits_itself()`        | O(n) (due to `.count()`) | O(n)                 |
| `FoodSpawner.spawn_food()`   | O(k) (k = empty cells) | O(1)                   |
| `Board.is_out_of_bounds()`   | O(1)                   | O(1)                   |
| `SnakeGameEngine.update()`   | O(n + W×H) (worst case)| O(n + W×H)             |
| `print_board()`              | O(W × H)               | O(W) (temporary row)   |

### Notes:
- **n** = Length of the snake
- **W, H** = Width and Height of the board
- **k** = Number of unoccupied cells (used during food generation)

### Optimizations:
- Self-collision check uses a `set` for O(1) lookup, but `.count()` adds O(n) in worst case. This can be removed for full O(1) check.
- Rendering and food spawning dominate the worst-case cost for large boards.


Add profiling or logging for performance








