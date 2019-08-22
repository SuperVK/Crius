const { Vector3, Rotator } = require('./types')

class Game {
    constructor(fieldInfo) {
        this.fieldInfo = fieldInfo
    }
    loadPacket(gameTickPacket) {
        this.ball = new Ball(gameTickPacket.ball)
        this.numCars = gameTickPacket.players.length
        this.cars = []
        for(let i = 0; i < this.numCars; i++) {
            this.cars.push(new Car(gameTickPacket.gameCars[i]))
        }
        this.gameInfo = gameTickPacket.gameInfo
    }
}



class Car {
    constructor(car) {
        this.position = new Vector3(car.physics.location)
        this.rotation = new Rotator(car.phsyics.rotation)
        this.velocity = new Vector3(car.physics.velocity)
        this.angularVelocity = new Vector3(car.physics.angularVelocity)
        this.team = car.team
        this.boost = car.boost
    }
}

class Ball {
    constructor(ball) {
        this.position = new Vector3(ball.physics.location)
        this.rotation = new Rotator(ball.physics.rotation)
        this.velocity = new Vector3(ball.physics.velocity)
        this.angularVelocity = new Vector3(ball.physics.angularVelocity)
        this.latestTouch = ball.latestTouch
    }
}

module.exports = {
    Game: Game,
    Ball: Ball
}
