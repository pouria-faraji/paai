FROM bitnami/spark:3.3

USER root
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

CMD ["bin/spark-class", "org.apache.spark.deploy.master.Master"]
