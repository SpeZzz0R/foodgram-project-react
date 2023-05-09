FROM python:3.7-slim
WORKDIR /app
COPY ./backend/foodgram/requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
