const { BaseAgent, SimpleController, quickChats, Manager } = require('rlbot-test');
const { Game } = require('./utils/preprocessing')
const KickoffState = require('./states/kickoff')

class BotVK extends BaseAgent {
    constructor(name, team, index, fieldInfo) {
        super(name, team, index, fieldInfo) //pushes these all to `this`.
        this.controller = new SimpleController()
        this.game = new Game(fieldInfo)
        this.state = new KickoffState(this)
        this.lastSecond = 0
    }
    getOutput(gameTickPacket, ballPrediction) {
        this.controller = new SimpleController()
        this.game.loadPacket(gameTickPacket)
        if(this.lastSecond == this.game.gameInfo.secondsElapsed) return this.controller
        this.lastSecond = this.game.gameInfo.secondsElapsed
        if(this.game.gameInfo.isKickoffPause && (this.state.timer > 10 || !(this.state instanceof KickoffState))) this.state = new KickoffState(this)
        this.state.run(this)
        return this.controller
    }
}

const manager = new Manager(BotVK)
manager.start()