FROM python:3.12.3-bullseye
COPY ./requirements.txt /usr/app/MesSender/requirements.txt
WORKDIR /usr/app/MesSender
RUN pip install -r requirements.txt
COPY ./src /usr/app/MesSender
EXPOSE 8000
CMD uvicorn server:app --host 0.0.0.0
