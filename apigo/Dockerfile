FROM golang AS builder

WORKDIR /app
ADD . .

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -ldflags '-w -s' -a -installsuffix cgo -o /go/bin/server

FROM alpine

RUN apk add --no-cache ca-certificates

COPY --from=builder /go/bin/server /go/bin/server

# Run the hello binary.
ENTRYPOINT ["/go/bin/server"]