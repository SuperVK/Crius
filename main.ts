import { BaseAgent, SimpleController, Manager, GameTickPacket, BallPrediction, Color } from 'rlbot-test';
import { Game } from './utils/preprocessing';
import { KickoffState } from './states/Kickoff';
import { BaseState } from './states/base';
import { GoalShotState } from './states/GoalShot'

export class Agent extends BaseAgent {
    controller: SimpleController;
    game: Game;
    state: BaseState;
    lastSecond: number;
    constructor(name, team, index, fieldInfo) {
        super(name, team, index, fieldInfo) //pushes these all to `this`.
        this.controller = new SimpleController()
        this.game = new Game(fieldInfo)
        this.state = new KickoffState(this)
        this.lastSecond = 0
    }
    getOutput(gameTickPacket: GameTickPacket, ballPrediction: BallPrediction) {
        this.controller = new SimpleController()
        this.game.loadPacket(gameTickPacket, ballPrediction, this.index)
        if(this.lastSecond == this.game.gameInfo.secondsElapsed) return this.controller
        this.lastSecond = this.game.gameInfo.secondsElapsed
        if(this.game.gameInfo.isKickoffPause && (this.state.timer > 10 || !(this.state instanceof KickoffState))) this.state = new KickoffState(this)
        if(this.state.finished) this.state = new GoalShotState(this)
        this.state.run(this)
        return this.controller
    }
}

const manager = new Manager(Agent)
manager.start()