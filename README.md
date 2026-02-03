# Centralized Data Architecture Example (FastAPI + Docker) - Company Data Only

This project demonstrates a simplified **centralized data architecture** using FastAPI, Python, and Docker, focusing exclusively on **company data**. In this model, a single application/team is responsible for the entire data lifecycle: ingestion, transformation, storage (mocked), governance, and serving company data via a unified API.

## Project Structure

```
.
├── main.py             # Entry point for the FastAPI application
├── schemas.py          # Pydantic models for data structures (Company only)
├── data_sources.py     # Data ingestion and transformation logic (for Company data)
├── data_sources/       # Directory containing raw, disparate company data files
│   ├── __init__.py
│   ├── data_source_a.py
│   ├── data_source_b.py
│   └── data_source_c.py
├── repositories.py     # Data access logic (CRUD operations on unified Company data)
├── routes.py           # API endpoints (FastAPI APIRouter - Company only)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration for building the image
└── README.md           # Project documentation and instructions
```

## Centralized Data Architecture Overview

In this example:
*   Raw company data is provided by three disparate sources (`data_source_a.py`, `data_source_b.py`, `data_source_c.py`) within the `data_sources/` directory.
*   The `data_sources.py` file acts as the ingestion and transformation layer. It reads data from these raw sources, normalizes varying field names, converts data types (e.g., "1M" to `1_000_000.0`), and unifies the data into a single `Company` Pydantic schema.
*   The `repositories.py` layer then interacts with this unified data, providing a clean interface for the API endpoints.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   [Docker](https://www.docker.com/get-started) installed on your system.
*   For local development, [uv](https://github.com/astral-sh/uv) is recommended for fast dependency management. You can install it via `curl -LsSf https://astral.sh/uv/install.sh | sh` or `pip install uv`.

### Build and Run with Docker

1.  **Navigate to the project directory**:
    Make sure you are in the `centralised_data_arc` directory, which contains the `Dockerfile`.

    ```bash
    cd centralised_data_arc
    ```

2.  **Build the Docker image**:
    This command will build a Docker image named `centralized-data-app` based on the `Dockerfile` in the current directory.

    ```bash
    docker build -t centralized-data-app .
    ```

3.  **Run the Docker container**:
    This command will start a Docker container from the `centralized-data-app` image, mapping port 8000 on your host to port 8000 in the container.

    ```bash
    docker run -p 8000:8000 centralized-data-app
    ```

    The application should now be running and accessible at `http://localhost:8000`.

### Local Development with uv

1.  **Navigate to the project directory**:
    ```bash
    cd centralised_data_arc
    ```

2.  **Create and activate a virtual environment with uv**:
    ```bash
    uv venv
    source .venv/bin/activate
    ```

3.  **Install dependencies with uv**:
    ```bash
    uv pip install -r requirements.txt
    ```

4.  **Run the FastAPI application locally**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

    The application should now be running and accessible at `http://localhost:8000`.

### Accessing the API

Once the Docker container or local application is running, you can access the FastAPI application and its API endpoints.

*   **API Documentation (Swagger UI)**: Open your web browser and go to `http://localhost:8000/docs`. Here you will find an interactive documentation of all available API endpoints.
*   **API Documentation (ReDoc)**: Alternatively, you can view the ReDoc documentation at `http://localhost:8000/redoc`.

#### Example API Endpoints:

You can use `curl` or any API client (like Postman or Insomnia) to test the endpoints.

**Get all companies:**
```bash
curl http://localhost:8000/api/companies
```

**Get a specific company by ID:**
```bash
curl http://localhost:8000/api/companies/alphacorp-us # Example using an identifier from data_source_c
```

Feel free to explore the other endpoints listed in the `/docs` or `/redoc` interfaces.