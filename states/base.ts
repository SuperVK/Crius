import { BaseAgent, GameTickPacket } from "rlbot-test";
import { Agent } from "../main";

export class BaseState {
    timer: number;
    startTime: number;
    finished: boolean;
    agent: Agent;
    constructor(agent: Agent) {
        this.timer = 0
        this.startTime = agent.game.gameInfo ? agent.game.gameInfo.secondsElapsed : 0
        this.finished = false
        this.agent = agent
    }
    run(agent: Agent) {}
    _run(agent) {
        this.agent = agent
        this.timer = agent.game.gameInfo.secondsElapsed-this.startTime
    }
}
