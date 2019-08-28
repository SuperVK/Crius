import { BaseState } from  './base';
import { Agent } from '../main';
import { ClearState } from './clear'
import { getLocal, Orientation, Vector3 } from '../utils/misc';
import { Color } from 'rlbot-test';
import { DodgeState } from './dodge';

export class GoalShotState extends BaseState {
    substate: (() => void)|BaseState;
    ballInterception: Vector3;
    ballTime: number;
    lastTouch: number; // the time when the last touch has been, useful for seeing if the ball has been hit
    constructor(agent) {
        super(agent)
        this.substate = this.findNewState
    }
    run(agent: Agent) {
        this._run(agent)
        if(this.substate instanceof BaseState) {
            this.substate.run(agent)
            if(this.substate.finished == true) this.finished = true
        } else {
            this.substate()
        }
    }
    findNewState() {
        let game = this.agent.game
        if(game.ball.position.y*game.teamMult < game.myCar.position.y*game.teamMult) {
            let vectorGoalToBall = new Vector3(game.ball.position.x, game.ball.position.y-5120*game.teamMult, 0)
            this.moveTo(new Vector3(game.ball.position.x+vectorGoalToBall.x/2, game.ball.position.y+vectorGoalToBall.y/2, 0))
        } else {
            if(this.ballInterception == null || this.lastTouch < this.agent.game.ball.latestTouch.gameSeconds) this.calcBestInterSpot()
            if(this.ballInterception != null) this.moveTo(this.ballInterception, true)
        }
    }
    moveTo(location: Vector3, ball?: boolean) {
        let localPosition = getLocal(this.agent.game.myCar.position, this.agent.game.myCar.rotation, location)
        if(localPosition.y > localPosition.x/25) this.agent.controller.steer = 0.5
        else if(localPosition.y < -localPosition.x/25) this.agent.controller.steer = -0.5

        // Roses are red, girls in your area are hot, I can't code, so I stole this from the example bot
        let botToTargetAngle = Math.atan2(location.y - this.agent.game.myCar.position.y, location.x - this.agent.game.myCar.position.x);
        let botFrontToTargetAngle = botToTargetAngle - this.agent.game.myCar.rotation.yaw;
        if (botFrontToTargetAngle < -Math.PI) botFrontToTargetAngle += 2 * Math.PI;
        if (botFrontToTargetAngle > Math.PI) botFrontToTargetAngle -= 2 * Math.PI;

        if(Math.abs(botFrontToTargetAngle) > Math.PI/3) this.agent.controller.handbrake = true
        this.agent.controller.boost = true;
        this.agent.controller.throttle = 1
        if(ball) {
            let ETA = this.ballInterception.getMagnitude()/this.agent.game.myCar.velocity.getMagnitude() // uu/(uu/s)=s
            if(this.agent.game.gameInfo.secondsElapsed+ETA < this.ballTime-1) {
                if(this.agent.game.myCar.boost != 0) this.agent.controller.boost = false
                else this.agent.controller.throttle = 0
            }
            if(localPosition.x < 750 && ball) {
                console.log('guess not?')
                this.substate = new DodgeState(this.agent)
            }
        }
        let blue = new Color(255, 0, 0, 255)
        this.agent.renderer.beginRendering()
        this.agent.renderer.drawLine3D(location.add(new Vector3(-100, 0, 0)).convertToRLBot(), location.add(new Vector3(100, 0, 0)).convertToRLBot(), blue)
        this.agent.renderer.drawLine3D(location.add(new Vector3(0, -100, 0)).convertToRLBot(), location.add(new Vector3(0, 100, 0)).convertToRLBot(), blue)
        this.agent.renderer.drawLine3D(location.add(new Vector3(0, 0, -100)).convertToRLBot(), location.add(new Vector3(0, 0, 100)).convertToRLBot(), blue)
        this.agent.renderer.endRendering()

    }
    calcBestInterSpot() {
        for(let slice of this.agent.game.ballPredictions) {
            let distance = slice.localPosition.getMagnitude()
            let seconds = distance/1200 // 1410 uu/s https://github.com/RLBot/RLBot/wiki/Useful-Game-Values
            if(Math.round(seconds+this.agent.game.gameInfo.secondsElapsed) == Math.round(slice.gameSeconds)) {
                this.ballInterception = slice.position
                this.ballTime = slice.gameSeconds
                this.lastTouch = this.agent.game.ball.latestTouch == undefined ? 0 : this.agent.game.ball.latestTouch.gameSeconds
                return;
            }
        }
        console.log('whoops nothing found')
    }
}