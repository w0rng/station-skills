# debt

### Launch in local server
1. run `docker build . -t debt-back`
2. run `docker run -p "8000:8000" -t debt-back`

### For CD

1. add `DOCKER_USERNAME`, `DOCKER_PASSWORD` in github secrets
2. push on main or run github action