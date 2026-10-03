import os

os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["CORS_ORIGINS"] = "http://localhost:5173"
