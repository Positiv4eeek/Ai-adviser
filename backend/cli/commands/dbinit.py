from cleo.commands.command import Command
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

class DbInitCommand(Command):
    name = "dbinit"
    description = "Initializes DB: optionally creates role/db/schema and runs migrations"

    def handle(self):
        cfg = get_db_config()
        parts = cfg.parts()
        app_user = parts["user"]
        app_pass = parts["password"]
        app_db   = parts["db"]

        super_url = cfg.postgres_super_url()

        if super_url:
            
            self.line("<info>Step 1/4: ensure role & db (superuser mode)…</info>")
            pg_engine = create_engine(super_url, poolclass=NullPool, future=True)

            
            with pg_engine.connect() as conn, conn.begin():
                conn.execute(
                    text("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = :role) THEN
                            EXECUTE format('CREATE ROLE %I LOGIN PASSWORD %L', :role, :pwd);
                        END IF;
                    END$$;
                    """),
                    {"role": app_user, "pwd": app_pass},
                )

            
            with pg_engine.connect() as conn:
                conn.execute(text("COMMIT"))
                exists = conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :db"),
                    {"db": app_db},
                ).first()
                if not exists:
                    conn.execute(
                        text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = :db"),
                        {"db": app_db},
                    )
                    conn.execute(text(f"CREATE DATABASE {app_db} OWNER {app_user}"))

            pg_engine.dispose()

            
            self.line("<info>Step 2/4: ensure schema…</info>")
            app_engine = create_engine(cfg.app_url(), poolclass=NullPool, future=True)
            with app_engine.connect() as conn, conn.begin():
                conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))
                
            app_engine.dispose()
        else:
            
            self.line("<comment>No POSTGRES_SUPERUSER_URL provided → skipping role/db/schema creation.</comment>")

        
        self.line("<info>Step 3/3: running Alembic migrations…</info>")
        import subprocess, os
        subprocess.run(["alembic", "upgrade", "head"], check=True, cwd=os.getcwd())

        self.line("<info>DB init complete.</info>")


def get_db_config():
    from db.config import DBConfig
    return DBConfig()
