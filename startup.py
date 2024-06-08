import uvicorn

from src.settings import settings

if __name__ == "__main__":
    config = uvicorn.Config(
        "src.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
        reload_dirs=["src"],
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()
