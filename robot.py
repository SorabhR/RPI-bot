from flask import Flask, render_template
import serial
import RPi.GPIO as GPIO

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)


pin={
    1:{"name":"up","state":"off"},
    2:{"name":"down","state":"off"},
    3:{"name":"right","state":"off"},
    4:{"name":"left","state":"off"},
    5:{"name":"stop","state":"off"}
}

def ard(s):
    if(s==1):
        forward()
    elif(s==2):
        backward()
    elif(s==3):
        right()
    elif(s==4):
        left()
    else:
        stops()


def forward():
      GPIO.outpt(6,GPIO.HIGH)
      GPIO.outpt(13,GPIO.LOW)
      GPIO.outpt(19,GPIO.HIGH)
      GPIO.outpt(26,GPIO.LOW)

def left():
      stops()

def right():
      stops()

def backward():
      stops()

def stops():
      GPIO.outpt(6,GPIO.LOW)
      GPIO.outpt(13,GPIO.LOW)
      GPIO.outpt(19,GPIO.LOW)
      GPIO.outpt(26,GPIO.LOW)

@app.route("/")
def main():
    temp={
        'pin':pin
    }
    return render_template("main.html",**temp)


@app.route("/<pino>/<state>")
def led(pino,state):
    pino=int(pino)
    pin[pino]["state"]=state

    for i in pin:
        if (i==pino):
            continue
        else:
            pin[i]["state"]="off"

    j=0
    for i in pin:
        if (pin[i]["state"]=="off"):
            j+=1

    if(j==5):
        pin[5]["state"]="on"

    for i in pin:
        if(pin[i]["state"]=="on"):
            ard(i)

    temp={
        'pin': pin
    }
    return render_template("main.html",**temp)



if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)
