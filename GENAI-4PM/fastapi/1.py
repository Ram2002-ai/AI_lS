from fastapi import FastAPI

app=FastAPI()

@app.get('/')

def hello_world():
    return {'message':'hello world'}

@app.get("/Home")
def Home():
    return {'message':'what is this'}


@app.post('name')
def name():

    return input('enter your name')

