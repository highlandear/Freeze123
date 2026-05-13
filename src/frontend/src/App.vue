<script>
const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";
const STORAGE_KEY = "freeze123-room-session";

const translations = {
  en: {
    title: "Red Light, Green Light",
    subtitle:
      "Create a room, bring in real players, then fill the rest with bots that actually feel different.",
    createRoom: "Create Room",
    openCreateRoom: "New Room",
    closeModal: "Close",
    joinRoom: "Join Room",
    availableRooms: "Open Rooms",
    browseRooms: "Browse joinable rooms and jump in without sharing a code first.",
    joinPrompt: "Choose your player name once, then join any room below.",
    refreshRooms: "Refresh Rooms",
    noRooms: "No joinable rooms yet. Create one to get the lobby started.",
    roomHost: "Host",
    roomHumans: "Humans",
    roomBots: "Bots",
    roomSlots: "Players",
    quickJoin: "Join This Room",
    startRace: "Start Race",
    leaveRoom: "Leave Room",
    loading: "Loading",
    roomCode: "Room Code",
    playerName: "Player Name",
    difficulty: "Bot Difficulty",
    botCount: "Bot Count",
    easy: "Easy",
    normal: "Normal",
    hard: "Hard",
    waitingRoom: "Waiting Room",
    roomReady: "Share the room code and start when everyone is ready.",
    currentCall: "Current Call",
    waiting: "Waiting",
    idle: "Lobby",
    greenLight: "Green Light",
    redLight: "Red Light",
    roomStatus: "Room",
    running: "Running",
    finished: "Finished",
    ready: "Ready",
    progress: "Progress",
    moves: "Moves",
    place: "Place",
    racers: "Racers",
    leaderboard: "Leaderboard",
    result: "Result",
    finishedLabel: "Finished",
    lostLabel: "Out",
    runningLabel: "On Track",
    waitingLabel: "Waiting",
    watcher: "Watcher",
    finish: "Finish",
    startLine: "Start",
    moveButton: "Move 10m",
    moveHint: "Space or Right Arrow to move",
    hostBadge: "Host",
    youBadge: "You",
    botBadge: "BOT",
    humanBadge: "Human",
    placeFmt: "#{place}",
    gameWon: "Finished",
    gameLost: "Caught",
    gameRunning: "Keep moving only on green.",
    gameWaiting: "Waiting for the host to start.",
    resultWon: "You finished in place #{place}.",
    resultLost: "You were caught. Final place #{place}.",
    resultWaiting: "The room is still gathering players.",
    createError: "Could not create the room.",
    joinError: "Could not join the room.",
    startError: "Could not start the room.",
    moveError: "Could not submit the move.",
    restoreError: "Could not restore the last room session.",
    roomPlayers: "Players in Room",
    noSession: "Create a room or join one with a room code.",
    english: "English",
    chinese: "中文",
  },
  zh: {
    title: "一二三木头人",
    subtitle: "现在可以真建房了。先拉真人进房，再用不同难度的机器人把赛道补满。",
    createRoom: "创建房间",
    openCreateRoom: "新建房间",
    closeModal: "关闭",
    joinRoom: "加入房间",
    availableRooms: "可加入房间",
    browseRooms: "查看还没开赛的房间，不用先拿到房间号也能直接加入。",
    joinPrompt: "先设置你的昵称，然后从下面任选一个房间加入。",
    refreshRooms: "刷新房间",
    noRooms: "暂时还没有可加入的房间，可以先创建一个。",
    roomHost: "房主",
    roomHumans: "真人",
    roomBots: "机器人",
    roomSlots: "玩家数",
    quickJoin: "加入这个房间",
    startRace: "开始比赛",
    leaveRoom: "离开房间",
    loading: "请稍候",
    roomCode: "房间号",
    playerName: "玩家昵称",
    difficulty: "机器人难度",
    botCount: "机器人数量",
    easy: "简单",
    normal: "普通",
    hard: "困难",
    waitingRoom: "等待室",
    roomReady: "把房间号发给朋友，大家到齐后再开始。",
    currentCall: "当前口令",
    waiting: "等待中",
    idle: "大厅中",
    greenLight: "绿灯",
    redLight: "红灯",
    roomStatus: "房间状态",
    running: "进行中",
    finished: "已结束",
    ready: "准备中",
    progress: "进度",
    moves: "移动次数",
    place: "名次",
    racers: "参赛者",
    leaderboard: "排行榜",
    result: "本场结果",
    finishedLabel: "已完成",
    lostLabel: "出局",
    runningLabel: "比赛中",
    waitingLabel: "等待开始",
    watcher: "木头人",
    finish: "终点",
    startLine: "起点",
    moveButton: "前进 10 米",
    moveHint: "按 Space 或右方向键前进",
    hostBadge: "房主",
    youBadge: "你",
    botBadge: "BOT",
    humanBadge: "真人",
    placeFmt: "第 {place} 名",
    gameWon: "成功冲线",
    gameLost: "被抓到了",
    gameRunning: "只在绿灯时前进，稳住节奏。",
    gameWaiting: "等待房主开始比赛。",
    resultWon: "你以第 {place} 名完成比赛。",
    resultLost: "你被抓到了，最终排名第 {place} 名。",
    resultWaiting: "房间还在等人，准备好就能开跑。",
    createError: "创建房间失败。",
    joinError: "加入房间失败。",
    startError: "开始比赛失败。",
    moveError: "提交动作失败。",
    restoreError: "恢复上次房间失败。",
    roomPlayers: "房间成员",
    noSession: "你可以先创建房间，或者输入房间号加入。",
    english: "English",
    chinese: "中文",
  },
};

