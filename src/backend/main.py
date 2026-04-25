from __future__ import annotations

from datetime import datetime, timezone
from random import uniform
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


FINISH_POSITION = 100
MOVE_STEP = 10
GREEN_SECONDS_RANGE = (2.0, 4.5)
RED_SECONDS_RANGE = (1.2, 3.2)

GameStatus = Literal["running", "won", "lost"]
LightStatus = Literal["green", "red"]


class GameState(BaseModel):
    game_id: str
    status: GameStatus
    light: LightStatus
    player_position: int
    finish_position: int
    started_at: str
    light_started_at: str
    light_duration_seconds: float
    ended_at: str | None = None
    move_count: int = 0
    message: str


class ActionRequest(BaseModel):
    action: Literal["move"] = "move"
    distance: int = Field(default=MOVE_STEP, ge=1, le=30)


app = FastAPI(title="Freeze123 API", version="0.1.0")

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

games: dict[str, GameState] = {}


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def as_iso(value: datetime) -> str:
    return value.isoformat()


def random_light_duration(light: LightStatus) -> float:
    low, high = GREEN_SECONDS_RANGE if light == "green" else RED_SECONDS_RANGE
    return round(uniform(low, high), 2)


def toggle_light(light: LightStatus) -> LightStatus:
    return "red" if light == "green" else "green"


def refresh_light(game: GameState) -> GameState:
    if game.status != "running":
        return game

    current_time = now_utc()
    light_started = datetime.fromisoformat(game.light_started_at)

    while (current_time - light_started).total_seconds() >= game.light_duration_seconds:
        light_started = light_started.timestamp() + game.light_duration_seconds
        light_started = datetime.fromtimestamp(light_started, timezone.utc)
        game.light = toggle_light(game.light)
        game.light_started_at = as_iso(light_started)
        game.light_duration_seconds = random_light_duration(game.light)

    game.message = (
        "Green light. Move now!"
        if game.light == "green"
        else "Red light. Stay still!"
    )
    return game


def public_state(game: GameState) -> GameState:
    return refresh_light(game)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/game/start", response_model=GameState)
def start_game() -> GameState:
    game_id = str(uuid4())
    started_at = now_utc()
    game = GameState(
        game_id=game_id,
        status="running",
        light="green",
        player_position=0,
        finish_position=FINISH_POSITION,
        started_at=as_iso(started_at),
        light_started_at=as_iso(started_at),
        light_duration_seconds=random_light_duration("green"),
        message="Game started. Green light. Move now!",
    )
    games[game_id] = game
    return public_state(game)


@app.post("/api/game/{game_id}/action", response_model=GameState)
def submit_action(game_id: str, action: ActionRequest) -> GameState:
    game = games.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")

    refresh_light(game)

    if game.status != "running":
        return game

    if action.action == "move" and action.distance > 0:
        game.move_count += 1

        if game.light == "red":
            game.status = "lost"
            game.ended_at = as_iso(now_utc())
            game.message = "You moved on red light. Game over."
            return game

        game.player_position = min(
            game.finish_position,
            game.player_position + action.distance,
        )

        if game.player_position >= game.finish_position:
            game.status = "won"
            game.ended_at = as_iso(now_utc())
            game.message = "You reached the finish line. You win!"
        else:
            game.message = "Nice move. Watch for red light!"

    return game


@app.get("/api/game/{game_id}", response_model=GameState)
def get_game(game_id: str) -> GameState:
    game = games.get(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail="Game not found")
    return public_state(game)
