# Core Server

## Quick Start

### With Pypi

Install product with:

```shell script
pip install ni-core-server==0.1.0
```

To launch server:

```shell script
core_server
```

Some options are available:

* `-p` | `--port` server port listening. Default: 8888
* `-l` | `--log-level` log level. Default 'INFO'

### With Docker

Install product with:

```shell script
docker pull primael94/ni-core-server:0.1.0
```

To launch server:

```shell script
docker run -d -p 8888:8888 primael94/ni-core-server:0.1.0
```

Some environment variables are available:

* `RABBIT_HOST` Host IP of rabbit. Default: rabbit
* `LEVEL_DEBUG` Log level. Default 'INFO'
* `PORT_SERVER` Server port listening. Default: 8888

### With docker-compose

```yaml
---

version: "3"

services:
  rabbitmq:
    image: rabbitmq:3-management
  core-server:
    build:
      .
    environment:
      - RABBIT_HOST=rabbitmq
      - LEVEL_DEBUG=DEBUG
    depends_on:
      - rabbitmq
    ports:
    - 8888:8888
```

## Under the hood

### Pipeline concept

When we submitting an image, that create a dedicated pipeline.

A pipeline is a job stack.

