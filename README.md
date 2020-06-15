# Graphize


Create story with image / video. Geo-tag your story. Find stories from all around the world or from your local vicinity. Discover stories of people you know about.


## API endpoints

1. `/grapher/create-graphie/` - POST request

    ```
    grapher_name (string) - Identifier for Grapher posting the story.
    
    subject (string) - Title of the story.
    
    description (string)
    
    graphie (file) - Image / Video file for your story.
    
    latitude (decimal) - considered only when longitude is provided and have a valid value.
    
    longitude (decimal) - considered only when latitude is provided and have a valid value.
    ```
    
    This API will validate all the information and store the story. The uploaded file will be stored at a temporary location and queued for further processing. The story will not be fetched by the 2nd API until the processing of the file associated with that story is completed.

2. `grapher/get-graphie-list/` - POST request

    ```
    grapher_name (string) - Fetch story of a particular grapher.

    unprocessed (boolean) - If true, will fetch stories that've just been posted and whose processing is still in queue.

    radius (integer) - If latitude & longitude are given, fetches stories within the given radius in meters. Default - 5000m

    latitude (decimal) & longitude (decimal) - Used as point of origin to find stories in given radius from it.
    ```

    This API will fetch all stories based on the given request parameters and return a list. Each object in list will have `grapher_name`, `subject`, `description` and `uuid`. You can use the `uuid` in the 3rd API to fetch the image / video file associated with it.

3. `/get-graphie-illustration/` - POST request 

    ```
    uuid (UUID) - Fetches the path of file associated with the story of the given value
    ```
    This API will fetch the path to the image / video file.


## PREREQUISITE

    - Make sure you have **python3.7** on your system. I haven't tested it with other versions and it might throw in some errors

    - Make sure you have **postgres** and **postgis** installed in your system. If you are a mac user, run `brew install postgresql` and `brew install postgis` to install them. The backend db engine is set as **Postgis** to allow geometric capabilities. Linux users, make sure you have `postgres` installed - `sudo apt install postgresql postgresql-contrib`, if so, then run `sudo apt install postgis`.

    - Once **Postgis** is installed, login as `postgres` user in the terminal and type `psql`. From `psql` console run `CREATE EXTENSION postgis;` and `CREATE EXTENSION postgis_topology;`.

    - Make sure you have **Rabbitmq** installed in your system. Linux user can install it by `sudo apt-get install rabbitmq-server` and run the service by `sudo systemctl start rabbitmq-server`. Mac users can install it through `brew install rabbitmq` and run the service by `brew services start rabbitmq`.


## How to run the app

    ```
    # Create a virtual environment with python3.7
    virtualenv -p python3 venv-graphize
    source venv-graphize/bin/activate

    # Clone the repo and install all the requirements
    git clone https://github.com/Zlash65/Graphize.git graphize

    cd graphize

    pip3 install -r req.txt

    python manage.py test

    # if all test cases are passing, the APIs are good to work
    python manage.py runserver

    # Use Postman or any other tool to test the above endpoints.
  ```