import { BaseAgent, SimpleController, Manager, GameTickPacket, BallPrediction, Color } from 'rlbot-test';
import { Game } from './utils/preprocessing';
import { KickoffState } from './states/Kickoff';
import { BaseState } from './states/base';
import { GoalShotState } from './states/GoalShot'
import { ClearState } from './states/clear';

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
        if(this.state.finished) {
            console.log('new statious')
            this.findNewState()
        }
        this.state.run(this)
        return this.controller
    }
    findNewState() {
        let game = this.game
        if(game.ballPredictions[60*3].position.y*game.teamMult < -2500) {
            this.state = new ClearState(this)
        } else {
            this.state = new GoalShotState(this)
        }
    }
}

const manager = new Manager(Agent)
manager.start()