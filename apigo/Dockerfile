FROM golang AS builder

WORKDIR /app
ADD . .
RUN GOOS=linux GOARCH=amd64 go build -ldflags="-w -s" -o /go/bin/server

FROM alpine

RUN apk add --no-cache ca-certificates

COPY --from=builder /go/bin/server /go/bin/server

# Run the hello binary.
ENTRYPOINT ["/go/bin/server"]