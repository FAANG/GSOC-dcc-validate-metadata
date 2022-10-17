# GSOC 2022 
## New FAANG Backend with Elasticsearch and GraphQL

### Backend

This repo only contains the code for the Backend GraphQL Django Server. You can read about the entire GSOC work done **[here](https://gist.github.com/sunnytarawade/342f7c99949bbe1077da48529117bb0e)**.
>Note
>The OS used for the development of the project was Ubuntu 22 LTS. Hence a linux based OS or Mac OS is recommended.
### Installation

1. Clone the repo (ssh):
```git clone git@github.com:FAANG/GSOC-dcc-validate-metadata.git```
2. Open a new terminal inside the repo and create a virtual env (You can make it in a different way as well, but here venv is used):
```python -m venv env```
3. Activate virtual env
```source env/bin/activate```

4. Install pip dependencies
```pip install -r requirements.txt```
If you get Module Not Found Error for some module, install that module manually using ```pip install <Missing Module Name>```

5. Start the redis server. There are two ways to do this.
    
    1. Starting server locally:
    Open a new terminal  window.
    Type ```sudo redis-server```. Install if not installed already.

    2. Using minikube:
    Ensure you have mini-kube up and running successfully. [Read here about how to install mini-kube](https://minikube.sigs.k8s.io/docs/start/)
    Open new terminal
    Start minikube by typing ```minikube start```
    Then type ```kubectl apply -f faang_gsoc/k8configs/redis-deployment+svc.yml```
    
6. Start the rabbitmq server. There are two ways to do this.

    1. Starting server locally: [Read here](https://www.rabbitmq.com/install-debian.html)

    2. Using minikube:
    Open new terminal
    Start minikube by typing ```minikube start```
    Then type ```kubectl apply -f faang_gsoc/k8configs/rabbitmq-deployment+svc.yml```

7. Start the python django server
```cd faang_gsoc```
```python manage.py makemigrations```
```python manage.py migrate```
```python manage.py runserver```
In a new browser tab, to see the [GraphiQL UI](https://github.com/graphql/graphiql) go to http://localhost:8000/subscriptions/

8. Start celery server
Open new terminal window and type:
```cd faang_gsoc```
```celery -A faang_gsoc -l info -Q graphql_api```

9. Start celery flower
Open new terminal window and type:
```cd faang_gsoc```
```celery -A faang_gsoc flower```
Open a new tab in the browser and go to http://localhost:5555

You can also read about the project setup and configurations here:
1.  [Project Setup](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-the-technical-d85bc9bb50bf)
2.  [Building for Scale](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-3ef99da2b1ed)

### Documentation

Please Read the following blogs to understand more about the code implementation in the following order:

1. [Introduction](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-c13b0f11d61)
2. [Basic Data Fetching](https://medium.com/@sunnytarawade000/8bbb71d2b6c8)
3. [Filtering Data](https://medium.com/@sunnytarawade000/299947f6cd01)
4. [Joins](https://medium.com/@sunnytarawade000/102d6ac164e0)
5. [Nested Joins](https://medium.com/@sunnytarawade000/71b6fdc435e2)
6. [Project Setup](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-the-technical-d85bc9bb50bf)
7. [Folder Structure of "graphql_api" app](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-the-technical-aa41c6eb5242)
8. [Fetching single document](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-the-technical-8c7be6ca8f4a)
9. [The function resolve_with_join](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-the-technical-3711673988e4)
10. [Building for Scale](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-3ef99da2b1ed)
11. [Working with Celery Tasks + GraphQL](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-db0550723fb9)
13. [Deployment](https://medium.com/@sunnytarawade000/sunnys-gsoc-adventure-63853c7e4b54)
