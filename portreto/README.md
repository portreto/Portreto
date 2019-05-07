# Personal Notes

## Web-app Django Container
- uses venv for all the python dependencies for easier development
- init.sh to activate venv and run Django from it
- host url: http://localhost:8000

## Zookeeper ensemble
- 3 zookeeper containers
    - zoo1
    - zoo2
    - zoo3

## MongoDB Set
- 3 MongoDB containers
    - mongo-rs0-1
    - mongo-rs0-2
    - mongo-rs0-3
- Setup container (setup-rs) runs on deployment to connect mongoDB replicas
- Mongo Admin container (adminmongo)
    - host url: http://localhost:1234
    - connection syntax: `mongodb://<user>:<password>@127.0.0.1:<port>/<db>`
    - example connection: `mongodb://mongo-rs0-1`

Mongo Create User: <br>
`db.createUser({user: "portreto",pwd: "portreto",roles: [ { role: "readWrite", db: "appdata" } ]})`

Mongo connect to replica set <br>
`mongo --host rs0/mongo-rs0-1:27017,mongo-rs0-2:27017,mongo-rs0-3:27017`



build Django container: `docker-compose build`

run containers: 
`docker-compose up -d`

## Groups

For developent purposes groups have been created using noop images
### Existing Groups:

| Name 	| Description                              	|
|------	|------------------------------------------	|
| db   	| Fire up all MongoDB related containers   	|
| zoo  	| Fire up all zookeeper related containers 	|

groups are called through `docker-compose run <name>` just like any other container