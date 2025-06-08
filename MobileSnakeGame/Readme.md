# 🐍 Snake Game – Single-Threaded Version with Game Completion Flow

This project presents a clean and modular single-threaded implementation of the classic Snake Game using **SOLID principles** and **object-oriented design patterns**. It supports food consumption, rendering, directional input handling, and a defined game completion flow.

---

## ✅ Requirements (LLD Interview Style)

* The snake moves in a grid-based board and wraps around boundaries.
* The snake grows after consuming food.
* The system must be extensible to support multiple food types or tiles.
* The design should log key game events.
* The game should terminate cleanly after a defined condition (e.g., fixed steps).

Environment:

* Python 3.7+
* No external dependencies (standard library only)

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

## 📎 License

MIT License © YourName
