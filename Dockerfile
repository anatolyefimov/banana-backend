FROM python:3

WORKDIR /app

ADD . /app

#COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#COPY .. .

EXPOSE 5000
CMD ["python", "run.py"]