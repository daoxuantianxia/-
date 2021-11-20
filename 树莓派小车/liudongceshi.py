from flask import Flask, render_template, Response,request
import cv2
import serial
def right():
    #serial.write('r'.encode())
    #response=serial.readline().decode()
    print('right')
def left():
    #serial.write('l'.encode())
    #response=serial.readline().decode()
    print('left')
def straight():
    #serial.write('f'.encode())
    #response=serial.readline().decode()
    print('forward')
def stop():
    #serial.write('s'.encode())
    #response=serial.readline().decode()
    print('stop')
def back():
    #serial.write('b'.encode())
    #response=serial.readline().decode()
    print('back')
class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        success, image = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
    #return 'hello'

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/control/',methods=['POST'])
def control():
    option =request.form.get('data')
    print(option)
    if option == 'forward':
        straight()
    elif option == 'back':
        back()
    elif option == 'left':
        left()
    elif option == 'right':
        right()
    else:
        stop()
    response = '成功'
    return response

if __name__ == '__main__':
    app.run()