function websocketBaseUrl() {
  if (API_BASE.startsWith("http://")) return API_BASE.replace("http://", "ws://");
  if (API_BASE.startsWith("https://")) return API_BASE.replace("https://", "wss://");
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  return `${protocol}://127.0.0.1:8000`;
}

export default {
  data() {
    return {
      language: "zh",
      loading: false,
      error: "",
      room: null,
      roomList: [],
      session: null,
      socket: null,
      reconnectTimer: null,
      showCreateModal: false,
      createForm: {
        playerName: "",
        botCount: 2,
        botDifficulty: "normal",
      },
      joinForm: {
        playerName: "",
      },
    };
  },
  computed: {
    t() {
      return translations[this.language];
    },
    hasRoom() {
      return Boolean(this.room && this.session);
    },
    myPlayer() {
      if (!this.hasRoom) return null;
      return this.room.players.find((player) => player.player_id === this.session.playerId) ?? null;
    },
    isHost() {
      return this.hasRoom && this.room.host_player_id === this.session.playerId;
    },
    canStart() {
      return this.hasRoom && this.room.room_status === "waiting" && this.isHost && !this.loading;
    },
    canMove() {
      return (
        this.hasRoom &&
        this.room.room_status === "running" &&
        this.myPlayer?.status === "running" &&
        !this.loading
      );
    },
    lightText() {
      if (!this.hasRoom) return this.t.waiting;
      const map = {
        idle: this.t.idle,
        green: this.t.greenLight,
        red: this.t.redLight,
      };
      return map[this.room.light] ?? this.t.waiting;
    },
    lightClass() {
      if (!this.hasRoom) return "idle";
      return this.room.light;
    },
    roomStatusText() {
      if (!this.hasRoom) return this.t.waiting;
      const map = {
        waiting: this.t.ready,
        running: this.t.running,
        finished: this.t.finished,
      };
      return map[this.room.room_status] ?? this.room.room_status;
    },
    progressPercent() {
      return this.myPlayer?.progress_percent ?? 0;
    },
    moveCount() {
      return this.myPlayer?.move_count ?? 0;
    },
    myPlace() {
      return this.myPlayer?.place ?? null;
    },
    racerCount() {
      return this.room?.players.length ?? 0;
    },
    botDifficultyLabel() {
      if (!this.hasRoom) return "";
      return this.t[this.room.bot_difficulty] ?? this.room.bot_difficulty;
    },
    rankedPlayers() {
      if (!this.hasRoom) return [];
      return this.room.players.map((player, index) => ({
        ...player,
        laneIndex: index,
        left: `${player.progress_percent}%`,
        bottom: `${18 + index * 70}px`,
        face: player.status === "won" ? "^_^" : player.status === "lost" ? "x_x" : ":)",
        gesture: player.status === "won" ? this.t.gameWon : player.status === "lost" ? this.t.gameLost : "",
      }));
    },
    resultTitle() {
      if (!this.hasRoom) return this.t.waitingRoom;
      if (this.myPlayer?.status === "won") return this.t.gameWon;
      if (this.myPlayer?.status === "lost") return this.t.gameLost;
      if (this.room.room_status === "waiting") return this.t.waitingRoom;
      return this.t.running;
    },
    resultDetail() {
      if (!this.hasRoom) return this.t.noSession;
      if (this.myPlayer?.status === "won") {
        return this.t.resultWon.replace("{place}", this.myPlace ?? "-");
      }
      if (this.myPlayer?.status === "lost") {
        return this.t.resultLost.replace("{place}", this.myPlace ?? "-");
      }
      if (this.room.room_status === "waiting") return this.t.resultWaiting;
      return this.t.gameRunning;
    },
    controlMessage() {
      if (this.error) return this.error;
      if (!this.hasRoom) return this.t.noSession;
      if (this.room.room_status === "waiting") return this.t.gameWaiting;
      if (this.myPlayer?.status === "won") return this.t.resultWon.replace("{place}", this.myPlace ?? "-");
      if (this.myPlayer?.status === "lost") return this.t.resultLost.replace("{place}", this.myPlace ?? "-");
      return this.t.gameRunning;
    },
  },
  mounted() {
    window.addEventListener("keydown", this.handleKeydown);
    this.restoreSession();
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
    this.cleanupSocket();
    if (this.reconnectTimer) window.clearTimeout(this.reconnectTimer);
  },
  methods: {
    setLanguage(language) {
      this.language = language;
      this.error = "";
    },
    roomPlayerStatus(status) {
      const map = {
        waiting: this.t.waitingLabel,
        running: this.t.runningLabel,
        won: this.t.finishedLabel,
        lost: this.t.lostLabel,
      };
      return map[status] ?? status;
    },
    placeText(place) {
      if (!place) return "-";
      return this.t.placeFmt.replace("{place}", place);
    },
    persistSession() {
      if (!this.session) return;
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.session));
    },
    clearSession() {
      localStorage.removeItem(STORAGE_KEY);
      this.session = null;
      this.room = null;
    },
    cleanupSocket() {
      if (this.socket) {
        this.socket.onopen = null;
        this.socket.onmessage = null;
        this.socket.onclose = null;
        this.socket.onerror = null;
        this.socket.close();
        this.socket = null;
      }
    },
    async restoreSession() {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        await this.fetchRoomList();
        return;
      }

      try {
        this.session = JSON.parse(raw);
        await this.fetchRoom();
        this.connectSocket();
      } catch {
        this.error = this.t.restoreError;
        this.clearSession();
        await this.fetchRoomList();
      }
    },
    async handleSessionResponse(response, fallbackName) {
      const payload = await this.readResponse(response);
      this.room = payload.room;
      this.session = {
        playerId: payload.player_id,
        roomCode: payload.room.room_code,
        playerName: fallbackName,
      };
      this.persistSession();
      this.connectSocket();
    },
    openCreateRoomModal() {
      this.showCreateModal = true;
      this.error = "";
    },
    closeCreateRoomModal() {
      this.showCreateModal = false;
    },
    async createRoom() {
      this.loading = true;
      this.error = "";
      try {
        const playerName = this.createForm.playerName || this.joinForm.playerName || "Player";
        const response = await fetch(`${API_BASE}/api/rooms/create`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            player_name: playerName,
            bot_count: this.createForm.botCount,
            bot_difficulty: this.createForm.botDifficulty,
          }),
        });
        await this.handleSessionResponse(response, playerName);
        this.joinForm.playerName = playerName;
        this.roomList = [];
        this.showCreateModal = false;
      } catch {
        this.error = this.t.createError;
      } finally {
        this.loading = false;
      }
    },
    async joinRoom(roomCode) {
      this.loading = true;
      this.error = "";
      try {
        const response = await fetch(`${API_BASE}/api/rooms/${roomCode}/join`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            player_name: this.joinForm.playerName || "Player",
          }),
        });
        await this.handleSessionResponse(response, this.joinForm.playerName || "Player");
        this.roomList = [];
      } catch {
        this.error = this.t.joinError;
        await this.fetchRoomList();
      } finally {
        this.loading = false;
      }
    },
    async fetchRoomList() {
      if (this.hasRoom) return;
      try {
        const response = await fetch(`${API_BASE}/api/rooms`);
        this.roomList = await this.readResponse(response);
      } catch {
        this.roomList = [];
      }
    },
    async fetchRoom() {
      if (!this.session) return;
      const response = await fetch(
        `${API_BASE}/api/rooms/${this.session.roomCode}?player_id=${this.session.playerId}`,
      );
      this.room = await this.readResponse(response);
    },
    connectSocket() {
      if (!this.session) return;

      this.cleanupSocket();
      const url = `${websocketBaseUrl()}/ws/rooms/${this.session.roomCode}?player_id=${this.session.playerId}`;
      this.socket = new WebSocket(url);

      this.socket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        if (payload.type === "room_state") {
          this.room = payload.room;
        }
      };

      this.socket.onclose = () => {
        this.socket = null;
        if (!this.session) return;
        this.reconnectTimer = window.setTimeout(async () => {
          try {
            await this.fetchRoom();
            this.connectSocket();
          } catch {
            this.error = this.t.restoreError;
          }
        }, 1000);
      };
    },
    async startRoom() {
      if (!this.canStart) return;

      this.loading = true;
      this.error = "";
      try {
        const response = await fetch(`${API_BASE}/api/rooms/${this.room.room_code}/start`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ player_id: this.session.playerId }),
        });
        this.room = await this.readResponse(response);
      } catch {
        this.error = this.t.startError;
      } finally {
        this.loading = false;
      }
    },
    async movePlayer() {
      if (!this.canMove) return;

      this.loading = true;
      this.error = "";
      try {
        const response = await fetch(
          `${API_BASE}/api/rooms/${this.room.room_code}/players/${this.session.playerId}/move`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ distance: 10 }),
          },
        );
        this.room = await this.readResponse(response);
      } catch {
        this.error = this.t.moveError;
      } finally {
        this.loading = false;
      }
    },
    leaveRoom() {
      this.cleanupSocket();
      if (this.reconnectTimer) window.clearTimeout(this.reconnectTimer);
      this.error = "";
      this.clearSession();
      this.fetchRoomList();
    },
    async readResponse(response) {
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      return response.json();
    },
    handleKeydown(event) {
      if (event.code === "Escape" && this.showCreateModal) {
        event.preventDefault();
        this.closeCreateRoomModal();
      }
      if (event.code === "Space" || event.code === "ArrowRight") {
        event.preventDefault();
        this.movePlayer();
      }
      if (event.code === "Enter" && this.canStart) {
        event.preventDefault();
        this.startRoom();
      }
    },
  },
};
</script>

