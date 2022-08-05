## Running the code using Docker
  - `docker compose build` it will build the necessary images to create the containers
  - `docker compose up -d` it will start the containers
  - To run the python code, we have to enter the data_engineer container, so run `docker compose exec data_engineer bash`
  - Now run `python3 data_engineer/load_data.py` to create tables and load the data
  - Once the data have been loaded run `python3 data_engineer/main.py` to execute all queries
  - Query results are also saved to **data_engineer/query_results** 