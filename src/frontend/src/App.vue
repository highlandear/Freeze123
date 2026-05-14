<script>
const API_BASE = import.meta.env.VITE_API_BASE ?? "http://127.0.0.1:8000";
const STORAGE_KEY = "freeze123-room-session";

const translations = {
  en: {
    title: "Freeze123",
    subtitle:
      "Jump straight into the three-step challenge from the home screen, or scroll down for the room-based party mode.",
    roomMode: "Room Race",
    soloMode: "Three-Step Challenge",
    createRoom: "Create Room",
    openCreateRoom: "New Room",
    closeModal: "Close",
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
    leaveRoom: "Leave Room",
    loading: "Loading",
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
    challengeTitle: "Three-Step Challenge",
    challengeIntro:
      "Pick a target distance, choose one of the legal three-step splits, then compare your path against three random turn-backs.",
    targetDistance: "Target Distance",
    rewardMultiplier: "Reward",
    combinationsTitle: "Step Splits",
    chosenSplit: "Chosen Split",
    randomWindow: "Turn-Back Range",
    startChallenge: "Run This Attempt",
    challengeSummary:
      "Your three picks are stage distances. Each check compares cumulative distance against the matching turn-back point.",
    noCombinations: "No legal splits yet.",
    latestAttempt: "Latest Attempt",
    showDetails: "Show Details",
    hideDetails: "Hide Details",
    attemptPending: "Pick a split and start a run to see the result here.",
    systemTurns: "Turn-Back Numbers",
    comparisons: "Step Checks",
    challengeWin: "You cleared all three looks.",
    challengeLose: "One of the steps got caught.",
    splitSeparator: " / ",
    passed: "Safe",
    failed: "Caught",
    challengeError: "Could not start the challenge.",
    configError: "Could not load challenge config.",
    comparisonRule: "Strictly lower wins",
    english: "English",
    chinese: "中文",
  },
  zh: {
    title: "一二三木头人",
    subtitle: "你可以继续玩联机房间模式，也可以切到三段闯关，直接做一局纯策略概率挑战。",
    roomMode: "房间竞速",
    soloMode: "一二三木头人",
    createRoom: "创建房间",
    openCreateRoom: "新建房间",
    closeModal: "关闭",
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
    leaveRoom: "离开房间",
    loading: "请稍候",
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
    challengeTitle: "一二三木头人",
    challengeIntro: "先选目标距离，再从合法三段组合里挑一种，然后和木头人的三次回头数值逐段对比。",
    targetDistance: "目标距离",
    rewardMultiplier: "奖励倍率",
    combinationsTitle: "三段组合",
    chosenSplit: "当前选择",
    randomWindow: "回头随机范围",
    startChallenge: "开始这一局",
    challengeSummary: "只要三段都严格小于对应的回头数值，你就能赢。",
    noCombinations: "当前没有可用组合。",
    latestAttempt: "最近一局",
    showDetails: "展开详情",
    hideDetails: "收起详情",
    attemptPending: "先选一个组合并开始挑战，结果会显示在这里。",
    systemTurns: "木头人回头数值",
    comparisons: "逐段判定",
    challengeWin: "三段都安全通过，挑战成功。",
    challengeLose: "有一段被抓到，这局失败。",
    splitSeparator: " / ",
    passed: "安全",
    failed: "被抓",
    challengeError: "开始挑战失败。",
    configError: "加载闯关配置失败。",
    comparisonRule: "必须严格小于才算通过",
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

function splitToText(segments, separator = " / ") {
  return segments.join(separator);
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
      showJoinRoomsModal: false,
      gameConfig: null,
      gameCombinations: [],
      selectedDistance: 6,
      selectedSegments: null,
      latestAttempt: null,
      latestAttemptExpanded: false,
      challengePlayback: {
        phase: "idle",
        progressPercent: 0,
        currentStepIndex: -1,
        currentSegment: null,
        currentDistance: null,
        currentTurn: null,
        currentPassed: null,
        result: null,
      },
      challengeTimers: [],
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
      if (this.error && this.hasRoom) return this.error;
      if (!this.hasRoom) return this.t.noSession;
      if (this.room.room_status === "waiting") return this.t.gameWaiting;
      if (this.myPlayer?.status === "won") return this.t.resultWon.replace("{place}", this.myPlace ?? "-");
      if (this.myPlayer?.status === "lost") return this.t.resultLost.replace("{place}", this.myPlace ?? "-");
      return this.t.gameRunning;
    },
    selectedSegmentsText() {
      if (!this.selectedSegments) return "-";
      return splitToText(this.selectedSegments, this.t.splitSeparator);
    },
    selectedMultiplier() {
      if (!this.gameConfig) return "-";
      return `${this.gameConfig.distance_multipliers[String(this.selectedDistance)] ?? "-"}x`;
    },
    challengeSummaryText() {
      return this.language === "zh"
        ? "你选的是每阶段距离，判定时会用累计路程与对应回头点比较，累计路程小于等于回头点即可通过。"
        : "Your picks are stage distances. Each check compares cumulative distance to the matching checkpoint, and passing means cumulative distance is less than or equal to it.";
    },
    turnRangeText() {
      if (!this.gameConfig) return "-";
      return `${this.gameConfig.random_min} - ${this.selectedDistance}`;
    },
    comparisonRuleText() {
      return this.language === "zh"
        ? "累计路程小于等于回头点即可通过"
        : "Cumulative distance must stay at or before the checkpoint";
    },
    soloArenaClass() {
      if (this.challengePlayback.phase === "green") return "green";
      if (this.challengePlayback.phase === "red") return "red";
      if (this.challengePlayback.result === "win") return "green";
      if (this.challengePlayback.result === "lose") return "red";
      return "idle";
    },
    soloPreviewMarkers() {
      const segments = this.selectedSegments ?? [];
      let cumulative = 0;
      return segments.map((segment, index) => {
        cumulative += segment;
        return {
          index,
          segment,
          cumulative,
          left: `${Math.min(100, Math.round((cumulative / this.selectedDistance) * 100))}%`,
        };
      });
    },
    soloRunnerLeft() {
      return `${this.challengePlayback.progressPercent}%`;
    },
    soloRunnerStatus() {
      if (this.challengePlayback.result === "win") return "won";
      if (this.challengePlayback.result === "lose") return "lost";
      return "running";
    },
    soloRunnerFace() {
      if (this.challengePlayback.result === "win") return "^_^";
      if (this.challengePlayback.result === "lose") return "x_x";
      return ":)";
    },
    soloRunnerGesture() {
      if (
        this.challengePlayback.currentSegment !== null &&
        this.challengePlayback.currentTurn !== null &&
        this.challengePlayback.currentDistance !== null
      ) {
        const operator = this.challengePlayback.currentPassed === false ? ">" : "<=";
        return `${this.challengePlayback.currentDistance} ${operator} ${this.challengePlayback.currentTurn}`;
      }
      if (this.challengePlayback.currentDistance !== null) {
        return `${this.challengePlayback.currentDistance}m`;
      }
      return this.selectedSegmentsText;
    },
  },
  watch: {
    selectedDistance() {
      this.fetchGameCombinations();
    },
  },
  async mounted() {
    window.addEventListener("keydown", this.handleKeydown);
    await Promise.all([this.restoreSession(), this.fetchGameConfig()]);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
    this.cleanupSocket();
    this.clearChallengePlaybackTimers();
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
    async openJoinRoomsModal() {
      this.showJoinRoomsModal = true;
      this.error = "";
      await this.fetchRoomList();
    },
    closeJoinRoomsModal() {
      this.showJoinRoomsModal = false;
    },
    clearChallengePlaybackTimers() {
      this.challengeTimers.forEach((timer) => window.clearTimeout(timer));
      this.challengeTimers = [];
    },
    resetChallengePlayback() {
      this.clearChallengePlaybackTimers();
      this.challengePlayback = {
        phase: "idle",
        progressPercent: 0,
        currentStepIndex: -1,
        currentSegment: null,
        currentDistance: null,
        currentTurn: null,
        currentPassed: null,
        result: null,
      };
    },
    queueChallengePlayback(callback, delayMs) {
      const timer = window.setTimeout(callback, delayMs);
      this.challengeTimers.push(timer);
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
    async fetchGameConfig() {
      try {
        const response = await fetch(`${API_BASE}/api/game/config`);
        this.gameConfig = await this.readResponse(response);
        if (this.selectedDistance < this.gameConfig.min_distance || this.selectedDistance > this.gameConfig.max_distance) {
          this.selectedDistance = this.gameConfig.min_distance;
        }
        await this.fetchGameCombinations();
      } catch {
        this.error = this.t.configError;
      }
    },
    async fetchGameCombinations() {
      if (!this.gameConfig) return;
      try {
        const response = await fetch(`${API_BASE}/api/game/combinations/${this.selectedDistance}`);
        const payload = await this.readResponse(response);
        this.gameCombinations = payload.combinations;
        this.selectedSegments = this.gameCombinations[0] ?? null;
        this.resetChallengePlayback();
      } catch {
        this.gameCombinations = [];
        this.selectedSegments = null;
        this.resetChallengePlayback();
      }
    },
    pickSegments(segments) {
      this.selectedSegments = segments;
      this.error = "";
      this.resetChallengePlayback();
    },
    playChallengeAttempt(attempt) {
      this.resetChallengePlayback();
      let cumulativeDistance = 0;
      let timelineOffset = 150;

      for (const [index, comparison] of attempt.comparisons.entries()) {
        cumulativeDistance += attempt.segments[index];
        const progressPercent = Math.min(
          100,
          Math.round((cumulativeDistance / attempt.target_distance) * 100),
        );

        this.queueChallengePlayback(() => {
          this.challengePlayback = {
            ...this.challengePlayback,
            phase: "green",
            currentStepIndex: index,
            currentSegment: attempt.segments[index],
            currentDistance: comparison.player,
            currentTurn: null,
            currentPassed: null,
            progressPercent,
            result: null,
          };
        }, timelineOffset);

        timelineOffset += 650;

        this.queueChallengePlayback(() => {
          this.challengePlayback = {
            ...this.challengePlayback,
            phase: "red",
            currentStepIndex: index,
            currentSegment: attempt.segments[index],
            currentDistance: comparison.player,
            currentTurn: comparison.turn,
            currentPassed: comparison.passed,
            progressPercent,
            result: comparison.passed ? null : "lose",
          };
        }, timelineOffset);

        timelineOffset += comparison.passed ? 550 : 700;

        if (!comparison.passed) {
          break;
        }
      }

      this.queueChallengePlayback(() => {
        this.challengePlayback = {
          ...this.challengePlayback,
          phase: "idle",
          result: attempt.result,
          currentDistance:
            attempt.result === "win"
              ? attempt.target_distance
              : this.challengePlayback.currentDistance,
          currentTurn:
            attempt.result === "win"
              ? attempt.turn_values.at(-1) ?? null
              : this.challengePlayback.currentTurn,
          currentPassed:
            attempt.result === "win" ? true : this.challengePlayback.currentPassed,
          progressPercent:
            attempt.result === "win" ? 100 : this.challengePlayback.progressPercent,
        };
      }, timelineOffset);
    },
    async startChallenge() {
      if (!this.selectedSegments) return;
      this.loading = true;
      this.error = "";
      try {
        const response = await fetch(`${API_BASE}/api/game/start`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            target_distance: this.selectedDistance,
            segments: this.selectedSegments,
          }),
        });
        this.latestAttempt = await this.readResponse(response);
        this.latestAttemptExpanded = false;
        this.playChallengeAttempt(this.latestAttempt);
      } catch {
        this.error = this.t.challengeError;
      } finally {
        this.loading = false;
      }
    },
    toggleLatestAttempt() {
      if (!this.latestAttempt) return;
      this.latestAttemptExpanded = !this.latestAttemptExpanded;
    },
    formatSegments(segments) {
      return splitToText(segments, this.t.splitSeparator);
    },
    async readResponse(response) {
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      return response.json();
    },
    handleKeydown(event) {
      if (event.code === "Escape") {
        if (this.showCreateModal) {
          event.preventDefault();
          this.closeCreateRoomModal();
        }
        if (this.showJoinRoomsModal) {
          event.preventDefault();
          this.closeJoinRoomsModal();
        }
      }
      if (event.code === "Space" || event.code === "ArrowRight") {
        if (!this.hasRoom) return;
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
        <p class="eyebrow">{{ language === 'zh' ? '一二三木头人' : 'Freeze123' }}</p>
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
        <button
          v-if="!hasRoom"
          class="secondary"
          type="button"
          @click="openCreateRoomModal"
        >
          {{ t.openCreateRoom }}
        </button>
        <button
          v-if="!hasRoom"
          class="secondary"
          type="button"
          @click="openJoinRoomsModal"
        >
          {{ t.availableRooms }}
        </button>
        <button v-else-if="hasRoom" class="secondary" type="button" @click="leaveRoom">
          {{ t.leaveRoom }}
        </button>
      </div>
    </section>

    <template v-if="!hasRoom">
    <section class="challenge-grid homepage-grid">
      <article class="entry-card challenge-setup-card">
        <h2>{{ t.challengeTitle }}</h2>
        <p class="card-copy">{{ t.challengeIntro }}</p>

        <div class="stat-grid compact-stats">
          <div>
            <span class="label">{{ t.targetDistance }}</span>
            <strong>{{ selectedDistance }}</strong>
          </div>
          <div>
            <span class="label">{{ t.rewardMultiplier }}</span>
            <strong>{{ selectedMultiplier }}</strong>
          </div>
          <div>
            <span class="label">{{ t.randomWindow }}</span>
            <strong>{{ turnRangeText }}</strong>
          </div>
          <div>
            <span class="label">{{ t.currentCall }}</span>
            <strong>{{ comparisonRuleText }}</strong>
          </div>
        </div>

        <label class="field">
          <span>{{ t.targetDistance }}</span>
          <input
            v-model.number="selectedDistance"
            type="range"
            :min="gameConfig?.min_distance ?? 3"
            :max="gameConfig?.max_distance ?? 30"
          />
        </label>

        <div class="distance-scale">
          <span>{{ gameConfig?.min_distance ?? 3 }}</span>
          <strong>{{ selectedDistance }}</strong>
          <span>{{ gameConfig?.max_distance ?? 30 }}</span>
        </div>

      </article>

      <article class="entry-card combo-card">
        <h2>{{ t.combinationsTitle }}</h2>
        <div v-if="gameCombinations.length" class="combo-list">
          <button
            v-for="segments in gameCombinations"
            :key="segments.join('-')"
            class="combo-chip"
            :class="{ active: selectedSegments && segments.join('-') === selectedSegments.join('-') }"
            type="button"
            @click="pickSegments(segments)"
          >
            {{ formatSegments(segments) }}
          </button>
        </div>
        <p v-else class="room-list-empty">{{ t.noCombinations }}</p>
      </article>

      <section class="arena solo-arena" :class="soloArenaClass">
        <div class="skyline">
          <span></span>
          <span></span>
          <span></span>
        </div>

        <div class="doll" :class="soloArenaClass">
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
            v-for="marker in soloPreviewMarkers"
            :key="`solo-lane-${marker.index}`"
            class="lane"
            :style="{ bottom: `${marker.index * 70}px` }"
          ></div>
          <div
            v-for="marker in soloPreviewMarkers"
            :key="`solo-marker-${marker.index}`"
            class="solo-marker"
            :style="{ left: marker.left }"
          >
            <span>{{ marker.cumulative }}m</span>
          </div>
          <div
            class="runner solo-runner"
            :class="[soloRunnerStatus, 'human']"
            :style="{ left: soloRunnerLeft, bottom: '24px' }"
          >
            <span class="gesture">{{ soloRunnerGesture }}</span>
            <span class="runner-tag">
              {{
                challengePlayback.currentDistance === null
                  ? selectedSegmentsText
                  : challengePlayback.currentTurn === null
                    ? `${challengePlayback.currentDistance}m`
                    : challengePlayback.result === 'lose'
                      ? t.failed
                      : t.passed
              }}
            </span>
            <span class="arm left-arm"></span>
            <span class="arm right-arm"></span>
            <span class="player-head"></span>
            <span class="player-face">{{ soloRunnerFace }}</span>
            <span class="player-body"></span>
            <span class="runner-name">Player</span>
          </div>
        </div>

        <div class="start-line">{{ t.startLine }}</div>
        <button
          class="primary solo-start-button"
          type="button"
          :disabled="loading || !selectedSegments"
          @click="startChallenge"
        >
          {{ loading ? t.loading : t.startChallenge }}
        </button>
      </section>

      <article class="entry-card challenge-result-card">
        <div class="card-head">
          <div>
            <h2>{{ t.latestAttempt }}</h2>
          </div>
          <button
            v-if="latestAttempt"
            class="ghost-action"
            type="button"
            @click="toggleLatestAttempt"
          >
            {{ latestAttemptExpanded ? t.hideDetails : t.showDetails }}
          </button>
        </div>
        <template v-if="latestAttempt">
          <div class="result-box" :class="latestAttempt.result">
            <span class="label">{{ t.result }}</span>
            <strong>{{ latestAttempt.result === 'win' ? t.challengeWin : t.challengeLose }}</strong>
            <p>{{ t.rewardMultiplier }}: {{ latestAttempt.multiplier }}x</p>
          </div>

          <div v-if="latestAttemptExpanded" class="attempt-expanded">
            <div class="attempt-detail-grid">
              <div class="attempt-detail-card">
                <span class="label">{{ t.chosenSplit }}</span>
                <strong>{{ formatSegments(latestAttempt.segments) }}</strong>
              </div>
              <div class="attempt-detail-card">
                <span class="label">{{ t.systemTurns }}</span>
                <strong>{{ formatSegments(latestAttempt.turn_values) }}</strong>
              </div>
            </div>

            <div class="leaderboard-card comparison-card">
              <span class="label">{{ t.comparisons }}</span>
              <div class="leaderboard-list">
                <div
                  v-for="comparison in latestAttempt.comparisons"
                  :key="comparison.index"
                  class="leader-row"
                  :class="comparison.passed ? 'won' : 'lost'"
                >
                  <div class="leader-main">
                    <strong>#{{ comparison.index }}</strong>
                    <span>
                      {{ comparison.player }}m
                      {{ comparison.passed ? '<=' : '>' }}
                      {{ comparison.turn }}m
                    </span>
                  </div>
                  <div class="leader-meta">
                    <span>{{ comparison.passed ? t.passed : t.failed }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
        <p v-else class="room-list-empty">{{ t.attemptPending }}</p>
      </article>
    </section>

    </template>

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
            {{ loading ? t.loading : t.roomMode }}
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

    <div v-if="showJoinRoomsModal && !hasRoom" class="modal-backdrop" @click.self="closeJoinRoomsModal">
      <section class="modal-card room-list-card" role="dialog" aria-modal="true" :aria-label="t.availableRooms">
        <div class="modal-head">
          <div>
            <h2>{{ t.availableRooms }}</h2>
          </div>
          <button class="ghost-action" type="button" @click="closeJoinRoomsModal">
            {{ t.closeModal }}
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
        <div class="card-head">
          <span class="label">{{ t.availableRooms }}</span>
          <button class="secondary compact" type="button" :disabled="loading" @click="fetchRoomList">
            {{ t.refreshRooms }}
          </button>
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
                <span>{{ t.difficulty }} {{ t[listedRoom.bot_difficulty] ?? listedRoom.bot_difficulty }}</span>
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
      </section>
    </div>
  </main>
</template>
