FROM golang:1.25.1

RUN go install github.com/googleapis/genai-toolbox@v0.15.0
WORKDIR /app
COPY tools.yaml /app/

ENTRYPOINT [ "genai-toolbox", "--tools-file", "/app/tools.yaml", "--address", "0.0.0.0" ]
