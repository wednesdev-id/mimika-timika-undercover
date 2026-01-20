from app.main import app

# Vercel expects a 'handler' or 'app' object.
# Since app.main:app is the FastAPI instance, it will be handled automatically by @vercel/python.
