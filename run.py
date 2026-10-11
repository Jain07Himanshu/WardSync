"""WardSync Unified Server Launcher.

Starts the unified backend running on http://127.0.0.1:8000
Connects civic_engine, civic_pipeline, and wardsync-frontend.
"""

import sys
import uvicorn
from pathlib import Path

# Ensure root is on path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if __name__ == "__main__":
    print("=" * 80)
    print("STARTING WARDSYNC UNIFIED PLATFORM")
    print("Connecting: civic_engine + civic_pipeline + wardsync-frontend")
    print("=" * 80)
    print("API Documentation:  http://127.0.0.1:8000/docs")
    print("Public Issues API:  http://127.0.0.1:8000/api/public/issues")
    print("Map Clusters API:   http://127.0.0.1:8000/api/public/map-clusters")
    print("Civic Engine API:   http://127.0.0.1:8000/api/v1")
    print("Frontend Dev App:   http://localhost:5173 (run 'npm run dev' in wardsync-frontend)")
    print("=" * 80 + "\n")

    uvicorn.run(
        "unified_server:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
