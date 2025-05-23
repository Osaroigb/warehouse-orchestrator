# Warehouse Orchestrator

**Table of Contents**

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation & Setup](#installation--setup)
5. [Environment Variables](#environment-variables)
6. [Docker Deployment](#docker-deployment)
7. [Running the App (Non-Docker)](#running-the-app-non-docker)
8. [API Documentation](#api-documentation)
9. [API Endpoints & Usage](#api-endpoints--usage)
10. [Testing](#testing)
11. [Troubleshooting](#troubleshooting)
12. [License](#license)

---

## Project Overview

**Warehouse Orchestrator** is a FastAPI backend system responsible for orchestrating customer orders, managing warehouse availability, assigning robot dispatches, and syncing inventory states. It acts as the intermediary between frontend ordering systems and physical warehouse processes.

---

## Features

* RESTful APIs to **create and manage orders**.
* Rate limiting per client IP.
* Dynamic **warehouse selection** based on operational readiness.
* **Extensible** architecture for future robot dispatch & ERP integrations.
* Robust error handling and structured API responses.
* Modular FastAPI project layout.

---

## Prerequisites

* **Python 3.10+**
* **PostgreSQL 13+**
* Optional:

  * **Docker** and **Docker Compose**
  * **Redis** (for future pub/sub or rate limiting via Redis)

---

## Installation & Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Osaroigb/warehouse-orchestrator.git
   cd warehouse-orchestrator
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure `.env`**:

   ```bash
   cp .env.example .env
   ```

5. **Run database migrations**:

   ```bash
   alembic upgrade head
   ```

6. **Run the app**:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## Environment Variables

`.env.example` contains all required variables:

* `APP_NAME`
* `APP_HOST`
* `APP_PORT`
* `DATABASE_URL` — PostgreSQL connection string
* `REDIS_URL` (optional for async tasks)

You must create a `.env` file in the root directory and populate these accordingly.

---

## Docker Deployment

1. **Build and start services**:

   ```bash
   docker-compose up --build
   ```

2. The app will be available at `http://localhost:8000`.

3. To stop:

   ```bash
   docker-compose down
   ```

---

## Running the App (Non-Docker)

For local development without Docker:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You may also run the app inside an IDE (e.g., VS Code) or set a debug configuration.

---

## API Documentation

Swagger UI is enabled by default at:

```
http://localhost:8000/docs
```

Redoc UI is available at:

```
http://localhost:8000/redoc
```

---

## API Endpoints & Usage

### `POST /orders/`

Creates a new order. Automatically assigns an available warehouse.

Request Body:

```json
{
  "platform": "ubereats",
  "order_ref": "UE-123456",
  "delivery_eta": "2025-05-10T12:00:00Z",
  "items": [
    {"sku": "MILK-1L", "quantity": 2},
    {"sku": "BREAD-WHT", "quantity": 1}
  ]
}
```

Possible Responses:

* `201 Created` – order successfully created
* `400 Bad Request` – duplicate order reference
* `503 Service Unavailable` – no warehouse available
* `422 Unprocessable Entity` – invalid input format

---

## Testing

### ✅ Running Tests

```bash
pytest
```

### Project Test Structure

* `tests/unit/`

  * `test_order_repo.py` — unit tests for repository layer
  * `test_order_service.py` — unit tests for service logic
  * `test_rate_limiter.py` — unit tests for rate limiting
* `tests/integration/`

  * `test_create_order.py` — end-to-end tests for order creation flow

All tests use **pytest**, **pytest-asyncio**, and include full database rollback for isolation.

---

## Troubleshooting

| Problem                                | Solution                                                           |
| -------------------------------------- | ------------------------------------------------------------------ |
| `relation "warehouses" does not exist` | Run `alembic upgrade head`                                         |
| `order_ref already exists`             | Use a random or unique test value                                  |
| Swagger docs not loading               | Confirm app is running and check `/docs` route                     |
| DB connection error                    | Verify `.env` has correct `DATABASE_URL` and PostgreSQL is running |
| Redis connection error                 | Optional: comment out Redis usage if not used                      |

---

## License

This project is licensed under the [MIT License](LICENSE).

---

🚀 **Happy shipping with Warehouse Orchestrator!** For feature requests or issues, please open a [GitHub Issue](https://github.com/your-org/warehouse-orchestrator/issues).
