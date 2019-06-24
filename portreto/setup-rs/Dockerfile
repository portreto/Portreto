FROM mongo

#Create app directory
WORKDIR /usr/src/configs

#Install app dependencies
COPY replicaSet.js .
COPY dbInit.js .
COPY dbInit_auth.js .
COPY setup.sh .

CMD ["./setup.sh"]