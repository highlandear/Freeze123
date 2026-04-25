<script>
const API_BASE = import.meta.env.VITE_API_BASE ?? "";

const translations = {
  en: {
    title: "Red Light, Green Light",
    subtitle: "Sprint on green. Freeze on red. Reach the finish line before you get caught moving.",
    start: "Start Game",
    restart: "Restart",
    loading: "Loading",
    shortcut: "Enter to start / Space to move",
    currentCall: "Current Call",
    timerHidden: "Timer hidden",
    waiting: "Waiting",
    greenLight: "Green Light",
    redLight: "Red Light",
    status: "Status",
    notStarted: "Not Started",
    running: "Running",
    won: "Won",
    lost: "Lost",
    progress: "Progress",
    moves: "Moves",
    roundResult: "Round Result",
    ready: "Ready",
    inProgress: "In Progress",
    victory: "Victory",
    gameOver: "Game Over",
    readyDetail: "Start a new round when ready.",
    runningDetail: "of the track completed.",
    wonDetail: "You won in {moves} moves.",
    lostDetail: "Move {moves} happened during red light.",
    messageStart: "Press Start. Move on green light. Stop on red light.",
    messageWon: "You reached the finish line. You win!",
    messageLost: "You moved on red light. Try again.",
    messageGreen: "Move now!",
    messageRed: "Freeze. Do not move.",
    startError: "Could not start. Please make sure the FastAPI backend is running.",
    moveError: "Could not submit the move. Please try again.",
    syncError: "Could not sync game state.",
    watcher: "Watcher",
    finish: "Finish",
    startLine: "Start",
    moveButton: "Move 10m",
    howToPlay: "How to Play",
    howToPlayText: "Click Move or press Space only during green light.",
    win: "Win",
    winText: "Reach 100% progress to cross the finish line.",
    lose: "Lose",
    loseText: "Moving during red light ends the round immediately.",
    player: "Player",
    faceReady: ":)",
    faceWin: "^_^",
    faceLose: "x_x",
    gestureWin: "VICTORY",
    gestureLose: "CAUGHT",
    english: "English",
    chinese: "\u4e2d\u6587",
  },
  zh: {
    title: "\u4e00\u4e8c\u4e09\u6728\u5934\u4eba",
    subtitle: "\u7eff\u706f\u51b2\u523a\uff0c\u7ea2\u706f\u5b9a\u4f4f\u3002\u5230\u8fbe\u7ec8\u70b9\u5c31\u83b7\u80dc\uff0c\u7ea2\u706f\u4e71\u52a8\u5c31\u51fa\u5c40\u3002",
    start: "\u5f00\u59cb\u6e38\u620f",
    restart: "\u91cd\u65b0\u5f00\u59cb",
    loading: "\u8bf7\u7a0d\u5019",
    shortcut: "Enter \u5f00\u59cb / Space \u524d\u8fdb",
    currentCall: "\u5f53\u524d\u53e3\u4ee4",
    timerHidden: "\u8ba1\u65f6\u5df2\u9690\u85cf",
    waiting: "\u7b49\u5f85\u5f00\u59cb",
    greenLight: "\u7eff\u706f",
    redLight: "\u7ea2\u706f",
    status: "\u72b6\u6001",
    notStarted: "\u672a\u5f00\u59cb",
    running: "\u8fdb\u884c\u4e2d",
    won: "\u80dc\u5229",
    lost: "\u5931\u8d25",
    progress: "\u8fdb\u5ea6",
    moves: "\u79fb\u52a8\u6b21\u6570",
    roundResult: "\u672c\u5c40\u7ed3\u679c",
    ready: "\u51c6\u5907\u5c31\u7eea",
    inProgress: "\u6311\u6218\u8fdb\u884c\u4e2d",
    victory: "\u80dc\u5229",
    gameOver: "\u6e38\u620f\u7ed3\u675f",
    readyDetail: "\u51c6\u5907\u597d\u540e\u5f00\u59cb\u65b0\u7684\u4e00\u5c40\u3002",
    runningDetail: "\u8def\u7a0b\u5df2\u5b8c\u6210\u3002",
    wonDetail: "\u4f60\u7528 {moves} \u6b21\u79fb\u52a8\u5230\u8fbe\u7ec8\u70b9\u3002",
    lostDetail: "\u7b2c {moves} \u6b21\u79fb\u52a8\u53d1\u751f\u5728\u7ea2\u706f\u9636\u6bb5\u3002",
    messageStart: "\u70b9\u51fb\u5f00\u59cb\u3002\u7eff\u706f\u65f6\u524d\u8fdb\uff0c\u7ea2\u706f\u65f6\u505c\u4e0b\u3002",
    messageWon: "\u4f60\u6210\u529f\u5230\u8fbe\u7ec8\u70b9\uff0c\u80dc\u5229\uff01",
    messageLost: "\u4f60\u5728\u7ea2\u706f\u65f6\u79fb\u52a8\u4e86\uff0c\u518d\u6765\u4e00\u5c40\u5427\u3002",
    messageGreen: "\u73b0\u5728\u53ef\u4ee5\u524d\u8fdb\uff01",
    messageRed: "\u6728\u5934\u4eba\uff0c\u4e0d\u8981\u52a8\u3002",
    startError: "\u542f\u52a8\u5931\u8d25\uff0c\u8bf7\u786e\u8ba4 FastAPI \u540e\u7aef\u6b63\u5728\u8fd0\u884c\u3002",
    moveError: "\u63d0\u4ea4\u52a8\u4f5c\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u518d\u8bd5\u3002",
    syncError: "\u540c\u6b65\u6e38\u620f\u72b6\u6001\u5931\u8d25\u3002",
    watcher: "\u6728\u5934\u4eba",
    finish: "\u7ec8\u70b9",
    startLine: "\u8d77\u70b9",
    moveButton: "\u524d\u8fdb 10 \u7c73",
    howToPlay: "\u73a9\u6cd5",
    howToPlayText: "\u53ea\u80fd\u5728\u7eff\u706f\u9636\u6bb5\u70b9\u51fb\u524d\u8fdb\u6216\u6309 Space\u3002",
    win: "\u80dc\u5229",
    winText: "\u8fdb\u5ea6\u5230\u8fbe 100% \u5373\u53ef\u51b2\u8fc7\u7ec8\u70b9\u3002",
    lose: "\u5931\u8d25",
    loseText: "\u7ea2\u706f\u9636\u6bb5\u79fb\u52a8\u4f1a\u7acb\u5373\u7ed3\u675f\u672c\u5c40\u3002",
    player: "\u73a9\u5bb6",
    faceReady: ":)",
    faceWin: "^_^",
    faceLose: "x_x",
    gestureWin: "\u80dc\u5229",
    gestureLose: "\u88ab\u6293",
    english: "English",
    chinese: "\u4e2d\u6587",
  },
};

