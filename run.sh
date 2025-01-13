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
RUN python -c 'from marker.models import load_all_models; load_all_models()' # tu mieliśmy z dockera skopiowane RUN (na początku) w rezultacie się nie ściągały modele; po wyrzuceniu tego dużo dłużej się ładuje; to racze nie porblem bo za chwilę i tak eksport markera ale zmieni się działanie run bo od teraz zacznie pobierać te modele markera

echo "Starting Celery worker"
cd app
. celery -A main.celery worker --loglevel=info --pool=solo & # to scale by concurrent processing please run this line as many times as many concurrent processess you want to have running
#^ Celery nam zostawia workera włączonego nawet jak user crtl+c/d na terminalu :( ja się właśnie doktoryzowałem z całego celery, ale coś mnie tknęło i odpalłem htopa a tam 4x celery poodpalane z różnymi komednami :) w MR jest rozwiązanie na dev pytanie czy nie robimy na prod czegoś podobnego

echo "Starting FastAPI server"
if [ $APP_ENV = 'production' ]; then 
    uvicorn main:app --host 0.0.0.0 --port 8000;
else 
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload;  
fi