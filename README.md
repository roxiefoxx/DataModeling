# Udacity Data Modeling Project: Song Play Analysis

## Table of Contents
- [Introduction](#introduction)
- [Database Schema Design](#database-schema-design)
- [The Data](#the-data)
- [ETL Pipeline](#etl-pipeline)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Conclusion](#conclusion)

## Introduction

This project focuses on creating a database for Sparkify, a fictional music streaming startup. Sparkify has been collecting data on songs and user activity, but they lack an efficient way to query and analyze this data. The goal of this project is to design a database schema and build an ETL (Extract, Transform, Load) pipeline in python to enable Sparkify to analyze their data efficiently.

### Purpose of the Project

The purpose of the project is to facilitate song play analysis for Sparkify. By storing data on songs, artists, users, and song plays, the database allows Sparkify to answer a wide range of analytical questions, such as:

- What are the most popular songs?
- Who are the most active users?
- What is the distribution of song plays by location?
- How long do users typically listen to songs?

With this database, Sparkify can gain valuable insights into user behavior and preferences, which can inform decisions related to content recommendation, user engagement, and business strategy.

## Requirements
This project was completed on a MacBook Pro running Ventura v13.5.1, using Visual Studio Code. 

While other environments will be different and have separate results, these were the conditions used in this project:
- Python v3.9.12
- Postgres.app v2.6.7

This specific module will need to be installed to use the provided scripts

```
pip install psycopg2-binary
pip install libpq
```

According to this [Stackoverflow](https://stackoverflow.com/questions/61054203/cant-install-libpq-dev), Anaconda's distribution of Python to bypass the libpq problem.

## The Files
The project files from Udacity can be downloaded from [project-template.zip](https://video.udacity-data.com/topher/2020/December/5fcdb6f5_project-template/project-template.zip). It will contain:
- /data/
- etl.ipynb
- test.ipynb
- create_tables.py
- etl.py
- README.md
- sql_queries.py

## The Data

All the data are contained in JSON files in the /data directory separated into song_data and log_data, each with nested folders within them. The are both real sample data from the Million Song Dataset.

### Song datasets
These files contain metadata about a song and its artist. Here is a glimpse at the contents of the file located here:
```
data/song_data/A/A/A/TRAAAAW128F429D538.json
```

```
{"num_songs": 1, "artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null, "artist_longitude": null, "artist_location": "California - LA", "artist_name": "Casual", "song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```

### Log datasets

This data is based on information gathered about users of the streaming app, what they listened to and what time. Here is another look at the file located at:
```
data/log_data/2018/11/2018-11-01-events.json
```

```
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
```

## Database Schema Design

The database schema is designed with the star schema to efficiently store and query data related to songs, artists, users, and song plays. It consists of the following tables:

### Fact Table 

Fact tables store quantitative data that is detailed at an atomic level (i.e., having time dimension in millisecond or each line a separate transaction).

1. **songplays**: Records of song plays, including information about the song, user, and timestamp.
   - Columns: songplay_id (PRIMARY KEY), start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Table

Dimension tables are descriptive or contain contextual attributes.

2. **users**: Information about Sparkify users.
   - Columns: user_id (PRIMARY KEY), first_name, last_name, gender, level

3. **songs**: Information about songs in the Sparkify catalog.
   - Columns: song_id (PRIMARY KEY), title, artist_id, year, duration

4. **artists**: Information about artists in the Sparkify catalog.
   - Columns: artist_id (PRIMARY KEY), name, location, latitude, longitude

5. **time**: Timestamp data extracted from song plays.
   - Columns: start_time (PRIMARY KEY), hour, day, week, month, year, weekday

This schema follows the principles of a star schema, which simplifies analytical queries and allows for efficient aggregation and filtering.

Justification for the schema design:
- **songplays** contains the fact data and serves as the central table for analyzing song plays.
- **users**, **songs**, and **artists** are dimension tables that provide additional details about users, songs, and artists.
- **time** is a time dimension table that aids in time-based analysis.

## ETL Pipeline

The ETL (Extract, Transform, Load) pipeline is responsible for ingesting and processing data to populate the database tables.

The ETL process consists of two main steps:

1. **Data Extraction**: Data is extracted from two sources:
   - JSON logs that contain user activity data, such as song plays and user information.
   - JSON files that contain metadata about songs and artists.

2. **Data Transformation and Loading**: The extracted data is transformed and loaded into the appropriate tables using Python and SQL scripts. The ETL process includes the following steps:
   - Parsing and processing JSON log files to create records for the **songplays** and **time** tables.
   - Extracting and processing song and artist data from JSON files to populate the **songs** and **artists** tables.
   - Loading user data into the **users** table.
   - Inserting records into the **songplays** table, including song and artist references.

The ETL pipeline ensures that the database is kept up to date with new data and can be run periodically to refresh the database with the latest user activity and song metadata.

## Usage

To set up and run the ETL pipeline and database:

1. Clone this repository to your local machine.

2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```

3. Create a PostgreSQL database for Sparkify. Modify the database connection settings in the `create_tables.py` and `etl.py` scripts to match your database configuration.

4. Run the following scripts in the specified order:
   - `create_tables.py`: This script will create the necessary tables in the database.
   - `etl.py`: This script will execute the ETL process to populate the tables with data.

5. With the database populated, you can run analytical queries to extract insights from the Sparkify data.

## Conclusion