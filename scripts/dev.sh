#!/bin/bash

flask --app src/server/server.py run &

cd src/client && npm run dev &