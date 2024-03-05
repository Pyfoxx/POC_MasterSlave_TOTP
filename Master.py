import flask
import requests
import itertools

slaves = ["127.0.0.1:5001"]
app = flask.Flask(__name__)


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def listener(port):
    app.run(port=port)


def makeEmIter(it, totp1, totp2, timeone, timetwo):
    it = list(split(it, len(slaves)))
    for v, i in enumerate(slaves):
        req = requests.post(f"http://{i}/iter", json={"it": it[v], "totp1": totp1, "totp2": totp2, "timeone":timeone, "timetwo":timetwo})
        if req.status_code != 200:
            print(f"ERROR ON {i}")
    print("slaves started")


@app.route('/receive', methods=['POST'])
def receiver():
    print(flask.request.data)
    return "200"


def makeIt():
    string = "abcdefghijklmnopqrstuvwxyz"
    it = list(itertools.product(string, repeat=5))
    return it


@app.route('/start')
def start():
    makeEmIter(makeIt(), totp1=000000, totp2=000000, timeone=0, timetwo=0)
    return "oui"

if __name__ == '__main__':
    listener(5000)

