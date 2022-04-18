FROM python:3.8.5-alpine3.12
WORKDIR /app
COPY ./src /app
RUN pip install pip --upgrade && pip install -r requirements.txt
CMD ["python3", "-u", "main.py"]

