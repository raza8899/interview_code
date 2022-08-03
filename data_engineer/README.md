# Challenge - Courses and Certificates

You are provided with 3 files:

- [users.json](./users.json) - File with fake user data
- [courses.json](./courses.json) - File with courses data
- [certificates.json](./certificates.json) - File with data about which users completed which courses and when they started/finished

## Specs

Given the data you are provided with, we would like you to build:

- A script that loads all 3 data sources into a database structure
- You provide the sql queries for the following analyzes
  - average complete time of a course
  - average amount of users time spent in a course
  - average amount of users time spent for each course individually
  - report of fastest vs. slowest users completing a course
  - amount of certificates per customer
- Your solution does run in a local docker(-compose) setup

## Bonus points, not mandatory

- You provide a possibility to visualize the data in a ui tool with graphs
- You provide addtional possibilities of analyzing the data via that ui tool (e.g. which times users start mostly, most frequent used courses, etc.)

## Running the code using Docker
  - `docker compose build` it will build the necessary images to create the containers
  - `docker compose up -d` it will start the containers
  - To run the python code, we have to enter the data_engineer container, so run `docker compose exec data_engineer bash`
  - Now run `python3 data_engineer/load_data.py`
  - Once the data have been loaded run `python3 data_engineer/main.py` to execute all queries
  - Query results are also saved to **data_engineer/query_results** 