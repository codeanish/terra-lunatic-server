# terra-lunatic-server

## Dependencies

Create a .env file in the root project directory. Add the appropriate URLs required into the .env file to map to the settings.py file in the api project. If you need a .env file, contact Anish.

## Running

This project utilises docker-compose to build two docker images and run them. After you've created the .env file, run the following commands:

### `docker-compose build`
### `docker-compose up -d`

This should bring up the two containers. The first container is the API, the second container makes sync requests to the API container to pull fresh data from flipside crypto. It may take a few minutes for the API to be filled with data and useable, you can see this if you check the logs of the API container. Once it's initialised, it should retain data for as long as the container is running. There is no persistence solution implemented at this stage, so on startup, there will always be a slight delay to pull all the data from flipside.