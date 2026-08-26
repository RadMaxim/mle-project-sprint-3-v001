"""FastAPI-приложение для модели оттока."""

from fastapi import FastAPI
from ml_service.fast_api_handler import FastApiHandler
# Создаём FastAPI-приложение 

from pydantic import BaseModel, Field, ConfigDict

from pydantic import BaseModel, Field, ConfigDict

from pydantic import BaseModel, Field, ConfigDict

class PropertyPredictionInput(BaseModel):
    """Схема входных данных для предсказания стоимости недвижимости с дефолтными значениями."""
    
    floor: int = Field(default=9, description="Этаж квартиры", ge=1)
    kitchen_area: float = Field(default=9.9, description="Площадь кухни в кв.м.", ge=0.0)
    living_area: float = Field(default=19.9, description="Жилая площадь в кв.м.", ge=0.0)
    rooms: int = Field(default=1, description="Количество комнат", ge=0)
    is_apartment: bool = Field(default=False, description="Является ли апартаментами")
    studio: bool = Field(default=False, description="Является ли студией")
    total_area: float = Field(default=35.1, description="Общая площадь в кв.м.", gt=0.0)
    build_year: int = Field(default=1965, description="Год постройки дома", ge=1700, le=2030)
    building_type_int: int = Field(default=6, description="Тип здания (числовой код)")
    latitude: float = Field(default=55.717113, description="Широта", ge=-90.0, le=90.0)
    longitude: float = Field(default=37.78112, description="Долгота", ge=-180.0, le=180.0)
    ceiling_height: float = Field(default=2.64, description="Высота потолков в метрах", ge=2.0, le=6.0)
    flats_count: int = Field(default=84, description="Количество квартир в доме", ge=1)
    floors_total: int = Field(default=12, description="Всего этажей в здании", ge=1)
    has_elevator: bool = Field(default=True, description="Наличие лифта")

    model_config = ConfigDict(from_attributes=True)


class PropertyFullData(PropertyPredictionInput):
    """Полная схема данных, включающая целевую переменную (target)."""
    target: float = Field(..., description="Цена недвижимости (целевая переменная)", ge=0)

app = FastAPI()
# Создаём обработчик запросов для API (модель загружается 1 раз при старте)
app.handler = FastApiHandler()

@app.post("/api/churn/")
def get_prediction_for_item(user_id: int, model_params: PropertyPredictionInput):
    clean_model_params = model_params.model_dump()
    # Формируем словарь в том формате, который ожидает ваш FastApiHandler
    params = {"user_id": user_id, "model_params":clean_model_params}
    
    # Передаем параметры в созданный ранее глобальный обработчик
    return app.handler.handle(params)
