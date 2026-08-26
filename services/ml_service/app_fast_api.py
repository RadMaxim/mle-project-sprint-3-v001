from fastapi import FastAPI
from ml_service.fast_api_handler import FastApiHandler
from ml_service.PropertyPredictionInput import PropertyPredictionInput
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Histogram
from prometheus_client import Counter

app = FastAPI()
# инициализируем и запускаем экпортёр метрик
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app)

main_app_predictions = Histogram(
    # имя метрики
    "Sprint3_Histogram",
    #описание метрики
    "Histogram of predictions",
    #указаываем корзины для гистограммы
    buckets=(1, 2, 4, 5,10, 20)
)

main_app_counter_pos = Counter("Sprint3_Counter", "Count of positive predictions")

# Создаём обработчик запросов для API (модель загружается 1 раз при старте)
app.handler = FastApiHandler()

@app.post("/api/churn/")
def get_prediction_for_item(user_id: int, model_params: PropertyPredictionInput):
    clean_model_params = model_params.model_dump()
    # Формируем словарь в том формате, который ожидает ваш FastApiHandler
    params = {"user_id": user_id, "model_params":clean_model_params}
    pred = app.handler.handle(params)
    main_app_predictions.observe(pred)
    if pred > 0:
        main_app_counter_pos.inc()
    # Передаем параметры в созданный ранее глобальный обработчик
    return pred
