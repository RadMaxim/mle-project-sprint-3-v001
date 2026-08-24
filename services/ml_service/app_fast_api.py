"""FastAPI-приложение для модели оттока."""

from fastapi import FastAPI
from fast_api_handler import FastApiHandler

# Создаём FastAPI-приложение 
app = FastAPI()

# Создаём обработчик запросов для API (модель загружается 1 раз при старте)
app.handler = FastApiHandler()

@app.post("/api/churn/")
def get_prediction_for_item(user_id: int, model_params: dict):
    
    # Формируем словарь в том формате, который ожидает ваш FastApiHandler
    params = {"user_id": user_id, "model_params":model_params}
    
    # Передаем параметры в созданный ранее глобальный обработчик
    return app.handler.handle(params)
