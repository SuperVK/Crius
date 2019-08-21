const BaseState = require('./base')
const DodgeState = require('./dodge')

class KickoffState extends BaseState {
    constructor(agent) {
        super(agent)
        this.substate = this.findNewState
    }
    run(agent, gameTickPacket) {
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
        this.agent.controller.throttle = true
        this.agent.controller.boost = true
        if(Math.floor(this.timer*10)/10 == 0.5) {
            this.substate = new DodgeState(this.agent)
        }
    }

}

module.exports = KickoffState