"""Entry point for the GetYuhRates web application.

Run this file with: fastapi dev main.py (development) or fastapi run main.py (production)
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
