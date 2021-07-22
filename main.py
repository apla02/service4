from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse, StreamingResponse
import json
from models.query import Query
from models.conversor_csv import pd_to_csv


# create  new instance of FastAPI aplication
app = FastAPI()

# path of static files
app.mount('/static', StaticFiles(directory='static'), name='')
# path of templates
templates = Jinja2Templates(directory='templates')


@app.get('/')
def home(request: Request):
    """endpoint to display the start website"""
    return templates.TemplateResponse(
        'home.html', {'request': request})


@app.get("/report/topjoiners", status_code=200)
def top_joiners():
    """endpoint to make a report of a top o joiners by tasks"""
    try:
        new_object = Query("http://service3-django:8010/task/")
        df = new_object.top_joiners()
        stream = pd_to_csv(df)
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type="text/csv")
        response.headers[
            "Content-Disposition"] = "attachment; filename=top_joiner.csv"
        return response
    except Exception as err:
        return {'message': 'page request not found'}


@app.get("/report/taskbyjoiner")
def task_by_joiner():
    """endpoint to make a report tasks by joiner"""
    try:
        new_object = Query("http://service3-django:8010/task/")
        df = new_object.task_by_joiner()
        stream = pd_to_csv(df)
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type="text/csv")
        response.headers[
            "Content-Disposition"] = "attachment; filename=task_by_joiner.csv"
        return response
    except Exception as err:
        return {'message': 'page request not found'}


@app.get("/report/taskbyxjoiner/{joiner_id}")
def task_by_x_joiner(joiner_id: int):
    """endpoint to make a report tasks by joiner,
     receive the joiner id as a parameter"""
    try:
        new_object = Query("http://service3-django:8010/task/")
        df = new_object.task_by_X_joiner(joiner_id)
        stream = pd_to_csv(df)
        response = StreamingResponse(
            iter([stream.getvalue()]), media_type="text/csv")
        response.headers[
            "Content-Disposition"
            ] = "attachment; filename=task_by_X_joiner.csv"
        return response
    except Exception as err:
        return {'message': 'content not found'}


@app.get("/report/daysleftbyjoiner")
def days_left_by_joiner():
    """endpoint to make a report of days left of joiners with pending tasks"""
    try:
        new_object = Query("http://service3-django:8010/task/")
        df = new_object.days_left_by_joiner()
        print(df)
        stream = pd_to_csv(df)
        response = StreamingResponse(iter(
            [stream.getvalue()]), media_type="text/csv")
        response.headers[
            "Content-Disposition"
            ] = "attachment; filename=days_left_by_joiner.csv"
        return response
    except Exception:
        return {'message': 'content not found'}


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8030)
