# 🐍 Snake Game – Single-Threaded Version with SOLID & Design Patterns

This project presents a clean and modular single-threaded implementation of the classic Snake Game using **SOLID principles** and **object-oriented design patterns**. It runs in a console environment and supports food consumption, rendering, and directional input handling.

---

## ✅ Requirements (LLD Interview Style)

* The snake moves in a grid-based board and wraps around boundaries.
* The snake grows after consuming food.
* The system must be extensible to support multiple food types or tiles.
* The design should log key game events.
* No need for concurrency or threading.
* Built with maintainability and testability in mind.

Environment:

* Python 3.7+
* No external dependencies (only uses Python standard library)

---

## 🔄 High-Level Game Flow

```
Main Thread
 └── Runs SnakeGameEngine.start_game()
       └── In each loop tick: handle input → update state → render board
```

---

## 🧠 Detailed Component Flow

### 1. Game Initialization

* Instantiate `SnakeGameEngine`.
* Components initialized: `Board`, `Snake`, `FoodSpawner`, `Renderer`, `GameLogger`, `InputHandler`.
* Food is spawned randomly.

### 2. Game Loop (start\_game)

* Runs for a fixed number of ticks.
* At each tick:

  * InputHandler updates direction.
  * Snake moves in the current direction.
  * Board wraps position.
  * Collision with food is checked.
  * Renderer prints game state.

---

## 📊 Features

* Grid-based movement with board wrapping.
* Direction changes via input handler.
* Snake grows on consuming food.
* Food appears in random positions.
* Console rendering.
* Logging events like "food eaten".

---

## 🧹 Design Patterns Used

| Pattern       | Role                                                          |
| ------------- | ------------------------------------------------------------- |
| **Strategy**  | `RandomFoodStrategy` injects food placement logic.            |
| **Singleton** | `GameLogger` ensures consistent logging instance.             |
| **Observer**  | `InputHandler` notifies the engine via callback registration. |
| **Factory**   | `FoodSpawner` uses strategy to generate new food positions.   |

---

## 📏 UML Overview

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
* Game renders new snake and food positions after each move.

---

## 🔹 Example Gameplay Tick

1. User input: right
2. Snake moves one cell to the right.
3. If snake eats food:

   * Grows in size
   * New food spawned
   * Logs event
4. Board is printed with current snake and food positions.

---

## 🥺 Testing Ideas

* ✅ Snake movement logic
* ✅ Board wrapping logic
* ✅ Food spawn in empty cell
* ✅ Input handler callback working
* ✅ Food collision detection and snake growth

---

## 📈 Extensibility

* Add different food types using `IFoodStrategy`
* Add `Tile` abstractions for obstacles or power-ups
* Add scoring, themes, or UI with minimal changes

---

## 📎 License

MIT License © YourName
