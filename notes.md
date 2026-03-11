This script is a **Pygame animation generator** that creates a 45-second full-HD sequence of a “blueprint being drawn” by multiple moving agents called **architects**. It saves every frame as a PNG so the frames can later be turned into a video.

Here is what each part is doing.

## Big picture

The program:

1. sets up a 1920×1080 Pygame window
2. creates intro title frames
3. creates 20 simulated “architects”
4. repeatedly asks a local AI model for movement commands like `forward 60` or `turn left`
5. feeds those commands to the architects
6. has them draw glowing blueprint-like lines as they move
7. overlays a scrolling HUD of the commands with a glitch effect
8. saves every frame to a `maze_frames` folder

So the result is a procedural animated drawing that looks like a living blueprint or maze plan.

---

## Imports and setup

The imports are standard Python libraries plus `pygame`.

* `pygame` handles graphics and drawing
* `random`, `time`, `math`, `re` support motion, timing, and parsing
* `json`, `urllib.request`, `urllib.parse` are used to talk to the local Ollama API
* `os` handles paths and directories

This line starts a timer:

```python
start_time = time.time()
```

It is later used to report how long the script took to run.

Then it creates a folder named `maze_frames` next to the script if it does not already exist:

```python
frames_dir = os.path.join(os.path.dirname(__file__), "maze_frames")
```

That is where every PNG frame is saved.

---

## AI instruction generator

The function `get_architecture_instructions()` talks to a **local Ollama server** at:

```python
http://localhost:11434/api/generate
```

It randomly chooses one of several prompts that all ask for exactly 5 simple movement commands such as:

* `forward 60`
* `turn left`
* `turn right`
* `turn around`

It sends the prompt as JSON to model:

```python
"gemma3:270m"
```

Then it reads the AI response, splits it into lines, strips blanks, and returns a list of instructions.

If the API fails for any reason, it falls back to this hardcoded list:

```python
[
    "forward 60",
    "turn left",
    "forward 40",
    "turn right",
    "forward 50"
]
```

So the animation still works even if Ollama is unavailable.

---

## Color and visual constants

These define the blueprint look:

```python
BLUEPRINT_BG = (12, 34, 78)
```

This is the dark blue background.

`BLUEPRINT_LINES` is a list of lighter blue/white line colors. Each architect gets one randomly.

The glitch symbol tiers are used for the HUD text corruption effect:

* `GLITCH_TIER_1`: basic symbols like `#`, `%`, `@`
* `GLITCH_TIER_2`: heavier block/math symbols like `█`, `Ω`, `∞`
* `GLITCH_TIER_3`: light fragments like `.`, `_`, spaces

As HUD text scrolls upward, letters gradually mutate into these symbols and disappear.

---

## The `Architect` class

This is the core of the animation.

Each architect is like a little drawing robot with its own:

* position
* direction
* drawing style
* speed
* pause behavior
* command queue

### `__init__`

When an architect is created, it gets:

* starting `(x, y)` position
* screen width/height for wrapping
* a random direction from right/up/left/down
* a random blueprint line color
* a random line width
* a random joint marker size

It also sets up movement state:

* `command_queue`: commands ready to execute
* `pending_commands`: commands delayed before activation
* `distance_remaining`: how much farther it still needs to move in a current forward command

Each architect behaves slightly differently because it gets random values for:

* `move_speed`
* `step_interval`
* `command_jitter`
* `rest_chance`
* pulse animation settings

That randomness is what makes the final motion feel organic instead of synchronized.

---

## Parsing commands

### `parse_and_execute(self, instruction, surface=None)`

This method takes a command string like:

* `forward 50`
* `turn left`
* `turn right`
* `turn around`

It does not execute it immediately. Instead, it adds it to `pending_commands` with a small random delay. That creates staggered responses so all architects do not react at once.

It uses regex here:

```python
forward_match = re.search(r'forward\s+(\d+)', instruction)
```

So if the instruction contains `forward 72`, it extracts `72`.

If it sees turn text, it stores one of:

