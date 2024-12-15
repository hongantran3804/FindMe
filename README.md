# FindMe

## Part 1 and 3

a Python script using OpenCV and a pre-trained machine learning model to
perform object detection on images of shelves.

### Installation

```
pip install -r requirements.txt
```

### Using objectDetection.py

```
python objectDetection.py
```

## Part 2

Create a Flask-based RESTful API to manage a collection of product information,
supporting operations for adding, retrieving, updating, and deleting records.

### Installation

```
pip install -r requirements.txt
```

### Setup Mysql

<a href="https://www.youtube.com/watch?v=Sfvpgu9ID2Q">Link to download mysql</a>
To connect with your database, make url to connect with database: mysql+pymysql://<username>:<password>@<hostname>:<port>/<database_name>

### Run main.py

```
uvicorn main:app -- reload
```

---
**NOTE**

After running main.py, go to the url <http://127.0.0.1:8000/docs> to test the function

---
