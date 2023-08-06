# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2019/11/12 21:27
# @author  : Mo
# @function: get service of fastapi


from fastapi import FastAPI
app = FastAPI()


@app.get('/test/a={a}/b={b}')
def calculate(a: int=None, b: int=None):
    c = a + b
    res = {"res":c}
    return res


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app,
                host="0.0.0.0",
                port=8080,
                workers=1)
