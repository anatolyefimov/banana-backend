FROM python:3

WORKDIR /app
ADD . /app

RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn

EXPOSE 5000

CMD [ "gunicorn", "-w", "4", "--bind", "0.0.0.0:5000", "wsgi:app"]
