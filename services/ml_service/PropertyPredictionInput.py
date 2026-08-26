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
