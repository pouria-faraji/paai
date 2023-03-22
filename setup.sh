#!/bin/bash
echo "Removing confluent and mongo stacks, if there are any"
docker stack rm app
docker stack rm confluent
docker stack rm mongo

sleep 2

echo "Deploying MongoDB service"
docker stack deploy -c ./mongo/docker-compose.yaml mongo

echo "Checking MongoDB for deploying Confluent Kafka"
./confluent/check_mongo_alive.sh

echo "Deploying Confluent Kafka services"
docker stack deploy -c ./confluent/docker-compose.yaml confluent
