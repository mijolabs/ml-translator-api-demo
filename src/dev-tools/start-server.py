from pathlib import Path

import uvicorn



if __name__ == "__main__":
    app_dir = str(Path(__file__).parent.parent)

    uvicorn.run(
        "app.main:app",
        app_dir=app_dir,
        host="0.0.0.0",
        port=8000,
        reload=True,
        workers=1
    )
