# Freeze123

Freeze123 是一个基于 Vue 和 FastAPI 的“一二三木头人”小游戏原型。

当前版本采用本地前后端分离开发：

- 后端：FastAPI，运行在 `http://127.0.0.1:8000`
- 前端：Vue + Vite，运行在 `http://127.0.0.1:5173`
- 前端通过 Vite proxy 请求后端 API

## 当前功能

- 创建一局新游戏
- 自动切换绿灯和红灯
- 绿灯时允许玩家前进
- 红灯时移动会失败
- 到达终点后胜利
- 支持重新开始

## 环境要求

- Python 3.10+
- Node.js 18+
- npm

## 安装后端依赖

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 安装前端依赖

在项目根目录执行：

```powershell
npm run frontend:install
```

也可以进入前端目录安装：

```powershell
cd src\frontend
npm install
```

## 启动后端

打开一个 PowerShell 窗口，在项目根目录执行：

```powershell
.\scripts\run_backend.ps1
```

后端地址：

```text
http://127.0.0.1:8000
```

FastAPI 接口文档：

```text
http://127.0.0.1:8000/docs
```

## 启动前端

再打开一个 PowerShell 窗口，在项目根目录执行：

```powershell
.\scripts\run_frontend.ps1
```

也可以执行：

```powershell
npm run frontend:dev
```

前端游戏地址：

```text
http://127.0.0.1:5173
```

## 项目结构

```text
.
|-- docs/
|   |-- api.md
|   `-- requirements.md
|-- scripts/
|   |-- run_backend.ps1
|   `-- run_frontend.ps1
|-- src/
|   |-- backend/
|   |   |-- __init__.py
|   |   `-- main.py
|   `-- frontend/
|       |-- index.html
|       |-- package.json
|       |-- vite.config.js
|       `-- src/
|           |-- main.js
|           `-- styles.css
|-- package.json
`-- requirements.txt
```

## API 概览

- `GET /health`：健康检查
- `POST /api/game/start`：开始新游戏
- `POST /api/game/{game_id}/action`：提交玩家移动
- `GET /api/game/{game_id}`：查询游戏状态

## 说明

当前版本为了优先跑通本地原型，游戏运行时文案使用英文，避免 Windows 终端编码影响源码。中文产品文档仍保留在 `docs/requirements.md`。
