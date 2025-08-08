## 🐳 Deployment with Docker

To run the application using Docker, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/Positiv4eeek/Ai-adviser.git
cd ai-adviser
```

### 2. Prepare environment files

Copy the example `.env` file:

```bash
cp backend/.env.example backend/.env
```

Then open `backend/.env` and set the required values:

```env
OPENAI_API_KEY=your-openai-key-here
smtp_user=your@email.com
smtp_password=your-email-password
smtp_host=smtp.example.com
smtp_port=465
secret_key=<super-secret-key>

DATABASE_URL=postgresql+psycopg2://aiadviser:supersecret@postgres:5432/aiadviserdb
POSTGRES_SUPERUSER_URL=postgresql+psycopg2://aiadviser:supersecret@postgres:5432/postgres

POSTGRES_USER=aiadviser
POSTGRES_PASSWORD=supersecret
POSTGRES_DB=aiadviserdb
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

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

> ✅ Ensure that `darkposss/ai-adviser:backend` and `darkposss/ai-adviser:frontend` images exist on [Docker Hub](https://hub.docker.com/repository/docker/darkposss/ai-adviser).

### 4. Initialize the database

Run Alembic migrations in the backend container:

```bash
docker compose run --rm backend dbinit
```

You should see `DB init complete.` in the output if migrations succeed.

### 5. Run the application

```bash
docker compose up -d
```

This will:

* Pull images from Docker Hub
* Start backend, frontend, and PostgreSQL
* Mount data volume for database persistence

### 6. Shutdown

To stop containers:

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