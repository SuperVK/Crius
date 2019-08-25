import { BaseState } from  './base';
import { BotVK } from '../main';
import { ClearState } from './clear'
import { getLocal, Orientation, Vector3 } from '../utils/misc';

export class GoalShotState extends BaseState {
    substate: (() => void)|BaseState;
    constructor(agent) {
        super(agent)
        this.substate = this.findNewState
    }
    run(agent: BotVK) {
        this._run(agent)
        if(this.substate instanceof BaseState) {
            this.substate.run(agent)
            if(this.substate.finished == true) this.substate = this.findNewState
        } else {
            this.substate()
        }
    }
    findNewState() {
        let game = this.agent.game
        if(game.ballPredictions[60*1].position.y*game.teamMult < -2500) {
            console.log(game.ballPredictions[60*3].position.y*game.teamMult)
            this.substate = new ClearState(this)
        }       
    }
}