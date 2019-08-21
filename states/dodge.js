const BaseState = require('./base')

class DodgeState extends BaseState {
    constructor(agent) {
        super(agent)
    }
    run(agent) {
        this._run(agent)
        this.agent.controller.boost = false
        if(this.timer <= 0.1) this.agent.controller.jump = true
        else if(this.timer <= 0.2) this.agent.controller.jump = false
        else if(this.timer <= 0.3) {
            this.agent.controller.jump = true    
            this.agent.controller.pitch = -1
        } else if(this.timer >= 1.5) this.finished = true
    }
}

module.exports = DodgeState