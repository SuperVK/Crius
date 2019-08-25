import { BaseState } from './base'
import { BotVK } from '../main';
import { getLocal, Orientation } from '../utils/misc';
import { Vector3 } from '../utils/misc';

export class ClearState extends BaseState {
    substate: (() => void)|BaseState;
    constructor(agent) {
        super(agent)
        this.substate = this.reachGoal
    }
    run(agent: BotVK) {
        this._run(agent)
        if(this.substate instanceof BaseState) {
            this.substate.run(agent)
            if(this.substate.finished == true) this.substate = this.reachGoal
        } else {
            this.substate()
        }
    }
    reachGoal() {
        let localGoalPos = getLocal(this.agent.game.myCar.position, new Orientation(this.agent.game.myCar.rotation), new Vector3(0, -5000*this.agent.game.teamMult, 0))
        if(localGoalPos.y > 100) this.agent.controller.steer = 0.5
        else if(localGoalPos.y < 100) this.agent.controller.steer = -0.5
        else this.agent.controller.steer = 0
        
        this.agent.controller.throttle = 1
    }
    goToBall() {

    }
}