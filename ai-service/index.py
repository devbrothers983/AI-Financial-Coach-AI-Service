# Vercel's Python runtime looks for a recognized entrypoint filename
# (index.py, app.py, main.py, etc.) and loads a top-level `app` variable
# from it. Putting this shim at the project root — rather than relying on
# Vercel finding app/main.py directly — guarantees the working directory is
# the project root when it runs, so `app.schemas`/`app.services` (absolute
# imports used throughout the FastAPI app) resolve exactly like they do
# locally under `uvicorn app.main:app`.
from app.main import app
