import { FieldInfo, GameInfo, BaseAgent, GameTickPacket, BallPrediction, Slice } from "rlbot-test";

import { Vector3, Rotator, Orientation, getLocal } from './misc'
import { dot } from "mathjs";

export class Game {
    fieldInfo: FieldInfo;
    ball: Ball;
    myCar: Car;
    teamMult: number;
    numCars: number;
    cars: Car[];
    gameInfo: GameInfo;
    ballPredictions: Ball[];
    constructor(fieldInfo: FieldInfo) {
        this.fieldInfo = fieldInfo
    }
    loadPacket(gameTickPacket: GameTickPacket, ballPrediction: BallPrediction, index: number) {
        if(gameTickPacket.players.length == 0) return console.log('no players found')
        this.myCar = new Car(gameTickPacket.players[index])
        this.ball = new Ball(gameTickPacket.ball, this.myCar)
        this.teamMult = ((this.myCar.team+this.myCar.team)-1)*-1
        this.numCars = gameTickPacket.players.length
        this.cars = []
        for(let i = 0; i < this.numCars; i++) {
            this.cars.push(new Car(gameTickPacket.players[i]))
        }
        this.gameInfo = gameTickPacket.gameInfo
        this.ballPredictions = []
        for(let i = 0; i < 360; i++) {
            this.ballPredictions.push(new Ball(ballPrediction.slices[i], this.myCar))
        }
    }
}

class Car {
    position: Vector3;
    rotation: Rotator;
    velocity: Vector3;
    angularVelocity: Vector3;
    team: number;
    boost: number;
    constructor(car: import("rlbot-test").Player) {
        if(car == undefined) return
        this.position = new Vector3(car.physics.location)
        this.rotation = new Rotator(car.physics.rotation)
        this.velocity = new Vector3(car.physics.velocity)
        this.angularVelocity = new Vector3(car.physics.angularVelocity)
        this.team = car.team
        this.boost = car.boost
    }
}

export class Ball {
    position: Vector3;
    rotation?: Rotator;
    velocity: Vector3;
    angularVelocity: Vector3;
    latestTouch?: any;
    localPosition?: Vector3;
    localVelocity?: Vector3;
    gameSeconds?: number;
    constructor(ball: import("rlbot-test").Ball|Slice|any, myCar?: Car) {
        this.position = new Vector3(ball.physics.location)
        if(ball.physics.rotation != null) this.rotation = new Rotator(ball.physics.rotation)
        this.velocity = new Vector3(ball.physics.velocity)
        this.angularVelocity = new Vector3(ball.physics.angularVelocity)
        if(myCar != undefined && myCar.rotation != undefined) {
            this.localPosition = getLocal(myCar.position, myCar.rotation, this.position)
            this.localVelocity = getLocal(myCar.position, myCar.rotation, this.position)
        }
        if(ball.latestTouch != null) this.latestTouch = ball.latestTouch
        if(ball.gameSeconds != null) this.gameSeconds = ball.gameSeconds
    }
}


