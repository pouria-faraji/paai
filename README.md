# Programming Assignment - AI Engineer
This repository contains the source code for an application which generates and sends fake IoT device data to a web service. Also, aggregation queries such as average, maximum and minimum for a specific timeframe can be executed in the web service.

## Architecture
The web service is designed and developed using microservices architecture, and the container orchestration is done by [Docker Swarm](https://docs.docker.com/engine/swarm/). There are five main services:

1. Generator
2. Paai (Abbreviation of *Programming Assignment AI*)
3. MongoDB
4. Confluent Kafka
5. Spark

### Generator
The *generator* is responsible for sending IoT data. There are 4 main device types which are implemented in this web service: *Thermostat, Barometer, Hygrometer, Heart Rate Meter*

Each device has its own data model, for instance, the following are sample data for a thermostat and a barometer:
```json
{
    "device_id": "1",
    "timestamp": "2023-03-28T20:04:22Z",
    "temperature": 25.2,
    "tag": "Thermostat"
}
```
```json
{
    "device_id": "2",
    "timestamp": "2023-03-28T20:05:22Z",
    "pressure": 1060.5,
    "tag": "Barometer"
}
```
The *generator* sends data every second for the specified number of devices in the generator API doc page.

Moreover, the programming language used for the *generator* and the *paai* service is [Python](https://www.python.org/) and for generating and sending data, `MultiThreading`  is used to avoid blocking the main thread.

### Paai
The *paai* service is responsible to receive data, parse, validate, and transform it and send it to a topic in the Kafka service.

The web framework used for building APIs in Python is [FastAPI](https://fastapi.tiangolo.com/).

There is an API endpoint which receives data from the *generator*, validates it and transform it into a `DeviceMessage` class, so all device types can have a same data model. A sample *DeviceMessage* is like the following:
```json
{
    "device_id": "1",
    "timestamp": "2023-03-28T20:04:22Z",
    "sensor": "temperature",
    "value": 25.2
}
```

After transforming, they are produced directly to a Kafka topic called `processed_messages`

Also, in order to increase scalability, multiple replicas of this service should be deployed, so that the service and the *swarm's load balancing* can manage heavy loading of the incoming data more efficiently. In the current implementation, 3 replicas of the service are deployed.

### MongoDB
MongoDB is the main database for the application to store device messages and also aggregated messages.

Other services such as Kafka and Spark are responsible to store messages in the database.

There is also another service called `mongo-express` for viewing and managing the MongoDB using a web UI.

### Kafka
Kafka is responsible to receive streaming data constantly coming from the *paai* service.

There is also a *MongoDB Sink Connector* which automatically sends the received data from Kafka to MongoDB. 

There are multiple services for the Kafka as the following:
- **Zookeeper:** For broker management and topic configurations
- **Broker:** For Streaming messages management
- **Connect:** For directing messages from Kafka to other services such as MongoDb, and vice versa
- **Control Center:** For viewing and managing the Kafka cluster using a web UI
- **Kafka Operator:** For initialization operations, such as installing the connector and creating topics

### Spark
This service is responsible for processing on real-time streaming data and executing different operations such as aggregation to calculate average, maximum and minimum of data for a specific time window.

There is a *spark job* defined to connect to the Kafka topic and receive the streaming data from Kafka. Aggregate and calculate average, maximum and minimum for a time window of 10 seconds (which can be changed in the [pyspark_job.py](./spark/pyspark_job.py) file). Then the data is directed to a collection in MongoDB.

## Limitations
The current implementation has a few limitations primarily due  to the limited resources available, such as memory in the development environment.

The application is intended for stand-alone use on a single machine, which is why only one broker replica is deployed in the Kafka service. While in a production environment with greater computing resources and multiple machines, it is recommended to deploy multiple replicas of the broker for optimal performance.

Due to the same resource limitations, Spark currently operates with only one worker node. However, in a multi-machine environment with greater computing resources, deploying multiple worker nodes can significantly enhance performance.

Moreover, To enhance data availability, it is recommended to leverage multiple instances of MongoDB nodes using replica sets.

## Installing and Running
### Prerequisites
In order to install and run the application, [Docker](https://www.docker.com/get-started/) must be already installed. Also it should be in swarm mode using the following command:
```
docker swarm init
```
Also make sure that the following port numbers are open and free:
- 8000 - Main web service
- 7000 - Generator web service
- 2181 - Confluent Zookeeper
- 9092 - Confluent Broker
- 9101 - Confluent Broker
- 8083 - Confluent Connect
- 9021 - Confluent Control Center
- 8080 - Spark Master
- 7077 - Spark Master
- 8081 - MongoDB Express
- 27017 - MongoDB

Also by running the following command, make sure that `make` utility is installed and available:
```
sudo apt-get install build-essential
```

### Building
To build the application, all docker images must be pulled and built. You can use the following command to automatically pull and build all docker images:
```
make build
```

### Running
To run the application, all docker services must be deployed to the Docker Swarm. You can use the following command to automatically deploy all services:
```
make run
```
After finishing the run command, you can access different services web UI page in the following URLs:
- **IoT Device Data Generator:** [http://127.0.0.1:7000/docs](http://127.0.0.1:7000/docs)
- **Main App Queries API Endpoint:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **MongoDB Express:** [http://127.0.0.1:8081](http://127.0.0.1:8081)
- **Spark Master UI:** [http://127.0.0.1:8080](http://127.0.0.1:8080)
- **Kafka Control Center:** [http://127.0.0.1:9021](http://127.0.0.1:9021)
### Testing
For testing, only unit testing is implemented for the *paai* service to test validation of raw and processed device messages.

In order to run tests, [Python](https://www.python.org/) and  [pytest](https://docs.pytest.org/en/7.1.x/getting-started.html) must be already installed. You can install the pytest framework by using the following command:
```
pip install -U pytest
```
Then for executing the test you can run the following command:
```
make test
```
### Uninstalling
To remove all services from the swarm run the following command:
```
make clean
```

## Adding Prediction Model
To build a pipeline for running prediction models, we can extend our implementation with the following components and data flow:
### Model Training
First we need to build and train our predicition model on the historical data using machine learning frameworks such as [TensorFlow](https://www.tensorflow.org/overview), [scikit-learn](https://scikit-learn.org/stable/), or [Spark's MLlib](https://spark.apache.org/mllib/).

We can use the historical data stored in the MongoDB as our model's training and validation data sets.

### Model Deployment
We can have another containerized service to be the host of our trained model deployed in the docker swarm. Then we can have an API endpoint (for instance using [FastAPI](https://fastapi.tiangolo.com/)) inside the service to serve our trained model.

### Real-time Prediction
To achieve real-time predictive capabilities while data is in motion, we can employ a Spark job that reads streaming data from a Kafka topic, performs transformations, rescaling, and cleaning, and then makes predictions on each record. Alternatively, we can use Spark's batch processing to predict each batch of data using our trained model. Finally, we can route the predicted data to either another Kafka topic for further processing or store the results in a MongoDB collection.

### Data
Regarding the data itself, there are a few factors that we should take into account:
1. In order to predict with a high accuracy, our model should be trained on data which are very similar to real-world data, with similar diversity, completeness, and distribution.
2. If we want our model to perform well on unseen data, it should be generalized well by exploiting different techniques which are frequently used for avoiding overfitting, such as cross-validation, regularization, and training with more data.
3. Preprocessing the data is also important. We need to handle transformation, normalization, missing values, outliers and removing noise in our data pipeline.
4. Data can contain sensitive information about users or devices, so it is important to protect data from unauthorized access by using encryption, and access control. 
