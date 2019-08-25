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
        this.agent.controller.throttle = 1
        let localPos = this.agent.game.ball.localPosition
        if(localPos.y > localPos.x/25) this.agent.controller.steer = 0.5
        else if(localPos.y < -localPos.x/25) this.agent.controller.steer = -0.5
        else this.agent.controller.steer = 0
        this.agent.controller.boost = true
        if(this.agent.game.ball.localPosition.x < 1500) {
            this.substate = new DodgeState(this.agent)
        }
    }

}
