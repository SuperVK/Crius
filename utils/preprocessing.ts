import { FieldInfo, GameInfo } from "rlbot-test";

import { Vector3, Rotator } from './types'

export class Game {
    fieldInfo: FieldInfo;
    ball: Ball;
    numCars: number;
    cars: Car[];
    gameInfo: GameInfo;
    constructor(fieldInfo) {
        this.fieldInfo = fieldInfo
    }
    loadPacket(gameTickPacket) {
        this.ball = new Ball(gameTickPacket.ball)
        this.numCars = gameTickPacket
        this.cars = []
        for(let i = 0; i < this.numCars; i++) {
            this.cars.push(new Car(gameTickPacket.gameCars[i]))
        }
        this.gameInfo = gameTickPacket.gameInfo
    }
}

class Car {
    position: Vector3;
    rotation: Rotator;
    velocity: Vector3;
    angularVelocity: Vector3;
    team: number;
    boost: number;
    constructor(car) {
        this.position = new Vector3(car.physics.location)
        this.rotation = new Rotator(car.phsyics.rotation)
        this.velocity = new Vector3(car.physics.velocity)
        this.angularVelocity = new Vector3(car.physics.angularVelocity)
        this.team = car.team
        this.boost = car.boost
    }
}

export class Ball {
    position: Vector3;
    rotation: Rotator;
    velocity: Vector3;
    angularVelocity: Vector3;
    latestTouch: any;
    constructor(ball) {
        this.position = new Vector3(ball.physics.location)
        this.rotation = new Rotator(ball.physics.rotation)
        this.velocity = new Vector3(ball.physics.velocity)
        this.angularVelocity = new Vector3(ball.physics.angularVelocity)
        this.latestTouch = ball.latestTouch
    }
}
