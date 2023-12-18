FROM python:3.8-alpine
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
COPY .key /app/.key
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD ["worker.py" ]
