import flask
import requests
import pyotp
import datetime
app = flask.Flask(__name__)


def listener(port):
    app.run(port=port)


@app.route('/iter', methods=['POST'])
def iter():
    process(flask.request)
    return "200"


def process(req):
    data = req.json
    print(req.remote_addr)
    it = data["it"]
    topt1 = data["topt1"]
    timeone = data["timeone"]
    topt2 = data["topt2"]
    timetwo = data["timetwo"]
    for i in it:
        if pyotp.TOTP(''.join(i)).verify(topt1, for_time=datetime.datetime.fromtimestamp(timeone)):
            if pyotp.TOTP(''.join(i)).verify(topt2, for_time=datetime.datetime.fromtimestamp(timetwo)):
                print(''.join(i))
                req = requests.post(f"http://{req.remote_addr}:5000/receive", data=''.join(i))
                print(req.status_code)
                return True
    return requests.post(f"http://{req.remote_addr}:5000/receive", data="404")

if __name__ == '__main__':
    listener(5001)