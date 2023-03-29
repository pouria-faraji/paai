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

There is an API endpoint which receives data from the *generator*, validates it and transform it into a `DeviceMessage`, so all device types can have a same data model. A sample *DeviceMessage* is like the following:
```json
{
    "device_id": "1",
    "timestamp": "2023-03-28T20:04:22Z",
    "sensor": "temperature",
    "value": 25.2
}
```

After transforming, they are produced directly to a Kafka topic called `processed_messages`

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

### Building

### Running