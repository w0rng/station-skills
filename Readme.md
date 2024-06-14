# station-skills

### Launch in local server

1. add `.env` by `.env.example`
2. run `docker-compose pull`
3. run `docker-compose up -d`

### For CD

1. add `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`, `SSH_PASSPHRASE`, `NEBOLIVE_TOKEN`, `NEBOLIVE_CODE` in github secrets
2. push on main or run github action