### Hexlet tests and linter status:

[![Actions Status](https://github.com/VictorVangeli/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/VictorVangeli/python-project-52/actions)

# About

This is the final project within the training program, and the methodology and chosen solutions are determined by the technical requirements.

The service is a simple web application for task tracking, which includes user registration and management, creation and management of task statuses, task tags, and the tasks themselves.

The project is built using the Django web framework, with the frontend implemented using django_bootstrap5, and Caddy is used as the web server.

Demonstration Access: [https://task-manager-52.pupsidian.ru](https://task-manager-52.pupsidian.ru)

# Quick Start:

1. If you don’t have [docker](https://www.docker.com/) installed, please follow installation instructions from docker.com: [Install Docker Engine | Docker Docs](https://docs.docker.com/engine/install/) Additionally, it’s necessary to have familiarity with Docker, docker compose and Docker repositories.

2. Clone the repository:

   • Navigate to the directory where you want to clone the repository;
   • Run the following command:

```bash
>> git clone https://github.com/VictorVangeli/python-project-52 && cd python-project-52
```

3. Make a copy of the .env.example file and rename it to .env.

4. Insert the actual values for the following fields:
```dotenv
	•	SECRET_KEY
	•	USE_POSTGRES
	•	DOMAIN
	•	ROLLBAR_ACCESS_TOKEN (optional)
```

5. [OPTIONAL] If you needed web server:
- Make a copy of the `Caddyfile.example` file and rename it to `Caddyfile`. 
- Replace the actual values for the following fields:
  - DOMAIN;
  - EMAIL;
- To uncomment the `caddy` service in `docker-compose.yml`, you need to remove the # symbols in front of its configuration.

6. Start docker compose
```shell
>> docker compose up -d
```

7. Before using the application, you need to create superuser:
```bash
docker compose exec tm_app uv run python manage.py createsuperuser
```

8. After this manipulation you can go to website which you wrote in field `DOMAIN`
