# API 文档

## `GET /health`

服务健康检查。

响应示例：

```json
{
  "status": "ok"
}
```

## `POST /api/game/start`

创建一局新游戏。

响应示例：

```json
{
  "game_id": "uuid",
  "status": "running",
  "light": "green",
  "player_position": 0,
  "finish_position": 100,
  "started_at": "2026-04-25T10:00:00+00:00",
  "light_started_at": "2026-04-25T10:00:00+00:00",
  "light_duration_seconds": 3.42,
  "ended_at": null,
  "move_count": 0,
  "message": "游戏开始，绿灯，可以前进！"
}
```

## `POST /api/game/{game_id}/action`

提交玩家动作。

请求示例：

```json
{
  "action": "move",
  "distance": 10
}
```

响应为最新游戏状态。红灯阶段移动会失败，绿灯阶段移动会推进玩家位置。

## `GET /api/game/{game_id}`

查询当前游戏状态。

响应为最新游戏状态。
