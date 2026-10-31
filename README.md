<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/integratech-org/bloca-api">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">BLOCA API</h3>

  <p align="center">
    Cloud REST API Backend for BLOCA System
    <br />
    Data Persistence • User Management • Real-time Updates • Business Logic
    <br />
    <a href="https://github.com/integratech-org/bloca-api"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/integratech-org/bloca-api/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/integratech-org/bloca-api/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#related-projects">Related Projects</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![BLOCA API Banner][product-banner]](https://github.com/integratech-org/bloca-api)

**BLOCA API** is the cloud-based backend service of the BLOCA ecosystem. Built with Django and Django Ninja, it provides a robust REST API for data persistence, user authentication and authorization, real-time communication via WebSockets, and business logic orchestration. The API serves as the central data hub, aggregating batch data from BLOCA Edge, serving predictions from BLOCA ML, and powering the dashboards in BLOCA Admin and BLOCA Mobile.

The API handles user management with role-based permissions, batch lifecycle tracking, feedstock inventory, equipment management, and historical analytics. It uses Django Channels for real-time updates to connected clients and PostgreSQL for reliable data storage.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Django][Django.com]][Django-url]
* [![Python][Python.org]][Python-url]
* [![PostgreSQL][PostgreSQL.org]][PostgreSQL-url]
* [![Redis][Redis.io]][Redis-url]
* [![Nginx][Nginx.com]][Nginx-url]
* [![Docker][Docker.com]][Docker-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This service is designed to run as a containerized application with Docker Compose or can be deployed to cloud platforms.

### Prerequisites

* **Software:**
  - Python 3.14 or higher
  - [uv](https://docs.astral.sh/uv/) package manager
  - PostgreSQL 15 or higher
  - Redis 7 or higher
  - Docker and Docker Compose (recommended)

* **Optional:**
  - Nginx or similar reverse proxy for production deployment

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/integratech-org/bloca-api.git
   cd bloca-api
   ```

2. Run the setup script (installs uv and dependencies)
   ```sh
   make setup
   ```

3. Create environment configuration
   ```sh
   cp .env.example .env
   # Edit .env with your specific configuration:
   # - Database credentials (PostgreSQL)
   # - Redis connection
   # - Django secret key
   # - CORS allowed origins
   # - Email settings
   # - Social authentication credentials (if enabled)
   ```

4. Start the development environment with Docker Compose
   ```sh
   docker compose up -d
   ```

5. Run database migrations
   ```sh
   make migrate
   ```

6. Create a superuser account
   ```sh
   make superuser
   ```

7. Install pre-commit hooks (for development)
   ```sh
   make pre-commit-install
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Start the BLOCA API service:

```sh
# Development server with auto-reload
make dev

# Production server with Gunicorn
make serve
```

The API will be available at:
- **HTTP API**: http://localhost:8000/api/v1/
- **WebSocket**: ws://localhost:8000/ws/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/

### Common Operations

```sh
# Run database migrations
make migrate

# Create database migrations
make makemigrations

# Access Django shell
make shell

# Run tests
make test

# Run linting and formatting
make lint
make format
```

### Development

Run pre-commit checks on all files:
```sh
make pre-commit-all
```

Update pre-commit hooks:
```sh
make pre-commit-update
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- FEATURES -->
## Features

### Core Functionality
- **RESTful API**: Django Ninja-powered REST API with automatic OpenAPI documentation
- **User Authentication**: Django Allauth integration with email/password and social authentication
- **Role-Based Access Control**: Hierarchical permissions for Admin, Operator, and Viewer roles
- **Batch Management**: Complete batch lifecycle tracking from feedstock submission to final quality assessment
- **Feedstock Inventory**: Material management with LDPE and sand stock tracking
- **Equipment Management**: Machine status monitoring and configuration

### Real-Time Communication
- **WebSocket Support**: Django Channels for real-time bidirectional communication
- **Live Telemetry Streaming**: Push process data to connected clients during active batches
- **Event Broadcasting**: System-wide notifications for batch status changes and alerts
- **Channel Layers**: Redis-backed channel layers for scalable WebSocket connections

### Data Management
- **Batch History**: Comprehensive storage of batch data with process parameters and ML predictions
- **Image Storage**: Block inspection images with CDN integration
- **Time-Series Data**: Efficient storage and querying of sensor telemetry
- **Analytics Endpoints**: Aggregated metrics and statistical analysis for reporting

### Integration & Security
- **CORS Configuration**: Configurable cross-origin resource sharing for frontend applications
- **Token Authentication**: Secure API access with JWT tokens
- **Rate Limiting**: Protection against API abuse
- **Database Optimization**: Indexed queries and connection pooling for performance

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- RELATED PROJECTS -->
## Related Projects

BLOCA API is part of the **BLOCA (Batch-Level Optimization through Compaction Analytics)** ecosystem:

* **[bloca-edge](https://github.com/integratech-org/bloca-edge)** - IoT edge hub running on Raspberry Pi for real-time telemetry collection and ML coordination
* **[bloca-ml](https://github.com/integratech-org/bloca-ml)** - Machine learning service for compressive strength prediction and CNN-based surface defect classification
* **[bloca-admin](https://github.com/integratech-org/bloca-admin)** - Web admin dashboard for system oversight and advanced analytics
* **[bloca-mobile](https://github.com/integratech-org/bloca-mobile)** - Mobile application for operators: feedstock submission, batch tracking, and remote machine control
* **[bloca-firmware](https://github.com/integratech-org/bloca-firmware)** - ESP32 firmware for sensor data collection and actuator control
* **[IntegraTech Organization](https://github.com/integratech-org)** - View all BLOCA projects and documentation

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

IntegraTech - [Facebook](https://www.facebook.com/profile.php?id=61592806334500) - integratech1@outlook.com

Project Link: [https://github.com/integratech-org/bloca-api](https://github.com/integratech-org/bloca-api)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/integratech-org/bloca-api.svg?style=for-the-badge
[contributors-url]: https://github.com/integratech-org/bloca-api/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/integratech-org/bloca-api.svg?style=for-the-badge
[forks-url]: https://github.com/integratech-org/bloca-api/network/members
[stars-shield]: https://img.shields.io/github/stars/integratech-org/bloca-api.svg?style=for-the-badge
[stars-url]: https://github.com/integratech-org/bloca-api/stargazers
[issues-shield]: https://img.shields.io/github/issues/integratech-org/bloca-api.svg?style=for-the-badge
[issues-url]: https://github.com/integratech-org/bloca-api/issues
[product-banner]: images/banner.png

<!-- Technology Badges -->
[Django.com]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[PostgreSQL.org]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Redis.io]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
[Nginx.com]: https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white
[Nginx-url]: https://nginx.org/
[Docker.com]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
