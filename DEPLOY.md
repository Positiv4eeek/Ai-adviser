
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
version: '3.8'

services:
  backend:
    image: darkposss/ai-adviser:backend
    container_name: my-backend
    ports:
      - "8000:8000"
    env_file:
      - ./backend/.env
    depends_on:
      - postgres

  frontend:
    image: darkposss/ai-adviser:frontend
    container_name: my-frontend
    ports:
      - "80:80"
    env_file:
      - ./frontend/.env

  postgres:
    image: postgres:15
    container_name: postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: aiadviser
      POSTGRES_PASSWORD: supersecret
      POSTGRES_DB: aiadviserdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

> ✅ Ensure that `darkposss/ai-adviser:backend` and `:frontend` exist on [Docker Hub](https://hub.docker.com/repository/docker/darkposss/ai-adviser).

### 4. Run the application

```bash
docker compose up -d
```

This will:

* Pull images from Docker Hub
* Start backend, frontend, and PostgreSQL
* Mount data volume for database persistence

### 5. Shutdown

To shut down the containers:

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

### 6. Connect to PostgreSQL

```bash
docker exec -it postgres psql -U aiadviser -d aiadviserdb
```

Or use pgAdmin / DBeaver with:

* **Host:** `localhost`
* **Port:** `5432`
* **User:** `aiadviser`
* **Password:** `supersecret`
* **Database:** `aiadviserdb`