<template>
  <main class="app-shell">
    <section class="hero">
      <div class="hero-copy">
        <p class="eyebrow">Freeze123</p>
        <h1>{{ t.title }}</h1>
        <p class="subtitle">{{ t.subtitle }}</p>
      </div>
      <div class="hero-actions">
        <div class="language-toggle" aria-label="Language switcher">
          <button
            class="ghost"
            :class="{ active: language === 'en' }"
            type="button"
            @click="setLanguage('en')"
          >
            {{ t.english }}
          </button>
          <button
            class="ghost"
            :class="{ active: language === 'zh' }"
            type="button"
            @click="setLanguage('zh')"
          >
            {{ t.chinese }}
          </button>
        </div>
        <button v-if="!hasRoom" class="secondary" type="button" @click="openCreateRoomModal">
          {{ t.openCreateRoom }}
        </button>
        <button v-else class="secondary" type="button" @click="leaveRoom">
          {{ t.leaveRoom }}
        </button>
      </div>
    </section>

    <section v-if="!hasRoom" class="lobby-grid single-column">
      <article class="entry-card room-list-card">
        <div class="card-head">
          <div>
            <span class="label">{{ t.availableRooms }}</span>
            <h2>{{ t.availableRooms }}</h2>
          </div>
          <button class="secondary compact" type="button" :disabled="loading" @click="fetchRoomList">
            {{ t.refreshRooms }}
          </button>
        </div>
        <p class="card-copy">{{ t.browseRooms }}</p>
        <div class="form-stack join-inline">
          <label class="field">
            <span>{{ t.playerName }}</span>
            <input v-model="joinForm.playerName" type="text" maxlength="24" />
          </label>
          <p class="join-prompt">{{ t.joinPrompt }}</p>
        </div>
        <div v-if="roomList.length" class="room-list">
          <div v-for="listedRoom in roomList" :key="listedRoom.room_code" class="room-list-item">
            <div class="room-list-main">
              <div>
                <strong>{{ listedRoom.room_code }}</strong>
                <span>{{ t.roomHost }}: {{ listedRoom.host_name }}</span>
              </div>
              <div class="room-list-meta">
                <span>{{ t.roomHumans }} {{ listedRoom.human_count }}/4</span>
                <span>{{ t.roomBots }} {{ listedRoom.bot_count }}</span>
                <span>
                  {{ t.difficulty }}
                  {{ t[listedRoom.bot_difficulty] ?? listedRoom.bot_difficulty }}
                </span>
              </div>
            </div>
            <div class="room-list-actions">
              <span class="room-slots">{{ t.roomSlots }} {{ listedRoom.total_players }}</span>
              <button class="primary" type="button" :disabled="loading" @click="joinRoom(listedRoom.room_code)">
                {{ t.quickJoin }}
              </button>
            </div>
          </div>
        </div>
        <p v-else class="room-list-empty">{{ t.noRooms }}</p>
      </article>
    </section>

    <template v-else>
      <section class="room-banner">
        <div>
          <span class="label">{{ t.waitingRoom }}</span>
          <strong>{{ room.room_code }}</strong>
          <p>{{ t.roomReady }}</p>
        </div>
        <div class="room-badges">
          <span class="pill">{{ t.difficulty }}: {{ botDifficultyLabel }}</span>
          <span class="pill">{{ t.racers }}: {{ racerCount }}</span>
          <button
            v-if="canStart"
            class="primary"
            type="button"
            :disabled="loading"
            @click="startRoom"
          >
            {{ loading ? t.loading : t.startRace }}
          </button>
        </div>
      </section>

      <section class="game-layout">
        <aside class="side-panel">
          <div class="light-card" :class="lightClass">
            <span class="label">{{ t.currentCall }}</span>
            <strong>{{ lightText }}</strong>
            <div class="phase-bar covered" aria-hidden="true">
              <span class="mystery-fill"></span>
              <span class="cover-strip"></span>
            </div>
          </div>

          <div class="stat-grid">
            <div>
              <span class="label">{{ t.roomStatus }}</span>
              <strong>{{ roomStatusText }}</strong>
            </div>
            <div>
              <span class="label">{{ t.place }}</span>
              <strong>{{ placeText(myPlace) }}</strong>
            </div>
            <div>
              <span class="label">{{ t.progress }}</span>
              <strong>{{ progressPercent }}%</strong>
            </div>
            <div>
              <span class="label">{{ t.moves }}</span>
              <strong>{{ moveCount }}</strong>
            </div>
          </div>

          <div class="result-box" :class="myPlayer?.status || 'ready'">
            <span class="label">{{ t.result }}</span>
            <strong>{{ resultTitle }}</strong>
            <p>{{ resultDetail }}</p>
          </div>

          <div class="leaderboard-card">
            <span class="label">{{ t.roomPlayers }}</span>
            <div class="leaderboard-list">
              <div
                v-for="player in rankedPlayers"
                :key="player.player_id"
                class="leader-row"
                :class="[player.player_type, player.status]"
              >
                <div class="leader-main">
                  <strong>{{ player.name }}</strong>
                  <div class="inline-badges">
                    <span v-if="player.player_id === room.host_player_id" class="mini-pill">
                      {{ t.hostBadge }}
                    </span>
                    <span v-if="player.player_id === session.playerId" class="mini-pill accent">
                      {{ t.youBadge }}
                    </span>
                    <span v-else class="mini-pill">
                      {{ player.player_type === 'bot' ? t.botBadge : t.humanBadge }}
                    </span>
                  </div>
                </div>
                <div class="leader-meta">
                  <span>{{ placeText(player.place) }}</span>
                  <span>{{ player.progress_percent }}%</span>
                  <span>{{ roomPlayerStatus(player.status) }}</span>
                </div>
              </div>
            </div>
          </div>
        </aside>

        <section class="arena" :class="lightClass">
          <div class="skyline">
            <span></span>
            <span></span>
            <span></span>
          </div>

          <div class="doll" :class="lightClass">
            <div class="doll-head">
              <span class="hair"></span>
              <span class="eye"></span>
              <span class="eye"></span>
            </div>
            <div class="doll-body"></div>
            <strong>{{ t.watcher }}</strong>
          </div>

          <div class="finish-line">
            <span>{{ t.finish }}</span>
          </div>

          <div class="track track-grid">
            <div
              v-for="player in rankedPlayers"
              :key="`${player.player_id}-lane`"
              class="lane"
              :style="{ bottom: `${player.laneIndex * 70}px` }"
            ></div>
            <div
              v-for="player in rankedPlayers"
              :key="player.player_id"
              class="runner"
              :class="[player.status, player.player_type]"
              :style="{ left: player.left, bottom: player.bottom }"
            >
              <span v-if="player.gesture" class="gesture">{{ player.gesture }}</span>
              <span class="runner-tag">
                {{
                  player.player_id === session.playerId
                    ? t.youBadge
                    : player.player_type === 'bot'
                      ? t.botBadge
                      : t.humanBadge
                }}
              </span>
              <span class="arm left-arm"></span>
              <span class="arm right-arm"></span>
              <span class="player-head"></span>
              <span class="player-face">{{ player.face }}</span>
              <span class="player-body"></span>
              <span class="runner-name">{{ player.name }}</span>
            </div>
          </div>

          <div class="start-line">{{ t.startLine }}</div>
        </section>
      </section>

      <section class="controls">
        <button class="move" type="button" :disabled="!canMove" @click="movePlayer">
          {{ t.moveButton }}
        </button>
        <p>{{ controlMessage }}</p>
        <span class="shortcut">{{ t.moveHint }}</span>
      </section>
    </template>

    <div v-if="showCreateModal && !hasRoom" class="modal-backdrop" @click.self="closeCreateRoomModal">
      <section class="modal-card" role="dialog" aria-modal="true" :aria-label="t.createRoom">
        <div class="modal-head">
          <div>
            <span class="label">{{ t.createRoom }}</span>
            <h2>{{ t.createRoom }}</h2>
          </div>
          <button class="ghost-action" type="button" @click="closeCreateRoomModal">
            {{ t.closeModal }}
          </button>
        </div>
        <div class="form-stack">
          <label class="field">
            <span>{{ t.playerName }}</span>
            <input v-model="createForm.playerName" type="text" maxlength="24" />
          </label>
          <label class="field">
            <span>{{ t.botCount }}</span>
            <select v-model.number="createForm.botCount">
              <option :value="0">0</option>
              <option :value="1">1</option>
              <option :value="2">2</option>
              <option :value="3">3</option>
              <option :value="4">4</option>
            </select>
          </label>
          <label class="field">
            <span>{{ t.difficulty }}</span>
            <select v-model="createForm.botDifficulty">
              <option value="easy">{{ t.easy }}</option>
              <option value="normal">{{ t.normal }}</option>
              <option value="hard">{{ t.hard }}</option>
            </select>
          </label>
        </div>
        <button class="primary full" type="button" :disabled="loading" @click="createRoom">
          {{ loading ? t.loading : t.createRoom }}
        </button>
      </section>
    </div>
  </main>
</template>
