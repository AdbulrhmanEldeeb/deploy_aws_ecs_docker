FROM python:3.12.4-slim as base

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt

EXPOSE 8080
# make host='0.0.0.0', port=8080 in your projects 
CMD python ./app.py