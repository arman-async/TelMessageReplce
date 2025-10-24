FROM python:3.10-slim
WORKDIR /project

COPY app ./app
COPY requirements.txt .

RUN pip install -r requirements.txt
CMD [ "python3", "-m", "app" ]