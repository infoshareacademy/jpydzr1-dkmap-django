FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN ls -la
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY TicTacToe /code/

