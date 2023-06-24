from pathlib import Path

import uvicorn



if __name__ == "__main__":
    app_dir = str(Path(__file__).parent.parent)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=80,
        workers=1,
        app_dir=app_dir,
        reload=True,
        reload_dirs=app_dir,
        reload_includes=["*.yml"]
    )
