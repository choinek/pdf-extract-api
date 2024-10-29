# pdf-extract-api

Convert any image or PDF to Markdown text or JSON structured document with super-high accuracy, including tabular data, numbers or math formulas.

The API is built with FastAPI and uses Celery for asynchronous task processing. Redis is used for caching OCR results.

![hero doc extract](ocr-hero.webp)

## Features:
- **PDF to Markdown** conversion with very high accuracy using different OCR strategies including [marker](https://github.com/VikParuchuri/marker), [surya-ocr](https://github.com/VikParuchuri/surya) or [tessereact](https://github.com/h/pytesseract)
- **PDF to JSON** conversion using Ollama supported models (eg. LLama 3.1)
- **Distributed queue processing** using [Celery][(](https://docs.celeryq.dev/en/stable/getting-started/introduction.html))
- **Caching** using Redis - the OCR results can be easily cached prior to LLM processing
- **CLI tool** for sending tasks and processing results 

## Getting started

### Prerequisites

- Docker
- Docker Compose

### Clone the Repository

```sh
git clone https://github.com/CatchTheTornado/doc-extract-api.git
cd doc-extract-api
```

### Setup environmental variables

Create `.env` file in the root directory and set the necessary environment variables. You can use the `.env.example` file as a template:

`cp .env.example .env`

Then modify the variables inside the file:

```bash
REDIS_CACHE_URL=redis://redis:6379/1
OLLAMA_API_URL=http://ollama:11434/api

# CLI settings
OCR_URL=http://localhost:8000/ocr
RESULT_URL=http://localhost:8000/ocr/result/{task_id}
CLEAR_CACHE_URL=http://localhost:8000/ocr/clear_cache
```

### Build and Run the Docker Containers

Build and run the Docker containers using Docker Compose:

```bash
docker-compose up --build
```

This will start the following services:
 - **FastAPI App**: Runs the FastAPI application.
 - **Celery Worker**: Processes asynchronous OCR tasks.
 - **Redis**: Caches OCR results.
 - **Ollama**: Runs the Ollama model.

## Endpoints

### OCR Endpoint
- **URL**: /ocr
- **Method**: POST
- **Parameters**:
  - **file**: PDF file to be processed.
  - **strategy**: OCR strategy to use (marker or tesseract).
  - **async_mode**: Whether to process the file asynchronously (true or false).
  - **ocr_cache**: Whether to cache the OCR result (true or false).

Example:

```bash
curl -X POST "http://localhost:8000/ocr" -F "file=examples/example-mri.pdf" -F "strategy=marker" -F "async_mode=true" -F "ocr_cache=true"
```

### OCR Result Endpoint
- **URL**: /ocr/result/{task_id}
- **Method**: GET
- **Parameters**:
  - **task_id**: Task ID returned by the OCR endpoint.

Example:

```bash
curl -X GET "http://localhost:8000/ocr/result/{task_id}"
```

### Clear OCR Cache Endpoint
 - **URL**: /ocr/clear_cache
 - **Method**: POST

Example:
```bash
curl -X POST "http://localhost:8000/ocr/clear_cache"
```


### Ollama Pull Endpoint
- **URL**: /llm_pull
- **Method**: POST
- **Parameters**:
  - **model**: Pull the model you are to use first

Example:

```bash
curl -X POST "http://localhost:8000/llama_pull" -H "Content-Type: application/json" -d '{"model": "llama3.1"}'
```

### Ollama Endpoint
- **URL**: /llm_generate
- **Method**: POST
- **Parameters**:
  - **prompt**: Prompt for the Ollama model.
  - **model**: Model you like to query

Example:

```bash
curl -X POST "http://localhost:8000/llama_generate" -H "Content-Type: application/json" -d '{"prompt": "Your prompt here", "model":"llama3.1"}'
```

## CLI tool

The project includes a CLI for interacting with the API. To make it work first run:

```bash
cd client
pip install -r requirements.txt
```

### Upload a File for OCR

```bash
python client/cli.py ocr --file examples/example-mri.pdf --ocr_cache
```

### Get OCR Result by Task ID

```bash
python client/cli.py result -task_id {your_task_id_from_upload_step}
```

### Clear OCR Cache

```bash
python client/cli.py clear_cache
```

### Pull LLama model

```bash
python llm_pull --model llama3.1
```

### Test LLama

```bash
python llm_generate --prompt "Your prompt here"
```

## License
This project is licensed under the GNU General Public License. See the [LICENSE](LICENSE.md) file for details.

**Important note on [marker](https://github.com/VikParuchuri/marker) license***:

The weights for the models are licensed `cc-by-nc-sa-4.0`, but Marker's author will waive that for any organization under $5M USD in gross revenue in the most recent 12-month period AND under $5M in lifetime VC/angel funding raised. You also must not be competitive with the [Datalab API](https://www.datalab.to/). If you want to remove the GPL license requirements (dual-license) and/or use the weights commercially over the revenue limit, check out the options [here](https://www.datalab.to/).



## Contact
In case of any questions please contact us at: info@catchthetornado.com