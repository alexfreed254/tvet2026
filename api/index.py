# Vercel serverless function entry point
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), '..', 'backend')
sys.path.insert(0, backend_path)

from mangum import Mangum
from app.main import app

# Wrap FastAPI app with Mangum for serverless
handler = Mangum(app, lifespan="off")
