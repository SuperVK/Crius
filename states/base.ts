import { BaseAgent, GameTickPacket } from "rlbot-test";
import { BotVK } from "../main";

export class BaseState {
    timer: number;
    startTime: number;
    finished: boolean;
    agent: BotVK;
    constructor(agent) {
        this.timer = 0
        this.startTime = agent.game.gameInfo ? agent.game.gameInfo.secondsElapsed : 0
        this.finished = false
        this.agent = agent
    }
    run(agent: BotVK) {}
    _run(agent) {
        this.agent = agent
        this.timer = agent.game.gameInfo.secondsElapsed-this.startTime
    }
}
