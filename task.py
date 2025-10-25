import datetime
import io
import os
import time
import zipfile

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("CELERY_TASK_RESULT_EXPIRES"))

mongo_uri = "mongodb://127.0.0.1:27017/celery-test"
redis_uri = "redis://localhost:6379"

task_app = Celery("tasks", broker=redis_uri, backend=mongo_uri)

task_app.conf.update(result_expires=10)


@task_app.task
def make_file():
    time.sleep(30)
    filenames = ["file1.txt", "file2.txt", "file3.txt"]
    date_time = datetime.datetime.now().strftime("%Y%m%d%H%m%S")
    file_name_zip = "{}_{}.zip".format("zip-files", date_time)
    try:
        buff = io.BytesIO()
        with zipfile.ZipFile(
            buff,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as new_zip:
            for filename in filenames:
                print(filename)
                # file, mime_type = dls.get_file(filename)
                path = f"{filename}"
                file = f"{filename} : hello world"
                new_zip.writestr(path, file)
        # 書き込み位置を先頭に戻す必要がある
        buff.seek(0)
        return buff.read()
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    task_app.start()
