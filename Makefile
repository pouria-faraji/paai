.PHONY: build run clean test

clean:
	echo "Removing confluent, mongo, spark and app stacks, if there are any"
	docker stack rm app
	docker stack rm confluent
	docker stack rm mongo
	docker stack rm spark

	echo "Removing networks, if there are any left"
	docker network rm app_default
	docker network rm confluent_default
	docker network rm mongo_default
	docker network rm spark_default

build:
	echo "Building application images"
	docker-compose build

run:
	echo "Running application"
	docker stack deploy -c ./mongo/docker-compose.yml mongo
	sleep 10

