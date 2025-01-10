# Games Service

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) 
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A backend microservice developed with **FastAPI** that serves and manages daily puzzles for users.

---

## Features
- Provides daily puzzles for users.
- Efficient and scalable backend architecture.
- Built with FastAPI for high performance and modern API capabilities.

---

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running Locally](#running-locally)
- [Contributing](#contributing)
- [License](#license)

---

## Getting Started

Follow these instructions to set up and run the `games-service` microservice locally.

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ob-kavici/games-service.git
   cd games-service
   ```

2. **(Optional) Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. Navigate to the `/app` directory:
   ```bash
   cd app
   ```

2. Copy and rename the `.env.template` file to `.env`:
   ```bash
   cp .env.template .env
   ```

3. Edit the `.env` file to include your environment variables (e.g., database connection strings, API keys, etc.).

4. Start the application using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

5. The service will be accessible at `http://127.0.0.1:8000`.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your commit message"
   ```
4. Push the branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to reach out if you encounter any issues or have suggestions for improvement!
