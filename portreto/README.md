# Important Notes

## Run
1) Build Django container: <br>
     `docker-compose build`
2) Run containers: <br>
     `docker-compose up -d`

## Helpfull docker commands
- List all running containers: <br>
    `docker ps`
- See logs of a container: <br>
    `docker logs <container>`
- Kill all running containers: <br>
    `docker kill $(docker ps -q)`
- Delete all stoped containers: <br>
    `docker rm $(docker ps -a -q)`
- Delete all images: <br>
    `docker rmi $(docker images -q) --force`
- Run bash (or any other command) in container using docker-compose: <br>
    `docker-compose run <docker_name> bash`

## Web-app Django Container

- host url: http://localhost:8000
- for every new python package installed: <br>
    `pip freeze > requirements.txt` <br>
    inside django's directory

## Zookeeper ensemble
- 3 zookeeper containers
    - zoo1
    - zoo2
    - zoo3

## MongoDB  Replica Set

- 3 MongoDB containers
    - mongo-rs0-1
    - mongo-rs0-2
    - mongo-rs0-3
- Setup container (setup-rs) runs on deployment to connect mongoDB replicas
- Mongo Admin container (adminmongo)
    - host url: http://localhost:1234
    - example connection: `mongodb://mongo-rs0-1`

### Connect to database using <b> adminmongo </b> container
1) Go to admin page: http://localhost:1234
2) Add connection `mongo1` at `mongodb://mongo-rs0-1`
3) Add connection `mongo2` at `mongodb://mongo-rs0-2`
4) Add connection `mongo3` at `mongodb://mongo-rs0-3`
5) Connect to each one of the above connections to find the primary replica 


### Connect to database CLI:
1) Run bush in setup-rs container: <br>
     `docker-compose run setup-rs bash`
2) Mongo connect to replica set: <br>
     `mongo --host rs0/mongo-rs0-1:27017,mongo-rs0-2:27017,mongo-rs0-3:27017`
3) Mongo use appdata db: <br>
     `use appdata`

Helpfull commands:

- Create User: <br>
    `db.createUser({user: "portreto",pwd: "portreto",roles: [ { role: "readWrite", db: "appdata" } ]})`
- General connect syntax: <br>
    `mongodb://<user>:<password>@127.0.0.1:<port>/<db>`

## Django

Current containers:
- web

## Helpfull commands:

### Django Make Migrations
1) Run containers (if needed): `docker-compose up`
2) Connect to container shell: `docker-compose run web bash`
3) Make Migrations: `python manage.py makemigrations`
4) Migrate: `python manage.py migrate`

### Django add python library
1) In django project folder run: `pip freeze > requirements.txt`
2) Build new django image: `docker-compose build web`
3) Run django container: `docker-compose up web`



## Groups

For developent purposes groups have been created using noop images
### Existing Groups:

| Name 	| Description                              	|
|------	|------------------------------------------	|
| db   	| Fire up all MongoDB related containers   	|
| zoo  	| Fire up all zookeeper related containers 	|

groups are called through `docker-compose run <name>` just like any other container


