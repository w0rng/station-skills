FROM golang:latest as prod

RUN mkdir /app

ADD debt/src /app/
WORKDIR /app
RUN go build -o main .
CMD ["./main"]