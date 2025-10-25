from typing import Any, Optional

from flask import Flask, make_response, request
from pydantic import BaseModel

from task import make_file, task_app

app = Flask(__name__)

class TaskStatus(BaseModel):
    id: str
    status: Optional[str] = None
    result: Optional[Any] = None

@app.route('/')
def hello():
    return "Hello World"

@app.route('/task')
def request_task():
    print("request task")
    task = make_file.delay()
    return TaskStatus(id=task.id).model_dump()

@app.route('/task/<string:task_id>')
def check_status(task_id:str) -> Any:
    print("request task : ", task_id)
    try:
        req = request.args
        operation = req.get("operation")
        if operation == "download":
            result = task_app.AsyncResult(task_id)
            blob = result.result
            filename = "test.zip"
            return (
                blob,
                200,
                {
                    "Content-Type": "octet-stream",
                    "Content-Disposition": f"attachment; filename={filename}",
                },
            )
        else:
            result = task_app.AsyncResult(task_id)
            status = TaskStatus(id=task_id, status=result.status)
            return status.model_dump()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True, port=8888, threaded=True)  
