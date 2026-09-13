# 🧪 Space Mission Automation QA Framework

**English** | [Русский](README.ru.md)

FastAPI Testing | Pytest | HTTPX | Asyncio | WebSockets | Locust

CI/CD: [![Space Mission QA Automation Pipeline](https://github.com/Anna1327/space-mission-tests/actions/workflows/main.yml/badge.svg)](https://github.com/Anna1327/space-mission-tests/actions/workflows/main.yml)

A high-performance asynchronous framework for comprehensive automated testing of a spacecraft’s backend (the [**Space Mission Monitoring**](https://github.com/Anna1327/space_mission_monitoring) ecosystem). Designed as a fully autonomous and isolated infrastructure to ensure continuous quality assurance (QA) of a distributed application.

## 📋 Architecture and types of testing

The framework is built on non-blocking I/O, operates within a single session’s event loop, and covers regression testing at all levels of integration:

1. **Async API Testing (`httpx`)**: Parallel testing of REST endpoints, verification of JWT authorisation, access control mechanisms and rate limiter (`slowapi`) request limits.
2. **Asynchronous WebSocket Testing (`websockets`)**: Native testing of reactive subscriptions to system telemetry channels. Real-time validation of asynchronous JSON frames with protection against race conditions.
3. **Database State Validation (`asyncpg`)**: A custom infrastructure context manager, `DBConnector`, for direct low-level access to the PostgreSQL DBMS. It allows you to prepare fixtures and validate the physical state of data on disk, bypassing the ORM layer.
4. **End-to-End (E2E) Scenarios (`allure.step`)**: Linear tracing of end-to-end business processes: *Customer registration ➔ Initialisation of mission sensors ➔ Simulation of a failure ➔ Asynchronous interception of a warning event in WebSocket ➔ Validation of cascading incident logging in the database ➔ Simulation of system auto-recovery*.
5. **Load & Performance Testing (`Locust`)**: Headless scripts simulating concurrent load to verify the degradation of the backend’s asynchronous health check response time as the number of users increases.

## 🛠 Technology stack

- **Core:** Python 3.13, Pytest 8+
- **Asynchronous engines:** Asyncio, AnyIO
- **HTTP transport:** HTTPX
- **WebSocket protocol:** websockets 16.0 (native asynchronous client)
- **Database driver:** asyncpg (direct asynchronous binary connection)
- **Load testing:** Locust (Headless mode)
- **Reporting:** Allure Framework
- **Orchestration and CI/CD:** Docker, Docker Compose, GitHub Actions

## 🚀 Isolated local execution

### Requirements
- Docker / Docker Compose

The test framework is fully containerized, runs in an isolated network environment and interacts with the application’s services within the shared Docker network.

```bash
# 1. Clone the test repository
git clone https://github.com
cd space-mission-tests

# 2. Run tests locally in manual debug mode
pytest -v

# 3. Run the entire test suite in isolation within a Docker container
docker compose up --build --abort-on-container-exit
```

## 📡 CI/CD Pipeline (GitHub Actions)

An automated continuous integration pipeline is set up in the project’s infrastructure:
- **Integration trigger:** Any push or successful merge to the backend repository automatically triggers the regression test suite in that repository.
- **Stable stage:** When the test code itself is updated, syntax validation, linting, and a consistency check of the framework’s fixtures are run.
