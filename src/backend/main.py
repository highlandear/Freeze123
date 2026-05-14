from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from random import choices, random, sample, uniform
from string import ascii_uppercase, digits
from typing import Any, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


FINISH_POSITION = 100
MOVE_STEP = 10
GREEN_SECONDS_RANGE = (2.0, 4.5)
RED_SECONDS_RANGE = (1.2, 3.2)
MAX_BOTS = 4
MAX_HUMANS = 4
ROOM_CODE_LENGTH = 6
BOT_NAMES = ("Bolt", "Pixel", "Comet", "Milo")
GAME_MIN_DISTANCE = 3
GAME_MAX_DISTANCE = 30
GAME_SEGMENT_COUNT = 3
GAME_TURN_MIN = 1

PlayerStatus = Literal["waiting", "running", "won", "lost"]
LightStatus = Literal["idle", "green", "red"]
RoomStatus = Literal["waiting", "running", "finished"]
PlayerType = Literal["human", "bot"]
BotDifficulty = Literal["easy", "normal", "hard"]
GameResult = Literal["win", "lose"]

BOT_PROFILES: dict[BotDifficulty, dict[str, tuple[float, float] | float]] = {
    "easy": {
        "reaction_seconds": (0.85, 1.35),
        "step_distance": (6, 10),
        "hesitation_chance": 0.24,
        "late_push_chance": 0.12,
    },
    "normal": {
        "reaction_seconds": (0.45, 0.9),
        "step_distance": (8, 12),
        "hesitation_chance": 0.1,
        "late_push_chance": 0.05,
    },
    "hard": {
        "reaction_seconds": (0.2, 0.55),
        "step_distance": (10, 14),
        "hesitation_chance": 0.03,
        "late_push_chance": 0.01,
    },
}


class PlayerState(BaseModel):
    player_id: str
    name: str
    player_type: PlayerType
    status: PlayerStatus
    position: int
    move_count: int
    finish_position: int
    progress_percent: int
    place: int | None = None
    ended_at: str | None = None
    message: str


class RoomState(BaseModel):
    room_id: str
    room_code: str
    room_status: RoomStatus
    host_player_id: str
    light: LightStatus
    finish_position: int
    started_at: str | None = None
    light_started_at: str | None = None
    light_duration_seconds: float | None = None
    bot_count: int
    bot_difficulty: BotDifficulty
    players: list[PlayerState]
    winner_ids: list[str] = Field(default_factory=list)


class SessionResponse(BaseModel):
    player_id: str
    room: RoomState


class RoomListItem(BaseModel):
    room_code: str
    room_status: RoomStatus
    host_name: str
    human_count: int
    bot_count: int
    total_players: int
    bot_difficulty: BotDifficulty


class CreateRoomRequest(BaseModel):
    player_name: str = Field(min_length=1, max_length=24)
    bot_count: int = Field(default=2, ge=0, le=MAX_BOTS)
    bot_difficulty: BotDifficulty = "normal"


class JoinRoomRequest(BaseModel):
    player_name: str = Field(min_length=1, max_length=24)


class StartRoomRequest(BaseModel):
    player_id: str


class MoveRequest(BaseModel):
    distance: int = Field(default=MOVE_STEP, ge=1, le=30)


class GameConfigResponse(BaseModel):
    min_distance: int
    max_distance: int
    segment_count: int
    comparison_rule: str
    random_min: int
    random_max: int
    distance_multipliers: dict[str, float]


class GameCombinationResponse(BaseModel):
    distance: int
    segment_count: int
    combinations: list[list[int]]


class StartGameRequest(BaseModel):
    target_distance: int = Field(ge=GAME_MIN_DISTANCE, le=GAME_MAX_DISTANCE)
    segments: list[int] = Field(min_length=GAME_SEGMENT_COUNT, max_length=GAME_SEGMENT_COUNT)


class GameComparison(BaseModel):
    index: int
    player: int
    turn: int
    passed: bool


class GameRoundResponse(BaseModel):
    game_id: str
    target_distance: int
    segments: list[int]
    turn_values: list[int]
    comparisons: list[GameComparison]
    result: GameResult
    multiplier: float
    created_at: str
    settled_at: str


