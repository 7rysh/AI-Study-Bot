#!/bin/bash

#Start uvicorn in background using &
cd /app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 &

sleep 3 #Wait for uvicorn start

#Start streamlit in the front 
cd /app/frontend
streamlit run front.py \
    --server.port 7860 \
    --server.address 0.0.0.0 \
    -- server.headless true