export default {
  data() {
    return {
      game: null,
      loading: false,
      error: "",
      poller: null,
      clock: Date.now(),
      clockTimer: null,
      language: "en",
    };
  },
  computed: {
    t() {
      return translations[this.language];
    },
    hasGame() {
      return Boolean(this.game);
    },
    canMove() {
      return this.hasGame && this.game.status === "running" && !this.loading;
    },
    lightText() {
      if (!this.hasGame) return this.t.waiting;
      return this.game.light === "green" ? this.t.greenLight : this.t.redLight;
    },
    lightClass() {
      if (!this.hasGame) return "idle";
      return this.game.light === "green" ? "green" : "red";
    },
    statusText() {
      if (!this.hasGame) return this.t.notStarted;
      const map = {
        running: this.t.running,
        won: this.t.won,
        lost: this.t.lost,
      };
      return map[this.game.status] || this.game.status;
    },
    moveCount() {
      return this.hasGame ? this.game.move_count : 0;
    },
    playerPosition() {
      return this.hasGame ? this.game.player_position : 0;
    },
    finishPosition() {
      return this.hasGame ? this.game.finish_position : 100;
    },
    progressPercent() {
      return Math.min(100, Math.round((this.playerPosition / this.finishPosition) * 100));
    },
    playerStyle() {
      return { left: `${this.progressPercent}%` };
    },
    playerStateClass() {
      if (!this.hasGame) return "ready";
      return this.game.status;
    },
    playerFace() {
      if (!this.hasGame || this.game.status === "running") return this.t.faceReady;
      return this.game.status === "won" ? this.t.faceWin : this.t.faceLose;
    },
    gestureText() {
      if (!this.hasGame || this.game.status === "running") return "";
      return this.game.status === "won" ? this.t.gestureWin : this.t.gestureLose;
    },
    buttonText() {
      if (this.loading) return this.t.loading;
      return this.hasGame ? this.t.restart : this.t.start;
    },
    message() {
      if (this.error) return this.error;
      if (!this.hasGame) return this.t.messageStart;
      if (this.game.status === "won") return this.t.messageWon;
      if (this.game.status === "lost") return this.t.messageLost;
      return this.game.light === "green" ? this.t.messageGreen : this.t.messageRed;
    },
    resultTitle() {
      if (!this.hasGame) return this.t.ready;
      if (this.game.status === "running") return this.t.inProgress;
      return this.game.status === "won" ? this.t.victory : this.t.gameOver;
    },
    resultDetail() {
      if (!this.hasGame) return this.t.readyDetail;
      if (this.game.status === "won") {
        return this.t.wonDetail.replace("{moves}", this.moveCount);
      }
      if (this.game.status === "lost") {
        return this.t.lostDetail.replace("{moves}", this.moveCount);
      }
      return `${this.progressPercent}% ${this.t.runningDetail}`;
    },
    phasePercent() {
      if (!this.hasGame || this.game.status !== "running") return 0;

      const startedAt = new Date(this.game.light_started_at).getTime();
      const durationSeconds = Number(this.game.light_duration_seconds);
      if (Number.isNaN(startedAt) || !Number.isFinite(durationSeconds) || durationSeconds <= 0) {
        return 0;
      }

      const elapsedSeconds = (this.clock - startedAt) / 1000;
      return Math.max(0, Math.min(100, (elapsedSeconds / durationSeconds) * 100));
    },
  },
  mounted() {
    window.addEventListener("keydown", this.handleKeydown);
    this.clockTimer = window.setInterval(() => {
      this.clock = Date.now();
    }, 100);
  },
  beforeUnmount() {
    window.removeEventListener("keydown", this.handleKeydown);
    window.clearInterval(this.clockTimer);
    this.stopPolling();
  },
  methods: {
    setLanguage(language) {
      this.language = language;
      this.error = "";
    },
    async startGame() {
      this.loading = true;
      this.error = "";
      try {
        const response = await fetch(`${API_BASE}/api/game/start`, {
          method: "POST",
        });
        this.game = await this.readResponse(response);
        this.startPolling();
      } catch (error) {
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
        const response = await fetch(`${API_BASE}/api/game/${this.game.game_id}/action`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ action: "move", distance: 10 }),
        });
        this.game = await this.readResponse(response);
        if (this.game.status !== "running") this.stopPolling();
      } catch (error) {
        this.error = this.t.moveError;
      } finally {
        this.loading = false;
      }
    },
    async refreshGame() {
      if (!this.hasGame || this.game.status !== "running") return;

      try {
        const response = await fetch(`${API_BASE}/api/game/${this.game.game_id}`);
        this.game = await this.readResponse(response);
      } catch (error) {
        this.error = this.t.syncError;
      }
    },
    async readResponse(response) {
      if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
      }
      return response.json();
    },
    handleKeydown(event) {
      if (event.code === "Space" || event.code === "ArrowRight") {
        event.preventDefault();
        this.movePlayer();
      }
      if (event.code === "Enter" && !this.loading) {
        event.preventDefault();
        this.startGame();
      }
    },
    startPolling() {
      this.stopPolling();
      this.poller = window.setInterval(() => this.refreshGame(), 350);
    },
    stopPolling() {
      if (this.poller) {
        window.clearInterval(this.poller);
        this.poller = null;
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
        <button class="primary" type="button" :disabled="loading" @click="startGame">
          {{ buttonText }}
        </button>
        <span class="shortcut">{{ t.shortcut }}</span>
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
          <small class="timer-note">{{ t.timerHidden }}</small>
        </div>

        <div class="stat-grid">
          <div>
            <span class="label">{{ t.status }}</span>
            <strong>{{ statusText }}</strong>
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

        <div class="result-box" :class="playerStateClass">
          <span class="label">{{ t.roundResult }}</span>
          <span class="result-face">{{ playerFace }}</span>
          <strong>{{ resultTitle }}</strong>
          <p>{{ resultDetail }}</p>
        </div>
      </aside>

      <section class="arena" :class="lightClass" aria-label="Game arena">
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

        <div class="track">
          <div class="track-fill" :style="{ width: progressPercent + '%' }"></div>
          <div class="player" :class="playerStateClass" :style="playerStyle">
            <span class="gesture" v-if="gestureText">{{ gestureText }}</span>
            <span class="arm left-arm"></span>
            <span class="arm right-arm"></span>
            <span class="player-head"></span>
            <span class="player-face">{{ playerFace }}</span>
            <span class="player-body"></span>
          </div>
        </div>

        <div class="start-line">{{ t.startLine }}</div>
      </section>
    </section>

    <section class="controls">
      <button
        class="move"
        type="button"
        :disabled="!canMove"
        @click="movePlayer"
        @touchstart.passive="movePlayer"
      >
        {{ t.moveButton }}
      </button>
      <p>{{ message }}</p>
    </section>

    <section class="rules">
      <div>
        <strong>{{ t.howToPlay }}</strong>
        <p>{{ t.howToPlayText }}</p>
      </div>
      <div>
        <strong>{{ t.win }}</strong>
        <p>{{ t.winText }}</p>
      </div>
      <div>
        <strong>{{ t.lose }}</strong>
        <p>{{ t.loseText }}</p>
      </div>
    </section>
  </main>
</template>