* `"turn_left"`
* `"turn_right"`
* `"turn_around"`

If it just sees the word `forward` without a number, it defaults to `50`.

---

## Releasing delayed commands

### `release_pending_commands(self)`

Each frame, this decreases the countdown delay for each pending command.

When a delay hits zero, that command moves into `command_queue`, where it becomes ready to execute.

---

## Updating each architect

### `update(self, surface, frame_count)`

This is called every frame.

What it does:

1. releases pending commands
2. decreases turn highlight timer if active
3. handles resting/pauses
4. only moves on its own rhythm (`step_interval`)
5. if it is in the middle of a forward command, it moves a little bit
6. otherwise, it starts the next queued command

This means architects do not instantly move a whole `forward 60`. They move it gradually over many frames.

That gradual movement is important because it allows continuous drawing.

---

## Moving and drawing lines

### `move_forward_step(self, distance, surface)`

This method:

* remembers the old position
* computes the new position using trig
* wraps position around screen edges with `%`
* draws a line from old position to new position

The movement math is:

```python
rad = math.radians(self.direction)
new_x = self.x + distance * math.cos(rad)
new_y = self.y - distance * math.sin(rad)
```

Note the minus on `y`: in screen coordinates, going “up” means decreasing y.

The architect briefly draws thicker lines after turning by using `corner_boost_timer`.

So turns leave stronger-looking corners.

---

## Drawing turn joints

### `draw_joint(self, surface)`

At a turn, the architect draws a little square blueprint-style joint at its current location.

This adds architectural detail and makes the corners look like drafting marks.

It draws:

* a filled square
* an outline
* a horizontal cross line
* a vertical cross line

---

## Turning methods

These three methods all do the same pattern:

* draw a joint marker
* set `corner_boost_timer`
* change direction

```python
turn_left
turn_right
turn_around
```

Direction is stored in degrees:

* `0 = right`
* `90 = up`
* `180 = left`
* `270 = down`

---

## Drawing the head marker

### `draw_head_marker(self, surface, frame_count)`

This draws a pulsing white circle at the architect’s current position.

It acts like a live cursor or drafting tool head.

The pulse uses sine wave math:

```python
pulse = (math.sin(frame_count * self.pulse_rate + self.pulse_phase) + 1.0) * 0.5
```

If the architect is currently moving forward, the marker gets a little bigger.

---

## Resolution and credits info

These values define the video dimensions:

```python
width = 1920
height = 1080
```

That is full HD.

Then the project metadata:

```python
name = "Sophia Vo"
title = "How to Make a Blueprint"
start_sequence_num = 1180000
```

`start_sequence_num` is the first frame number used in filenames.

So frames will be named something like:

* `1180000.png`
* `1180001.png`
* etc.

This is probably for course submission requirements.

---

## Pygame initialization

The code then creates:

* a clock for 60 FPS timing
* a Pygame window
* rendered text surfaces for the name and title

Fonts:

```python
titles_font = pygame.font.SysFont(None, int(width/12))
```

Then it renders the title text into images:

```python
name_f = titles_font.render(name, True, (255,255,255))
title_f = titles_font.render(title, True, (255,255,255))
```

---

## HUD text system

The HUD shows incoming AI instructions as scrolling terminal-like text.

```python
hud_messages = []
```

Each message stores:

* a list of character objects
* its vertical position `y`
* how much of it has been revealed so far with a typewriter effect

### `clean_for_hud(raw_text)`

This removes markdown and leading numbering like `1.` or `2)`.

### `is_valid_command(text)`

This filters out junk AI output. It only accepts text containing words like:

* `forward`
* `turn`
* `advance`
* `move`
* `rest`

So if the AI says something conversational like “Here are your commands,” that line is ignored.

---

## Intro frames

### `make_black()`

This creates 60 black frames, or 1 second at 60 FPS.

The script uses it to build a simple intro sequence:

1. 1 second black
2. 3 seconds showing name and title
3. 1 second black

So before the main animation even starts, there are already 5 seconds of frames.

---

## Main blueprint drawing surfaces

