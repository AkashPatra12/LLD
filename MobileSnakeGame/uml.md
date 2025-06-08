# 🐍 Mobile Snake Game – LLD with SOLID, Design Patterns, and Distributed Readiness

This project implements a modular, extensible Snake game in Python using object-oriented principles, SOLID design, and architectural patterns fit for scaling to multiplayer or distributed environments.

---

## 🧱 Core Components

1. **SnakeGameEngine** – Controls the game loop and state transitions.
2. **Board** – Represents the 2D game grid with wrapping.
3. **Snake** – Maintains the snake’s position, growth, and movement logic.
4. **FoodSpawner** – Uses a strategy to place food on the board.
5. **InputHandler** – Handles user or remote input via callbacks.
6. **GameLogger** – Singleton logger for tracking game events.
7. **Renderer** – Renders game state to console.
8. **GameServerInterface** – Interface to abstract multiplayer or online play.

---

## 🧩 Design Patterns Used

| Pattern               | Purpose                                                      |
|------------------------|--------------------------------------------------------------|
| **Strategy**          | For flexible food spawning logic.                            |
| **Observer**          | `InputHandler` notifies the engine of direction changes.     |
| **Command**           | Directional input can be treated as commands.                |
| **Singleton**         | Central logger via `GameLogger`.                             |
| **Factory-like**      | `FoodSpawner` creates food objects with a swappable strategy.|
| **MVC (lightweight)** | Separation of concerns between UI rendering and game logic.  |

---

## ✅ SOLID Principles

- **S**ingle Responsibility: Entities have isolated roles (e.g. rendering vs logic).
- **O**pen/Closed: Easily extend `FoodStrategy`, `Renderer`, or add power-ups.
- **L**iskov: Subtypes like `IFoodStrategy` can be replaced seamlessly.
- **I**nterface Segregation: Input, rendering, and networking are cleanly separated.
- **D**ependency Inversion: Game engine relies on abstract interfaces (e.g. `GameServerInterface`).

---

## 🔁 Scalability & Extensibility

- **Multiplayer Ready**: Use `GameServerInterface` to plug into WebSocket or cloud sync.
- **Theming**: UI rendering logic is decoupled and swappable.
- **Analytics**: Extend `GameLogger` to support remote log streaming.
- **Cloud Save**: Add `GameStateSerializer` for persistence and replays.

---

## 🧬 UML Class Diagram

```text
+--------------------+        +---------------------+
|  SnakeGameEngine   |<>------|     GameState       |
+--------------------+        +---------------------+
| - gameState        |        | - snake: Snake      |
| - inputHandler     |        | - board: Board      |
| - renderer         |        | - food: Food        |
| - foodSpawner      |        | - score: int        |
| - logger           |        +---------------------+
| +startGame()       |
| +update()          |
+--------------------+

+----------------+        +---------------+
|     Board      |<>------|    Tile       |
+----------------+        +---------------+
| - grid[][]     |        | - position    |
| +draw()        |        +---------------+

+----------------+
|     Snake      |
+----------------+
| - body: Deque  |
| - direction    |
| +move()        |
| +grow()        |
+----------------+

+--------------------+       +-----------------+
|    FoodSpawner     |<------|  IFoodStrategy  |
+--------------------+       +-----------------+
| - strategy          |       | +generateFood() |
| +spawnFood()        |       +-----------------+
+--------------------+

+-------------------+
|   InputHandler    |<>---Observer pattern---> GameEngine
+-------------------+
| +onSwipe()        |
+-------------------+

+----------------+
|    Renderer    |
+----------------+
| +render()      |
+----------------+

+----------------------+
|  GameLogger (Singleton) |
+----------------------+
| +logEvent()          |
+----------------------+

+--------------------------+
|  GameServerInterface     |
+--------------------------+
| +syncState()             |
| +fetchLiveGameData()     |
+--------------------------+
