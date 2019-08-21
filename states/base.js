class baseState {
    constructor(agent) {
        this.timer = 0
        this.startTime = agent.game.gameInfo ? agent.game.gameInfo.secondsElapsed : 0
        this.finished = false
        this.agent = agent
    }
    _run(agent) {
        this.agent = agent
        this.timer = agent.game.gameInfo.secondsElapsed-this.startTime
    }
}

module.exports = baseState