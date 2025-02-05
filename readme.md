# airflow-etl-server-access-log

This project demonstrates an ETL pipeline built with Apache Airflow. 
The pipeline downloads a web server access log, extracts key fields (timestamp and visitor ID), 
transforms the data, and writes the results to an output file. The project uses Docker Compose for 
containerized deployment, making it easy to set up and run.

## Setup and Running the Project

1. **Clone the repository:**

```bash
git clone https://github.com/AlexMasCode/airflow-etl-server-access-log.git
cd airflow-etl-server-access-log
```

2. **Initialize the Airflow database:**

Before starting the containers, initialize the Airflow metadata database:
```bash
docker-compose run --rm airflow-webserver airflow db init
```

3. **Start the Docker containers:**

Bring up all services in detached mode:
```bash
docker-compose up -d
```

4. **Access the Airflow UI:**

Open your web browser and navigate to http://localhost:8080. You can trigger the ETL DAG manually or wait for its scheduled run.


## How It Works
- Download File: A Python task downloads the web server access log from a public URL.
- Extract Data: Another task reads the downloaded log and extracts the timestamp and visitor ID.
- Transform Data: The extracted data is transformed (e.g., converted to uppercase).
- Load Data: The transformed data is written to an output file.

All files are stored in the data directory on the host, thanks to volume mapping (./data:/opt/airflow/data), so you can easily inspect the results.

## Stopping the Project

To stop the containers, run:
```bash
  docker-compose down
```