After the intro, the program switches to the blueprint scene.

It creates:

### `drawing_surface`

A transparent surface where all line drawing accumulates over time.

### `fade_surface`

A mostly transparent blue overlay used to slowly fade older lines.

Each frame, the code blits `fade_surface` onto `drawing_surface`, slightly washing out old lines without erasing everything immediately.

That creates the ghostly, decaying blueprint look.

---

## Creating architects

```python
architects = []
num_architects = 20
```

It creates 20 architects positioned randomly in the middle half of the screen:

```python
start_x = random.randint(width // 4, 3 * width // 4)
start_y = random.randint(height // 4, 3 * height // 4)
```

So they start clustered in a broad center region instead of the edges.

---

## Initial AI instructions

The script fetches an initial batch of instructions:

```python
current_instructions = get_architecture_instructions()
instruction_index = 0
```

Then it sets:

```python
frames_per_instruction_set = 60
```

So every 60 frames, or every 1 second, it asks the AI for 5 new commands.

---

## Main animation loop

This is the heart of the whole program:

```python
for i in range(0, 45 * 60):
```

That means 45 seconds at 60 FPS = **2700 frames**.

Inside the loop:

### 1. Refresh AI commands every second

If one second has passed, it requests a new instruction set from Ollama.

### 2. Feed one command every 12 frames

Every 12 frames, it takes the next instruction from the current set and:

* adds it to the HUD
* sends it to all architects

Since 60 / 12 = 5, that means all 5 commands are distributed over one second.

That matches the 5-command AI batches nicely.

### 3. HUD message creation

Each displayed HUD line is stored as a list of per-character objects:

```python
{
    'char': char,
    'is_scrambled': False,
    'life': 1.0,
    'eroded_frames': 0
}
```

This allows each character to glitch independently.

### 4. Random extra moves

Sometimes one random architect gets an extra command like:

* `forward 30`
* `forward 20`
* `turn left`
* `turn right`

This adds unpredictability.

### 5. Fade old drawing

```python
drawing_surface.blit(fade_surface, (0, 0))
```

This slowly dims older lines.

### 6. Update architects

Each architect moves and draws onto `drawing_surface`.

### 7. Compose final frame

The screen is rebuilt by:

* filling with blueprint background
* blitting the accumulated line drawing
* drawing pulsing head markers on top
* drawing HUD text on top of that

### 8. HUD glitch effect

For each HUD message:

* letters reveal gradually with `progress += 0.5`
* as the message rises upward, `height_factor` increases
* letters become more likely to scramble into glitch symbols
* scrambled symbols eventually disappear

This simulates terminal decay or corrupted machine instructions.

### 9. Remove dead messages

If a message scrolls too high or all its characters have vanished, it is removed.

### 10. Save frame

Every frame is saved as a PNG:

```python
pygame.image.save(screen, os.path.join(frames_dir, str(frame_num) + ".png"))
```

Then `frame_num` increments.

---

## Progress prints

Every 600 frames, it prints progress:

```python
if i % 600 == 0:
    print(f"Progress: {i // 60} seconds completed")
```

So roughly every 10 seconds of animation time.

---

## Shutdown and timing stats

At the end, it prints elapsed runtime in seconds and minutes:

```python
print("seconds:", int(time.time() - start_time))
print("~minutes: ", int((time.time() - start_time)/60))
```

Then it cleanly quits Pygame and exits.

---

## What makes this visually interesting

The script is not just moving lines randomly. Its style comes from combining several effects:

* **multiple independent agents** instead of one path
* **AI-generated movement instructions**
* **random delays and speeds** so movement is unsynchronized
* **persistent drawing with slow fading**
* **corner joints and width boosts** to make turns feel drafted
* **pulsing head markers** so the active positions remain visible
* **glitching command HUD** for a techno-blueprint vibe

---

## In one sentence

This code generates a frame-by-frame animated “blueprint maze” video where 20 autonomous drawing agents follow AI-generated movement instructions and leave behind fading architectural linework with a glitchy command display.
