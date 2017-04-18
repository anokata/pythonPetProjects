from flask import Flask

app = Flask(__name__)

@app.route('/')
def view_hello():
    return "hi"

if __name__=='__main__':
    app.debug = True
    app.run() # run dev webserver
