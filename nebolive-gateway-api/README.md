# nebolive-gateway-api

### Description
A skill that allows you to find out the outdoor air quality index

### Launch in local server
1. add `.env` file by `.env.example`
2. run `docker build . -t nebolive-back`
3. run `docker run --env-file .env -p 8080:8080 nebolive-back`
