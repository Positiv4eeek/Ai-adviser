
## 🐳 Deployment with Docker

To run the application using Docker, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/Positiv4eeek/Ai-adviser.git
cd ai-adviser
```

### 2. Prepare environment files

Copy the example `.env` files:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Edit the `.env` files according to your setup.

### 3. Create `docker-compose.yml`

If it’s not already present, create a file named `docker-compose.yml` with the following content:

```yaml
version: '3'

services:
  backend:
    image: darkposss/ai-adviser:backend
    container_name: my-backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env

  frontend:
    image: darkposss/ai-adviser:frontend
    container_name: my-frontend
    ports:
      - "80:80"
    env_file:
      - ./frontend/.env
```

> ✅ Ensure that `darkposss/ai-adviser:backend` and `:frontend` exist on [Docker Hub](https://hub.docker.com/repository/docker/darkposss/ai-adviser).

### 4. Run the application

```bash
docker compose up -d
```

This will pull the backend and frontend images and start both services.

### 5. Stop the application

To shut down the containers:

```bash
docker compose down
```