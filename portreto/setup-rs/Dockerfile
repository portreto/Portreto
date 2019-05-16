FROM mongo

#Create app directory
WORKDIR /usr/src/configs

#Install app dependencies
COPY replicaSet.js .
COPY dbInit.js .
COPY setup.sh .

CMD ["./setup.sh"]