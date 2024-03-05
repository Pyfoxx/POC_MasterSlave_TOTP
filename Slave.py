import flask
import requests
import pyotp
from datetime import datetime
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
    timeone = data["timeone"]
    timetwo = data["timetwo"]
    totpone = data["totpone"]
    totptwo = data["totptwo"]
    for i in it:
        if pyotp.TOTP(''.join(i)).verify(totpone, for_time=datetime.fromtimestamp(timeone)):
            if pyotp.TOTP(''.join(i)).verify(totptwo, for_time=datetime.fromtimestamp(timetwo)):
                print(''.join(i))
                req = requests.post(f"http://{req.remote_addr}:5000/receive", data=''.join(i))
                print(req.status_code)
                return True
    return requests.post(f"http://{req.remote_addr}:5000/receive", data="404")

if __name__ == '__main__':
    listener(5001)