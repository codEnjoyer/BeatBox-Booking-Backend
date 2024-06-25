import uvicorn

from app.settings import settings

if __name__ == "__main__":
    config = uvicorn.Config(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
        reload_dirs=["app"],
        log_level="info",
    )
    server = uvicorn.Server(config)
    server.run()
