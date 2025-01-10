#!/bin/bash

pip install -r app/requirements.txt

if [ ! -f .env.localhost ]; then
  cp .env.localhost.example .env.localhost
fi 

set -a; source .env.localhost; set +a

echo "Starting Ollama Server"
ollama serve &

echo "Pulling LLama3.1 model"
ollama pull llama3.1

echo "Pulling LLama3.2-vision model"
ollama pull llama3.2-vision

echo "Starting Redis"
docker run  -p 6379:6379 --restart always --detach redis &

echo "Your ENV settings loaded from .env.localhost file: "
printenv

echo "Downloading models"
RUN python -c 'from marker.models import load_all_models; load_all_models()'

echo "Starting Celery worker"
cd text-extract-api
celery -A main.celery worker --loglevel=info --pool=solo & # to scale by concurrent processing please run this line as many times as many concurrent processess you want to have running

echo "Starting FastAPI server"
if [ $APP_ENV = 'production' ]; then 
    uvicorn main:app --host 0.0.0.0 --port 8000;
else 
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload;  
fi