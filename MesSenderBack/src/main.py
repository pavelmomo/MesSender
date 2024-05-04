import uvicorn
from utils.logging import LOGGING_CONFIG

if __name__ == "__main__":
    # запуск веб-сервера uvicorn
    uvicorn.run(app="server:app", reload=False, host="0.0.0.0",log_config=LOGGING_CONFIG)
