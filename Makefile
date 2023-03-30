.PHONY: build run clean test
.SILENT: clean build run test

clean:
	echo "Removing confluent, mongo, spark and app stacks, if there are any"
	docker stack rm app
	docker stack rm spark
	docker stack rm confluent
	docker stack rm mongo

build:
	echo "Pulling Required images"
	docker-compose -f mongo/docker-compose.yml pull
	docker-compose -f confluent/docker-compose.yml pull
	docker-compose -f spark/docker-compose.yml pull

	echo "Building application images"
	docker-compose build

run:
	echo "Running MongoDB"
	docker stack deploy -c ./mongo/docker-compose.yml mongo
	sleep 10
	echo "Running Confluent Kafka"
	docker stack deploy -c ./confluent/docker-compose.yml confluent
	sleep 10
	until curl --connect-timeout 5 --silent 127.0.0.1:8083; do echo "Confluent Connect takes a few minutes to start. Please wait..."; sleep 20; done
	echo "Running Spark Master"
	docker stack deploy -c ./spark/docker-compose.yml spark
	sleep 5
	echo "Running Spark Worker"
	docker service scale spark_spark-worker=1
	sleep 5
	echo "Running Spark Job Service"
	docker service scale spark_spark-job=1

	$(eval url := "127.0.0.1:8080")
	$(eval search_text := "Running Applications (1)")
	until curl --silent $(url) | grep -q $(search_text); do echo "Spark job not ready yet. Please wait..."; sleep 10; done

	echo "Running Generator and main app APIs"
	docker stack deploy -c docker-compose.yml app

	$(eval url := "127.0.0.1:7000/docs")
	$(eval search_text := "IoT Device Message Generator")
	until curl --silent $(url) | grep -q $(search_text); do echo "Starting Up. Please wait..."; sleep 10; done

	$(eval url := "127.0.0.1:8000/docs")
	$(eval search_text := "PAAI")
	until curl --silent $(url) | grep -q $(search_text); do echo "Starting Up. Please wait..."; sleep 10; done

	echo "All services are deployed to the Docker Swarm. You can open the following URLs."
	echo "IoT Device Data Generator: http://127.0.0.1:7000/docs"
	echo "Main App Queries API Endpoint: http://127.0.0.1:8000/docs"
	echo "MongoDB Express: http://127.0.0.1:8081"
	echo "Spark Master UI: http://127.0.0.1:8080"
	echo "Kafka Control Center: http://127.0.0.1:9021"

test:
	echo "Performing unit testing"
	pytest -v paai/tests/unit/device_raw_messages.py
