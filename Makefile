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
	echo "Running MogoDB"
	docker stack deploy -c ./mongo/docker-compose.yml mongo
	sleep 10
	echo "Running MogoDB"
	docker stack deploy -c ./confluent/docker-compose.yml confluent
	sleep 10
	docker stack deploy -c ./spark/docker-compose.yml spark
	sleep 5
	# docker service update spark_spark-worker --force
	docker service scale spark_spark-worker=1
	sleep 5
	# docker service update spark_spark-job --force
	docker service scale spark_spark-job=1

	$(eval url := "127.0.0.1:8080")
	$(eval search_text := "Running Applications (1)")
	until curl --silent $(url) | grep -q $(search_text); do echo "Spark job not ready yet..."; sleep 10; done

	echo "Running Generator and main app APIs"
	docker stack deploy -c docker-compose.yml app

	echo "IoT Device Data Generator: http://127.0.0.1:7000/docs"
	echo "Main App Queries API Endpoint: http://127.0.0.1:8000/docs"
	echo "MongoDB Express: http://127.0.0.1:8081"
	echo "Spark Master UI: http://127.0.0.1:8080"