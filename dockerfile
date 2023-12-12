FROM python:3.11.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN pip install celery redis

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

