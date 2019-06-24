#!/bin/bash
echo ************************************************
echo Starting the replica set
echo ************************************************

# Initialize replicaset
sleep 2 | echo Sleeping
mongo mongodb://mongo-rs0-1:27017 replicaSet.js

# Initialize database
sleep 20 | echo Sleeping
mongo mongodb://mongo-rs0-1:27017/appdata dbInit.js
mongo mongodb://mongo-rs0-2:27017/appdata dbInit.js
mongo mongodb://mongo-rs0-3:27017/appdata dbInit.js
sleep 2 | echo Sleeping
mongo mongodb://mongo-rs0-1:27017/auth dbInit.js
mongo mongodb://mongo-rs0-2:27017/auth dbInit.js
mongo mongodb://mongo-rs0-3:27017/auth dbInit.js