import { BaseState } from  './base';
import { DodgeState } from './dodge';
import { BotVK } from '../main';

export class KickoffState extends BaseState {
    substate: (() => void)|BaseState;
    constructor(agent) {
        super(agent)
        this.substate = this.findNewState
    }
    run(agent: BotVK) {
        if(this.agent.game.gameInfo.isKickoffPause == false) this.finished = true
        this._run(agent)
        if(this.substate instanceof BaseState) {
            this.substate.run(agent)
            if(this.substate.finished == true) this.substate = this.findNewState
        } else {
            this.substate()
        }
    }
    findNewState() {
        console.log(this.timer)
        this.agent.controller.throttle = 1
        this.agent.controller.boost = true
        if(Math.floor(this.timer*10)/10 == 0.5) {
            this.substate = new DodgeState(this.agent)
        }
    }

}
