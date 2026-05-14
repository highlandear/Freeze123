# Game Design

## Overview

The project currently contains two playable modes:

1. `Three-Step Challenge` for single-player runs
2. `Room Race` for multiplayer room-based sessions

This document describes the logic that is currently implemented in the codebase.

## Three-Step Challenge

### Goal

The player chooses a target distance and splits that distance into three movement stages.
The game generates three wooden-doll checkpoints.
Each stage is checked against the matching checkpoint using the player's cumulative distance.
If all three checks pass, the player wins.
If any check fails, the run ends immediately.

### Input Rules

The player chooses:

1. `target_distance`
   Range: `3` to `30`
2. `segments`
   Exactly three positive integers whose sum equals `target_distance`

Examples:

- `3 -> [1, 1, 1]`
- `4 -> [1, 1, 2]`, `[1, 2, 1]`, `[2, 1, 1]`
- `6 -> [1, 2, 3]`, `[2, 2, 2]`, etc.

### Checkpoint Generation

Each run generates three checkpoint values called `turn_values`.

Rules:

1. All checkpoint values are within `1 .. target_distance`
2. All three checkpoint values are unique
3. All three checkpoint values are sorted in ascending order
4. The third checkpoint is always equal to `target_distance`

Examples:

- `target_distance = 3` -> `[1, 2, 3]`
- `target_distance = 6` -> `[1, 4, 6]`, `[2, 3, 6]`
- `target_distance = 20` -> `[4, 11, 20]`

These values represent three checkpoints on the route.

### Stage Distance and Cumulative Distance

The player's three chosen numbers represent the distance walked in each stage.
Checks are performed using cumulative distance, not single-stage distance.

Example:

- `segments = [1, 4, 1]`

Cumulative distances:

- Stage 1: `1`
- Stage 2: `1 + 4 = 5`
- Stage 3: `1 + 4 + 1 = 6`

### Win/Lose Check

Let:

- stage distances be `[s1, s2, s3]`
- cumulative distances be `[d1, d2, d3]`
- checkpoint values be `[t1, t2, t3]`

Where:

- `d1 = s1`
- `d2 = s1 + s2`
- `d3 = s1 + s2 + s3`

Pass conditions:

- `d1 <= t1`
- `d2 <= t2`
- `d3 <= t3`

The comparison rule is `<=`.
Reaching the checkpoint exactly still counts as a pass.

### Fail Fast Rule

If any stage fails, the entire run ends immediately.
The system does not process later stages after the first failure.

Example:

- Stage 1 cumulative distance: `1`
- Stage 2 cumulative distance: `5`
- Stage 2 checkpoint: `4`
- Result: `5 > 4`

The player loses at stage 2 and stage 3 is not evaluated.

### Win Condition

The player wins only if all comparisons pass.

Because the last checkpoint is always equal to `target_distance`, a successful final stage means the player reaches the finish line without being caught.

### Reward Multiplier

Reward multiplier is based only on `target_distance`.
It does not depend on which valid three-stage split the player chose.

Current implementation uses a linear multiplier table:

- `3 -> 1.0x`
- `4 -> 1.2x`
- `5 -> 1.4x`
- ...
- `30 -> 6.4x`

### Single-Player API

Current endpoints:

- `GET /api/game/config`
- `GET /api/game/combinations/{distance}`
- `POST /api/game/start`
- `GET /api/game/{game_id}`

`POST /api/game/start` validates the input, generates checkpoints, settles the run immediately, and stores the result in memory.

### Frontend Behavior

The single-player mode is the main content on the homepage.

Current UI behavior:

- choose target distance with a slider
- choose one legal three-stage split
- start the run from the game display area
- preview cumulative checkpoint markers on the track
- animate the player stage by stage
- stop immediately on the failed stage
- show a collapsible `Latest Attempt` panel for detailed result review

The overhead hint and result panel display comparisons using:

- `<=` when passed
- `>` when failed

## Room Race

### Goal

Players create or join a room, add bots if needed, and race under red-light / green-light rules.

### Room Flow

1. host creates a room
2. other human players join by room code
3. bots may be added during room creation
4. host starts the race
5. players move during green light
6. moving during red light causes immediate failure
7. positions and results are synchronized in real time

### Multiplayer API

Current endpoints:

- `GET /api/rooms`
- `POST /api/rooms/create`
- `POST /api/rooms/{room_code}/join`
- `GET /api/rooms/{room_code}`
- `POST /api/rooms/{room_code}/start`
- `POST /api/rooms/{room_code}/players/{player_id}/move`
- `GET /ws/rooms/{room_code}`

### Multiplayer Frontend

The multiplayer entry points are currently exposed as buttons:

- `Create Room`
- `Open Rooms`

Both open modal dialogs instead of occupying homepage space permanently.

## Current Source of Truth

At the moment, the backend in `src/backend/main.py` is the source of truth for gameplay rules, and the frontend in `src/frontend/src/App.vue` mirrors that behavior visually.

Key rule summary:

1. single-player uses three stage distances
2. checks use cumulative distance
3. checkpoints are unique and ascending
4. the last checkpoint is always the finish distance
5. comparison rule is `<=`
6. failure ends the run immediately
7. frontend presentation is aligned with backend settlement
