import sys
import uvicorn


if __name__ == "__main__":
    #sys.path.append(".")  # добавление пути проекта в path ( для VSCode)
    uvicorn.run(app="server:app", reload=True)  # запуск веб-сервера uvicorn
