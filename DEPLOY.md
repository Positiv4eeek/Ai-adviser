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

**Example `backend/.env`** (minimum required for deployment):

```env
POSTGRES_USER=aiadviser
POSTGRES_PASSWORD=supersecret
POSTGRES_DB=aiadviserdb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
SECRET_KEY=your_secret_key_here
```

> **Note:**
>
> * If you plan to initialize the database using `dbinit`, ensure `.env` contains correct PostgreSQL credentials.
> * `POSTGRES_HOST` must match the service name in `docker-compose.yml` (here it’s `postgres`).
> * Change `SECRET_KEY` to a secure random value.

### 3. Create `docker-compose.yml`

If it’s not already present, create a file named `docker-compose.yml` with the following content:

```yaml
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

> ✅ Ensure that `darkposss/ai-adviser:backend` and `darkposss/ai-adviser:frontend` exist on [Docker Hub](https://hub.docker.com/repository/docker/darkposss/ai-adviser).

### 4. Run the application

```bash
docker compose up -d
```

This will:

* Pull images from Docker Hub
* Start backend, frontend, and PostgreSQL
* Mount data volume for database persistence

### 5. Initialize the database

Run the following command **once** after the first deployment (or after wiping the DB) to create roles, databases, schemas, and run Alembic migrations:

```bash
docker compose run --rm backend dbinit
```

Expected output (example):

```
[entrypoint] dbinit
Step 1/4: ensure role & db (superuser mode)…
Step 2/4: ensure schema…
Step 3/3: running Alembic migrations…
DB init complete.
```

### 6. Shutdown

To shut down the containers:

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

### 7. Connect to PostgreSQL

```bash
docker exec -it postgres psql -U aiadviser -d aiadviserdb
```

Or use pgAdmin / DBeaver with:

* **Host:** `localhost`
* **Port:** `5432`
* **User:** `aiadviser`
* **Password:** `supersecret`
* **Database:** `aiadviserdb`