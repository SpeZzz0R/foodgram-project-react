FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
#COPY . .
#RUN pip3 install -r backend/foodgram/requirements.txt --no-cache-dir
COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]



#FROM python:3.7-slim
#WORKDIR /app
#COPY requirements.txt .
#RUN pip3 install -r requirements.txt --no-cache-dir
#COPY . .
#CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
