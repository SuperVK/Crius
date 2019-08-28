import { Vector3 as renderVector3 } from 'rlbot-test'
import { dot } from 'mathjs';


export class Vector3 {
    x: number;
    y: number;
    z: number;
    constructor(xArr, y?: number, z?: number) {
        if(typeof xArr == 'object') {
            if(xArr.length != undefined) {
                this.x = xArr[0]
                this.y = xArr[1]
                this.z = xArr[2]
            } else {
                this.x = xArr.x
                this.y = xArr.y
                this.z = xArr.z
            }
        } else {
            this.x = xArr
            this.y = y
            this.z = z
        }
    }
    convertToArray(): number[] {
        return [this.x, this.y, this.z]
    }
    convertToRLBot(): renderVector3 {
        return new renderVector3(this.x, this.y, this.z)
    }
    subtract(target: Vector3): Vector3 {
        return new Vector3(this.x-target.x, this.y-target.y, this.z-target.z)
    }
    add(target: Vector3): Vector3 {
        return new Vector3(this.x+target.x, this.y+target.y, this.z+target.z)
    }
    getMagnitude(): number {
        return Math.sqrt(this.x**2+this.y**2+this.z**2)
    }
    getUnitVector(): Vector3 {
        let magnitude = this.getMagnitude()
        return new Vector3(this.x/magnitude, this.y/magnitude, this.z/magnitude)
    }
}

export class Rotator {
    pitch: number;
    yaw: number;
    roll: number;
    constructor(pitchArr, yaw?, roll?) {
        if(typeof pitchArr == 'object') {
            if(pitchArr.length != undefined) {
                this.pitch = pitchArr[0]
                this.yaw = pitchArr[1]
                this.roll = pitchArr[2]
            } else {
                this.pitch = pitchArr.pitch
                this.yaw = pitchArr.yaw
                this.roll = pitchArr.roll
            }
        } else {
            this.pitch = pitchArr
            this.yaw = yaw
            this.roll = roll
        }
    }
}

// stolen from: https://github.com/ddthj/v0tzwei/blob/master/util/orientation.py
export class Orientation {
    yaw: number;
    roll: number;
    pitch: number;
    forward: Vector3;
    right: Vector3;
    up: Vector3;
    constructor(rotation: Rotator) {
        this.yaw = rotation.yaw;
        this.roll = rotation.roll;
        this.pitch = rotation.pitch;

        let cr = Math.cos(this.roll)
        let sr = Math.sin(this.roll)
        let cp = Math.cos(this.pitch)
        let sp = Math.sin(this.pitch)
        let cy = Math.cos(this.yaw)
        let sy = Math.sin(this.yaw)

        this.forward = new Vector3(cp*cy, cp*sy, sp)
        this.right = new Vector3(cy*sp*sr-cr*sy, sy*sp*sr+cr*cy, -cp*sr)
        this.up = new Vector3(-cr*cy*sp-sr*sy, -cr*sy*sp+sr*cy, cp*cr)
    }
}

export function getLocal(center: Vector3, rotation: Rotator, target: Vector3): Vector3 {
    let orientation = new Orientation(rotation)
    let x = dot(target.subtract(center).convertToArray(), orientation.forward.convertToArray())
    let y = dot(target.subtract(center).convertToArray(), orientation.right.convertToArray())
    let z = dot(target.subtract(center).convertToArray(), orientation.up.convertToArray())
    return new Vector3(x, y, z)
}