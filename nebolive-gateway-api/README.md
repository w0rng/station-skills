# nebolive-gateway-api

### Launch in local server
1. add `.env` file by `.env.example`
2. run `docker build . -t nebolive-back`
3. run `docker run --env-file .env -p 8080:8080 nebolive-back`

### For CD
1. add `DOCKER_USERNAME`, `DOCKER_PASSWORD` in github secrets
2. push on main or run github action