app = FastAPI(title="Freeze123 API", version="0.3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms: dict[str, dict[str, Any]] = {}
room_locks: dict[str, asyncio.Lock] = {}
room_connections: dict[str, set[WebSocket]] = {}
room_tasks: dict[str, asyncio.Task] = {}
game_rounds: dict[str, dict[str, Any]] = {}

DISTANCE_MULTIPLIERS = {
    str(distance): round(1.0 + (distance - GAME_MIN_DISTANCE) * 0.2, 2)
    for distance in range(GAME_MIN_DISTANCE, GAME_MAX_DISTANCE + 1)
}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def as_iso(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def parse_iso(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def random_light_duration(light: LightStatus) -> float:
    low, high = GREEN_SECONDS_RANGE if light == "green" else RED_SECONDS_RANGE
    return round(uniform(low, high), 2)


def toggle_light(light: LightStatus) -> LightStatus:
    return "red" if light == "green" else "green"


def compute_progress(position: int, finish_position: int) -> int:
    return min(100, round((position / finish_position) * 100))


def generate_room_code() -> str:
    while True:
        room_code = "".join(choices(ascii_uppercase + digits, k=ROOM_CODE_LENGTH))
        if room_code not in rooms:
            return room_code


def clean_name(name: str) -> str:
    return name.strip()[:24]


def validate_game_segments(target_distance: int, segments: list[int]) -> None:
    if len(segments) != GAME_SEGMENT_COUNT:
        raise HTTPException(
            status_code=400,
            detail=f"segments must contain exactly {GAME_SEGMENT_COUNT} values",
        )
    if any(segment <= 0 for segment in segments):
        raise HTTPException(status_code=400, detail="segments must all be positive integers")
    if sum(segments) != target_distance:
        raise HTTPException(status_code=400, detail="segments must sum to target_distance")


def generate_distance_combinations(distance: int, parts: int = GAME_SEGMENT_COUNT) -> list[list[int]]:
    combinations: list[list[int]] = []

    def backtrack(remaining: int, slots_left: int, current: list[int]) -> None:
        if slots_left == 1:
            if remaining > 0:
                combinations.append([*current, remaining])
            return

        max_value = remaining - (slots_left - 1)
        for value in range(1, max_value + 1):
            backtrack(remaining - value, slots_left - 1, [*current, value])

    backtrack(distance, parts, [])
    return combinations


def build_turn_values(target_distance: int) -> list[int]:
    if target_distance == GAME_SEGMENT_COUNT:
        return list(range(GAME_TURN_MIN, target_distance + 1))

    checkpoints = sample(range(GAME_TURN_MIN, target_distance), GAME_SEGMENT_COUNT - 1)
    return [*sorted(checkpoints), target_distance]


def get_distance_multiplier(distance: int) -> float:
    return float(DISTANCE_MULTIPLIERS[str(distance)])


def settle_game_round(target_distance: int, segments: list[int]) -> dict[str, Any]:
    validate_game_segments(target_distance, segments)
    turn_values = build_turn_values(target_distance)
    comparisons = []
    cumulative_distance = 0
    for index, (segment, turn_value) in enumerate(zip(segments, turn_values, strict=True)):
        cumulative_distance += segment
        passed = cumulative_distance <= turn_value
        comparisons.append(
            {
                "index": index + 1,
                "player": cumulative_distance,
                "turn": turn_value,
                "passed": passed,
            }
        )
        if not passed:
            break
    result: GameResult = "win" if all(item["passed"] for item in comparisons) else "lose"
    timestamp = now_utc()
    return {
        "game_id": str(uuid4()),
        "target_distance": target_distance,
        "segments": segments,
        "turn_values": turn_values,
        "comparisons": comparisons,
        "result": result,
        "multiplier": get_distance_multiplier(target_distance),
        "created_at": as_iso(timestamp),
        "settled_at": as_iso(timestamp),
    }


def serialize_game_round(game_round: dict[str, Any]) -> GameRoundResponse:
    return GameRoundResponse(
        game_id=game_round["game_id"],
        target_distance=game_round["target_distance"],
        segments=game_round["segments"],
        turn_values=game_round["turn_values"],
        comparisons=[GameComparison(**comparison) for comparison in game_round["comparisons"]],
        result=game_round["result"],
        multiplier=game_round["multiplier"],
        created_at=game_round["created_at"],
        settled_at=game_round["settled_at"],
    )


def build_human_player(name: str, seat: int) -> dict[str, Any]:
    return {
        "player_id": str(uuid4()),
        "name": clean_name(name) or "Player",
        "player_type": "human",
        "status": "waiting",
        "position": 0,
        "move_count": 0,
        "finish_position": FINISH_POSITION,
        "progress_percent": 0,
        "place": None,
        "ended_at": None,
        "message": "Waiting in the lobby.",
        "seat": seat,
    }


def build_bot_player(name: str, seat: int, difficulty: BotDifficulty) -> dict[str, Any]:
    profile = BOT_PROFILES[difficulty]
    return {
        "player_id": str(uuid4()),
        "name": name,
        "player_type": "bot",
        "status": "waiting",
        "position": 0,
        "move_count": 0,
        "finish_position": FINISH_POSITION,
        "progress_percent": 0,
        "place": None,
        "ended_at": None,
        "message": f"{difficulty.title()} bot is ready.",
        "seat": seat,
        "difficulty": difficulty,
        "reaction_window": profile["reaction_seconds"],
        "step_window": profile["step_distance"],
        "hesitation_chance": profile["hesitation_chance"],
        "late_push_chance": profile["late_push_chance"],
        "next_action_at": None,
    }


def create_room(host_name: str, bot_count: int, bot_difficulty: BotDifficulty) -> tuple[dict[str, Any], str]:
    room_code = generate_room_code()
    host = build_human_player(host_name, seat=1)
    players = [host]
    for index in range(bot_count):
        players.append(
            build_bot_player(BOT_NAMES[index], seat=index + 2, difficulty=bot_difficulty)
        )

    room = {
        "room_id": str(uuid4()),
        "room_code": room_code,
        "room_status": "waiting",
        "host_player_id": host["player_id"],
        "light": "idle",
        "finish_position": FINISH_POSITION,
        "started_at": None,
        "light_started_at": None,
        "light_duration_seconds": None,
        "bot_count": bot_count,
        "bot_difficulty": bot_difficulty,
        "players": players,
    }
    rooms[room_code] = room
    room_locks[room_code] = asyncio.Lock()
    room_connections[room_code] = set()
    return room, host["player_id"]


def get_room_or_404(room_code: str) -> dict[str, Any]:
    room = rooms.get(room_code.upper())
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


def get_player_or_404(room: dict[str, Any], player_id: str) -> dict[str, Any]:
    for player in room["players"]:
        if player["player_id"] == player_id:
            return player
    raise HTTPException(status_code=404, detail="Player not found in room")


def summarize_joinable_room(room: dict[str, Any]) -> RoomListItem:
    human_count = sum(1 for player in room["players"] if player["player_type"] == "human")
    host = get_player_or_404(room, room["host_player_id"])
    return RoomListItem(
        room_code=room["room_code"],
        room_status=room["room_status"],
        host_name=host["name"],
        human_count=human_count,
        bot_count=room["bot_count"],
        total_players=len(room["players"]),
        bot_difficulty=room["bot_difficulty"],
    )


def reset_player_for_race(player: dict[str, Any]) -> None:
    player["status"] = "running"
    player["position"] = 0
    player["move_count"] = 0
    player["progress_percent"] = 0
    player["place"] = None
    player["ended_at"] = None
    player["message"] = "On the track."
    if player["player_type"] == "bot":
        player["next_action_at"] = None


def sort_players(room: dict[str, Any]) -> list[dict[str, Any]]:
    if room["room_status"] == "waiting":
        return sorted(room["players"], key=lambda player: player["seat"])

    status_rank = {"won": 0, "running": 1, "lost": 2, "waiting": 3}
    max_time = datetime.max.replace(tzinfo=timezone.utc)
    return sorted(
        room["players"],
        key=lambda player: (
            status_rank[player["status"]],
            parse_iso(player["ended_at"]) or max_time,
            -player["position"],
            player["move_count"],
            player["seat"],
        ),
    )


def assign_places(room: dict[str, Any]) -> None:
    if room["room_status"] == "waiting":
        for player in room["players"]:
            player["place"] = None
        return

    for index, player in enumerate(sort_players(room), start=1):
        player["place"] = index


def room_has_active_racers(room: dict[str, Any]) -> bool:
    return any(player["status"] == "running" for player in room["players"])


def update_room_status(room: dict[str, Any]) -> None:
    if room["room_status"] == "waiting":
        assign_places(room)
        return

    room["room_status"] = "running" if room_has_active_racers(room) else "finished"
    assign_places(room)


def schedule_bot(bot: dict[str, Any], from_time: datetime) -> None:
    low, high = bot["reaction_window"]
    reaction_seconds = round(uniform(low, high), 2)
    bot["next_action_at"] = as_iso(from_time + timedelta(seconds=reaction_seconds))


def finish_player(player: dict[str, Any], status: Literal["won", "lost"], message: str, ended_at: datetime) -> None:
    player["status"] = status
    player["ended_at"] = as_iso(ended_at)
    player["message"] = message
    if player["player_type"] == "bot":
        player["next_action_at"] = None


def move_player(room: dict[str, Any], player: dict[str, Any], distance: int, action_time: datetime) -> None:
    if room["room_status"] != "running" or player["status"] != "running":
        return

    player["move_count"] += 1
    if room["light"] == "red":
        finish_player(player, "lost", "Moved during red light.", action_time)
        update_room_status(room)
        return

    player["position"] = min(player["finish_position"], player["position"] + distance)
    player["progress_percent"] = compute_progress(player["position"], player["finish_position"])
    if player["position"] >= player["finish_position"]:
        finish_player(player, "won", "Reached the finish line.", action_time)
    else:
        player["message"] = "Advanced safely."
    update_room_status(room)


def set_green_phase(room: dict[str, Any], start_time: datetime) -> None:
    room["light"] = "green"
    room["light_started_at"] = as_iso(start_time)
    room["light_duration_seconds"] = random_light_duration("green")
    for player in room["players"]:
        if player["status"] != "running":
            continue
        if player["player_type"] == "bot":
            player["message"] = "Bot is sprinting."
            schedule_bot(player, start_time)
        else:
            player["message"] = "Green light. Move now!"


def set_red_phase(room: dict[str, Any], start_time: datetime) -> None:
    room["light"] = "red"
    room["light_started_at"] = as_iso(start_time)
    room["light_duration_seconds"] = random_light_duration("red")
    for player in room["players"]:
        if player["status"] != "running":
            continue
        if player["player_type"] == "bot":
            player["next_action_at"] = None
            if random() < float(player["late_push_chance"]):
                finish_player(player, "lost", "Bot pushed too late and got caught.", start_time)
            else:
                player["message"] = "Bot froze in time."
        else:
            player["message"] = "Red light. Stay still!"
    update_room_status(room)


def toggle_phase(room: dict[str, Any], start_time: datetime) -> None:
    if room["light"] == "green":
        set_red_phase(room, start_time)
    else:
        set_green_phase(room, start_time)


def advance_world(room: dict[str, Any]) -> None:
    while room["room_status"] == "running":
        phase_start = parse_iso(room["light_started_at"])
        duration = room["light_duration_seconds"]
        if phase_start is None or duration is None:
            break

        phase_change_at = phase_start + timedelta(seconds=duration)
        current_time = now_utc()
        active_bots = [
            player
            for player in room["players"]
            if player["player_type"] == "bot"
            and player["status"] == "running"
            and player.get("next_action_at")
        ]

        next_bot_at = None
        if room["light"] == "green" and active_bots:
            next_bot_at = min(parse_iso(bot["next_action_at"]) for bot in active_bots)

        if current_time >= phase_change_at and (
            next_bot_at is None or phase_change_at <= next_bot_at
        ):
            toggle_phase(room, phase_change_at)
            continue

        if (
            room["light"] == "green"
            and next_bot_at is not None
            and current_time >= next_bot_at
            and next_bot_at < phase_change_at
        ):
            for bot in active_bots:
                if parse_iso(bot["next_action_at"]) != next_bot_at:
                    continue
                if random() < float(bot["hesitation_chance"]):
                    bot["message"] = "Bot hesitated."
                    schedule_bot(bot, next_bot_at)
                    continue
                step_low, step_high = bot["step_window"]
                step_distance = round(uniform(step_low, step_high))
                move_player(room, bot, int(step_distance), next_bot_at)
                if bot["status"] == "running" and room["light"] == "green":
                    schedule_bot(bot, next_bot_at)
            continue

        break


def serialize_room(room: dict[str, Any]) -> RoomState:
    assign_places(room)
    players = [
        PlayerState(
            player_id=player["player_id"],
            name=player["name"],
            player_type=player["player_type"],
            status=player["status"],
            position=player["position"],
            move_count=player["move_count"],
            finish_position=player["finish_position"],
            progress_percent=player["progress_percent"],
            place=player["place"],
            ended_at=player["ended_at"],
            message=player["message"],
        )
        for player in sort_players(room)
    ]
    return RoomState(
        room_id=room["room_id"],
        room_code=room["room_code"],
        room_status=room["room_status"],
        host_player_id=room["host_player_id"],
        light=room["light"],
        finish_position=room["finish_position"],
        started_at=room["started_at"],
        light_started_at=room["light_started_at"],
        light_duration_seconds=room["light_duration_seconds"],
        bot_count=room["bot_count"],
        bot_difficulty=room["bot_difficulty"],
        players=players,
        winner_ids=[player.player_id for player in players if player.status == "won"],
    )


async def broadcast_room_state(room_code: str, state: RoomState) -> None:
    dead_connections: list[WebSocket] = []
    for websocket in list(room_connections.get(room_code, set())):
        try:
            await websocket.send_json({"type": "room_state", "room": state.model_dump(mode="json")})
        except Exception:
            dead_connections.append(websocket)
    for websocket in dead_connections:
        room_connections.get(room_code, set()).discard(websocket)


async def push_room_state(room_code: str) -> RoomState:
    room = get_room_or_404(room_code)
    lock = room_locks[room_code.upper()]
    async with lock:
        advance_world(room)
        state = serialize_room(room)
    await broadcast_room_state(room_code.upper(), state)
    return state


async def room_ticker(room_code: str) -> None:
    room_code = room_code.upper()
    last_snapshot = ""
    try:
        while room_code in rooms:
            async with room_locks[room_code]:
                room = rooms.get(room_code)
                if room is None:
                    break
                advance_world(room)
                state = serialize_room(room)
                snapshot = state.model_dump_json()
                finished = room["room_status"] == "finished"
            if snapshot != last_snapshot:
                await broadcast_room_state(room_code, state)
                last_snapshot = snapshot
            if finished:
                break
            await asyncio.sleep(0.25)
    finally:
        room_tasks.pop(room_code, None)


def ensure_room_task(room_code: str) -> None:
    existing_task = room_tasks.get(room_code)
    if existing_task and not existing_task.done():
        return
    room_tasks[room_code] = asyncio.create_task(room_ticker(room_code))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/game/config", response_model=GameConfigResponse)
def get_game_config_endpoint() -> GameConfigResponse:
    return GameConfigResponse(
        min_distance=GAME_MIN_DISTANCE,
        max_distance=GAME_MAX_DISTANCE,
        segment_count=GAME_SEGMENT_COUNT,
        comparison_rule="less_than_or_equal",
        random_min=GAME_TURN_MIN,
        random_max=GAME_MAX_DISTANCE,
        distance_multipliers=DISTANCE_MULTIPLIERS,
    )


@app.get("/api/game/combinations/{distance}", response_model=GameCombinationResponse)
def get_game_combinations_endpoint(distance: int) -> GameCombinationResponse:
    if not GAME_MIN_DISTANCE <= distance <= GAME_MAX_DISTANCE:
        raise HTTPException(
            status_code=400,
            detail=f"distance must be between {GAME_MIN_DISTANCE} and {GAME_MAX_DISTANCE}",
        )

    return GameCombinationResponse(
        distance=distance,
        segment_count=GAME_SEGMENT_COUNT,
        combinations=generate_distance_combinations(distance),
    )


@app.post("/api/game/start", response_model=GameRoundResponse)
def start_game_endpoint(payload: StartGameRequest) -> GameRoundResponse:
    game_round = settle_game_round(
        target_distance=payload.target_distance,
        segments=payload.segments,
    )
    game_rounds[game_round["game_id"]] = game_round
    return serialize_game_round(game_round)


@app.get("/api/game/{game_id}", response_model=GameRoundResponse)
def get_game_round_endpoint(game_id: str) -> GameRoundResponse:
    game_round = game_rounds.get(game_id)
    if game_round is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return serialize_game_round(game_round)


@app.get("/api/rooms", response_model=list[RoomListItem])
async def list_rooms_endpoint() -> list[RoomListItem]:
    joinable_rooms = []
    for room in rooms.values():
        if room["room_status"] != "waiting":
            continue
        human_count = sum(1 for player in room["players"] if player["player_type"] == "human")
        if human_count >= MAX_HUMANS:
            continue
        joinable_rooms.append(summarize_joinable_room(room))

    return sorted(joinable_rooms, key=lambda room: room.room_code)


@app.post("/api/rooms/create", response_model=SessionResponse)
async def create_room_endpoint(payload: CreateRoomRequest) -> SessionResponse:
    room, player_id = create_room(
        host_name=payload.player_name,
        bot_count=payload.bot_count,
        bot_difficulty=payload.bot_difficulty,
    )
    state = serialize_room(room)
    return SessionResponse(player_id=player_id, room=state)


@app.post("/api/rooms/{room_code}/join", response_model=SessionResponse)
async def join_room_endpoint(room_code: str, payload: JoinRoomRequest) -> SessionResponse:
    room = get_room_or_404(room_code)
    room_code = room_code.upper()
    async with room_locks[room_code]:
        if room["room_status"] != "waiting":
            raise HTTPException(status_code=409, detail="Room already started")

        human_count = sum(1 for player in room["players"] if player["player_type"] == "human")
        if human_count >= MAX_HUMANS:
            raise HTTPException(status_code=409, detail="Room is full")

        player = build_human_player(payload.player_name, seat=len(room["players"]) + 1)
        player["message"] = "Joined the lobby."
        room["players"].append(player)
        state = serialize_room(room)

    await broadcast_room_state(room_code, state)
    return SessionResponse(player_id=player["player_id"], room=state)


@app.get("/api/rooms/{room_code}", response_model=RoomState)
async def get_room_endpoint(room_code: str, player_id: str | None = Query(default=None)) -> RoomState:
    room = get_room_or_404(room_code)
    room_code = room_code.upper()
    async with room_locks[room_code]:
        if player_id is not None:
            get_player_or_404(room, player_id)
        advance_world(room)
        return serialize_room(room)


@app.post("/api/rooms/{room_code}/start", response_model=RoomState)
async def start_room_endpoint(room_code: str, payload: StartRoomRequest) -> RoomState:
    room = get_room_or_404(room_code)
    room_code = room_code.upper()
    async with room_locks[room_code]:
        if room["room_status"] != "waiting":
            raise HTTPException(status_code=409, detail="Room already started")
        if payload.player_id != room["host_player_id"]:
            raise HTTPException(status_code=403, detail="Only the host can start the room")

        start_time = now_utc()
        room["room_status"] = "running"
        room["started_at"] = as_iso(start_time)
        room["light"] = "green"
        room["light_started_at"] = as_iso(start_time)
        room["light_duration_seconds"] = random_light_duration("green")
        for player in room["players"]:
            reset_player_for_race(player)
        set_green_phase(room, start_time)
        state = serialize_room(room)

    ensure_room_task(room_code)
    await broadcast_room_state(room_code, state)
    return state


@app.post("/api/rooms/{room_code}/players/{player_id}/move", response_model=RoomState)
async def move_player_endpoint(room_code: str, player_id: str, payload: MoveRequest) -> RoomState:
    room = get_room_or_404(room_code)
    room_code = room_code.upper()
    async with room_locks[room_code]:
        if room["room_status"] != "running":
            raise HTTPException(status_code=409, detail="Room is not running")

        advance_world(room)
        player = get_player_or_404(room, player_id)
        if player["player_type"] != "human":
            raise HTTPException(status_code=403, detail="Bots cannot be controlled")
        move_player(room, player, payload.distance, now_utc())
        state = serialize_room(room)

    await broadcast_room_state(room_code, state)
    return state


@app.websocket("/ws/rooms/{room_code}")
async def room_websocket(websocket: WebSocket, room_code: str, player_id: str | None = Query(default=None)) -> None:
    room_code = room_code.upper()
    room = rooms.get(room_code)
    if room is None:
        await websocket.close(code=4404)
        return

    if player_id is not None:
        try:
            get_player_or_404(room, player_id)
        except HTTPException:
            await websocket.close(code=4403)
            return

    await websocket.accept()
    room_connections.setdefault(room_code, set()).add(websocket)
    try:
        await push_room_state(room_code)
        while True:
            message = await websocket.receive_text()
            if message == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        room_connections.get(room_code, set()).discard(websocket)
    except Exception:
        room_connections.get(room_code, set()).discard(websocket)
        await websocket.close()
