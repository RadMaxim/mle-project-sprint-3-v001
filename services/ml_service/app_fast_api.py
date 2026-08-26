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
    "Sprint3_Histogram",
    "Histogram of predictions",
    # Корзины: 1млн, 3млн, 5млн, 10млн, 15млн, 25млн, 50млн
    buckets=(1_000_000, 3_000_000, 5_000_000, 10_000_000, 15_000_000, 25_000_000, 50_000_000)
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
    prediction_value = pred.get("prediction", 0.0)
    
    # Записываем значение в гистограмму Prometheus
    main_app_predictions.observe(prediction_value)
    
    # Логика для счетчика (если цена больше 0, увеличиваем счетчик)
    if prediction_value > 0:
        main_app_counter_pos.inc()
    
    return pred
