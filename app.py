from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return '<h1>Hello Ofek!</h1><p>Running on Amazon ECS</p>'

if __name__ == '__main__':
    # אנחנו מגדירים host='0.0.0.0' כדי שהאפליקציה תהיה נגישה מחוץ לקונטיינר
    app.run(debug=True, host='0.0.0.0', port=5000)
