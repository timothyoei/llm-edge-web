# llm-edge-web
Web App for LLMs on EDGE Devcies

## Development

Start the container and attach your editor the running container (e.g., VSCode Dev Containers extension)
```
docker compose up -d
```

If you want to run both the client and server, you can use the following:
Run the development script
```
./scripts/dev.sh
```

If you want to run them separately, you can use the following:

**Client**
```
cd src/client && npm run dev
```

**Server**
```
python3 src/server/server.py
```

Clean up the container when finished
```
docker compose down --rmi all
```
