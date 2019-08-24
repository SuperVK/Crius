interface InterfaceVector3 {
    x: number;
    y: number;
    z: number;
}

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
