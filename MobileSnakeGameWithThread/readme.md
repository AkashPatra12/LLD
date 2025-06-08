# 🐍 Snake Game – Multithreaded Python Version with SOLID & Distributed Design

This project showcases a multithreaded implementation of the classic Snake Game using **SOLID principles**, **design patterns**, and hooks for distributed systems. It includes support for concurrent input handling and simulates multiplayer readiness using threading and locking.

---

## ✅ Requirements

In a Low-Level Design (LLD) interview context, the requirements for the Snake Game system are:

* The game should support a 2D grid-based board where a snake can move in four directions.
* The snake should grow in size upon consuming food and the game should render this update visually.
* When the snake hits the boundary, it should wrap around the board.
* The game should support direction inputs from a user or external source (simulating multiplayer or remote control).
* There should be an ability to log gameplay events for debugging or analytics.
* The design should be extensible (e.g., new food types, power-ups, themes).
* The architecture should allow concurrency and be prepared for distributed setup (e.g., cloud sync, multiplayer).

Technical environment for running the code:

* Python 3.7+
* No external dependencies (only Python standard library)

---

## 🔄 High-Level Game Flow

```
Main Thread
   └── Creates Mock Server and Game Thread
         └── Game Thread runs SnakeGameEngine.start_game()
               └── Repeatedly calls update() every tick
```

## 🧠 Detailed Component Flow

### 1. Game Initialization (`__main__`)

* `MockGameServer` is created with initial input.
* `SnakeGameEngine` is instantiated with the server.
* A background thread starts the game loop.

### 2. SnakeGameEngine.**init**()

* Initializes:

  * `Board`, `Snake`, `FoodSpawner`, `Renderer`, `Logger`, `InputHandler`
* Registers `handle_input` callback.
* Spawns food using strategy.

### 3. Game Loop (start\_game)

* For a fixed number of ticks:

  * Calls `update()` and sleeps for `tick_rate` seconds.

### 4. Game Tick (update)

* If server is present:

  * Fetch input → update direction
* Move snake
* Wrap snake head if needed
* If food is eaten:

  * Log event
  * Grow snake
  * Spawn new food
* Sync state to server
* Render updated state to console

### 5. Threading & Locking

* Server access is protected with `threading.Lock`
* Input and state updates are safely handled

## 🧠 Features

* Console-based snake movement and food consumption.
* Real-time direction change via simulated server inputs.
* Thread-safe multiplayer simulation using `threading.Lock`.
* Clean architecture following OOP and SOLID design principles.
* Plug-and-play food strategy and server sync support.

---

## 🧹 Design Patterns Used

| Pattern       | Role                                                            |
| ------------- | --------------------------------------------------------------- |
| **Strategy**  | Dynamic food spawning behavior via `IFoodStrategy`.             |
| **Observer**  | `InputHandler` notifies `SnakeGameEngine` of direction changes. |
| **Command**   | Directional inputs treated as encapsulated commands.            |
| **Singleton** | Centralized logging through `GameLogger`.                       |
| **Factory**   | FoodSpawner creates food using injected strategy.               |

---

## 🧱 UML Overview

```text
+---------------------+         +---------------------+
|  SnakeGameEngine    |<------->|    GameServerInterface  |
+---------------------+         +---------------------+
| - board             |         | +sync_state()       |
| - snake             |         | +fetch_remote_moves() |
| - food_spawner      |         +---------------------+
| - renderer          |
| - logger            |         +----------------+
| - input_handler     |<------->|  InputHandler   |
| +start_game()       |         +----------------+
| +update()           |             ↑
+---------------------+            Observer pattern

+----------------+
|     Snake      |
+----------------+
| - body         |
| - direction    |
| +move()        |
| +set_direction()|
+----------------+

+-----------------------+
|     FoodSpawner       |
+-----------------------+
| - strategy            |
| +spawn_food()         |
+-----------------------+

+----------------+
|   Renderer     |
+----------------+
| +render()      |
+----------------+

+----------------+
|  GameLogger    | (Singleton)
+----------------+
| +log_event()   |
+----------------+
```

---

## ⚙️ Code Flow

### Initialization

* A `MockGameServer` is instantiated with preloaded direction input.
* A game engine is started in a separate thread.

### Game Loop (`start_game`)

* Loops for N ticks with `tick_rate` pause between iterations.
* In each tick:

  * Fetch direction from server.
  * Move the snake.
  * Check if food is eaten and grow if true.
  * Sync state with server.
  * Render board.

### Concurrency Handling

* Server input queue is guarded by a `Lock`.
* Input and game loop can run concurrently without data races.

---

## 🧵 Why Threading is Used

Threading is not strictly required for distributed systems, but it enables real-time responsiveness and concurrent input processing, which are crucial for interactive or multiplayer systems.

### ✅ Why Threading is Used Here

* Runs the game loop in parallel with external inputs.
* Simulates remote player input while maintaining consistent game updates.
* Prevents input delay or render blocking.
* Protects shared resources (`input_queue`, `state`) with `threading.Lock`.

### 💡 Where It's Used

* Game loop runs in its own `threading.Thread`.
* Shared input queue in `MockGameServer` is accessed from multiple threads safely.

### 🔄 Alternatives

* Use `asyncio` instead of threads for coroutines.
* Use message queues (e.g., Kafka) for distributed input.
* Backend sync via polling or event triggers.

## 🎮 Thoughts on Multiplayer Games

In a true multiplayer game:

* Each player would have a client interface sending inputs to a central server.
* Server maintains canonical game state, broadcasts updates to clients.
* You would need:

  * **Input listeners** (WebSockets, HTTP, etc.)
  * **State broadcasters** to push updates
  * **Threading or async IO** to manage multiple client connections
  * **Locking or transactional updates** to handle simultaneous actions

Threading helps prototype these behaviors locally and prepares the codebase for production-scale distributed gameplay.

## 🔐 Thread Safety

* All access to shared data (`input_queue`, `state`) in `MockGameServer` is protected using `threading.Lock`.
* The game runs in a separate thread; main thread simulates additional inputs.

---

## 🚀 Running the Game

```bash
python snake_game_lld.py
```

The game will:

* Render the board every 0.5 seconds.
* Simulate direction changes from a remote client.
* Display logs when food is eaten.

---

## 📊 Scalability Considerations

* Replace `MockGameServer` with a WebSocket or REST server for real-time multiplayer.
* Extend `GameLogger` to publish to cloud logging services.
* Add `GameStateSerializer` for save/load or replay functionality.

---

## 📦 Extensibility Ideas

* Add AI snake player (`SnakeBot`) with pathfinding.
* Introduce power-ups or obstacles using polymorphic `Tile` classes.
* Export state to UI with `pygame` or Web GUI.

---

## 🥺 Testing

To test logic:

* Create unit tests for `Snake`, `Board`, and `FoodSpawner`.
* Simulate remote input using `add_input()` in `MockGameServer`.

---

## 📎 License

MIT License © YourName
