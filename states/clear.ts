import { BaseState } from './base'
import { Agent } from '../main';
import { getLocal, Orientation } from '../utils/misc';
import { Vector3 } from '../utils/misc';
import { DodgeState } from './dodge';
import { Ball } from '../utils/preprocessing';
import { Color } from 'rlbot-test';

export class ClearState extends BaseState {
    substate: (() => void)|BaseState;
    ballInterception: Vector3;
    lastTouch: number; // the time when the last touch has been, useful for seeing if the ball has been hit
    constructor(agent) {
        super(agent)
        this.substate = this.reachGoal
    }
    run(agent: Agent) {
        this._run(agent)
        if(this.substate instanceof BaseState) {
            this.substate.run(agent)
            if(this.substate.finished == true) this.substate = this.reachGoal
        } else {
            this.substate()
        }
    }
    reachGoal() {
        let localGoalPos = getLocal(this.agent.game.myCar.position, this.agent.game.myCar.rotation, new Vector3(0, -4240*this.agent.game.teamMult, 0))
        if(localGoalPos.getMagnitude() > 750) {
            if(localGoalPos.y > 100) this.agent.controller.steer = 0.5
            else if(localGoalPos.y < -100) this.agent.controller.steer = -0.5
            else this.agent.controller.steer = 0
            this.agent.controller.throttle = 1
        } else {
            if(this.agent.game.myCar.velocity.getMagnitude() > 100) this.agent.controller.throttle = -1
            if(this.agent.game.ball.localPosition.y > 150) this.agent.controller.steer = 0.5
            else if(this.agent.game.ball.localPosition.y < -150) this.agent.controller.steer = -0.5
            else this.substate = this.goToBall
            this.agent.controller.handbrake = true
            this.agent.controller.throttle = 0;
        }
    }
    goToBall() {
        if(this.ballInterception == null || this.lastTouch < this.agent.game.ball.latestTouch.gameSeconds) this.calcBestInterSpot()
        this.agent.controller.throttle = 1
        let localPos = getLocal(this.agent.game.myCar.position, this.agent.game.myCar.rotation, this.ballInterception)
        let red = new Color(255, 255, 0, 0)
        this.agent.renderer.beginRendering()
        this.agent.renderer.drawLine3D(this.ballInterception.add(new Vector3(-100, 0, 0)).convertToRLBot(), this.ballInterception.add(new Vector3(100, 0, 0)).convertToRLBot(), red)
        this.agent.renderer.drawLine3D(this.ballInterception.add(new Vector3(0, -100, 0)).convertToRLBot(), this.ballInterception.add(new Vector3(0, 100, 0)).convertToRLBot(), red)
        this.agent.renderer.drawLine3D(this.ballInterception.add(new Vector3(0, 0, -100)).convertToRLBot(), this.ballInterception.add(new Vector3(0, 0, 100)).convertToRLBot(), red)
        this.agent.renderer.endRendering()
        if(localPos.y > localPos.x/25) this.agent.controller.steer = 0.5
        else if(localPos.y < -localPos.x/25) this.agent.controller.steer = -0.5
        else this.agent.controller.steer = 0
        this.agent.controller.boost = true
        if(this.agent.game.ball.localPosition.x < 1500) {
            this.substate = new DodgeState(this.agent)
            this.ballInterception = null
        }
    }
    calcBestInterSpot() {
        for(let slice of this.agent.game.ballPredictions) {
            let distance = slice.localPosition.getMagnitude()
            let seconds = distance/1000 // 1410 uu/s https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
            console.log(seconds)
            if(Math.round(seconds+this.agent.game.gameInfo.secondsElapsed) == Math.round(slice.gameSeconds)) {
                this.ballInterception = slice.position
                this.lastTouch = this.agent.game.ball.latestTouch.gameSeconds
                return;
            }
        }
        console.log('whoops nothing found')
    }
}