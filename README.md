# pdf2txt

[![Code Inc.](https://img.shields.io/badge/Code%20Inc.-Document%20Cloud-blue)](https://www.codeinc.co)
[![Docker Image CI](https://github.com/codeinchq/pdf2txt/actions/workflows/docker-image.yml/badge.svg)](https://github.com/codeinchq/pdf2txt/actions/workflows/docker-image.yml)
[![Docker Image Version](https://img.shields.io/docker/v/codeinchq/pdf2txt?sort=semver&label=Docker%20Hub&color=red)](https://hub.docker.com/r/codeinchq/pdf2txt/tags)

This repository contains a simple containerized API to convert PDF documents to text using [Mozilla's pdf.js](https://mozilla.github.io/pdf.js/) and [pdf.js-extract](https://www.npmjs.com/package/pdf.js-extract).

The image is available on [Docker Hub](https://hub.docker.com/r/codeinchq/pdf2txt) under the name `codeinchq/pdf2txt`.

## Configuration

By default, the container listens on port 3000. The port is configurable using the `PORT` environment variable.

## Usage

All requests must by send in POST to the `/extract` endpoint with a `multipart/form-data` content type. The request must contain a PDF file with the key `file`. 

Additional parameters can be sent to customize the conversion process:
* `firstPage`: The first page to extract. Default is `1`.
* `lastPage`: The last page to extract. Default is the last page of the document.
* `password`: The password to unlock the PDF. Default is none.
* `normalizeWhitespace`: If set to `true`, the server normalizes the whitespace in the extracted text. Default is `true`.
* `format`: The output format. Supported values are `text` (the server returns the raw text as `text/plain`) or `json` (the server returns a JSON object as `text/json`). Default is `text`.

The server returns `200` if the conversion was successful and the images are available in the response body. In case of error, the server returns a `400` status code with a JSON object containing the error message (format: `{error: string}`).

### Example

#### Step 1: run the container using Docker
```bash
docker run -p "3000:3000" codeinchq/pdf2txt 
```

#### Step 2: convert a PDF file to text
Convert a PDF file to text with a JSON response:
```bash
curl -X POST -F "file=@/path/to/file.pdf" http://localhost:3000/extract -o example.json
```
Convert a PDF file to text:
```bash
curl -X POST -F "file=@/path/to/file.pdf" http://localhost:3000/extract
```

Extract a password-protected PDF file's text content as JSON and save it to a file:
```bash
curl -X POST -F "file=@/path/to/file.pdf" -F "password=XXX" -F "format=json" http://localhost:3000/extract -o example.json
```

### Health check

A health check is available at the `/health` endpoint. The server returns a status code of `200` if the service is healthy, along with a JSON object:
```json
{ "status": "up" }
```

## Client

A PHP 8 client is available at on [GitHub](https://github.com/codeinchq/document-cloud-php-client) and [Packagist](https://packagist.org/packages/codeinc/document-cloud-client).

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/codeinchq/pdf2txt?tab=MIT-1-ov-file) file for details.
