```bash
pip install -r requirements.txt 
flask run
```

```
sudo docker-compose up --build
```
если не в докере, то 
```
python run.py
```
, но скорее всего надо будет подложить переменные окружения с $MONGO_URI and $DB
