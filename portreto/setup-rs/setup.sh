#!/bin/bash
echo ************************************************
echo Starting the replica set
echo ************************************************

sleep 2 | echo Sleeping
mongo mongodb://mongo-rs0-1:27017 replicaSet.js
sleep 2 | echo Sleeping
mongo mongodb://mongo-rs0-1:27017/appdata dbInit.js
mongo mongodb://mongo-rs0-2:27017/appdata dbInit.js
mongo mongodb://mongo-rs0-3:27017/appdata dbInit.js