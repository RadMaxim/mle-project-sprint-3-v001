
from catboost import CatBoostClassifier
# импортируйте необходимую библиотеку
# ваш код здесь

def load_churn_model(model_path: str):
    """Загружаем обученную модель оттока.
    Args:
        model_path (str): Путь до модели.
    """
    model = CatBoostClassifier()
    try:
        model.load_model(model_path)
        print("Model loaded successfully")
    except Exception as e:
        print(f"Failed to load model: {e}")
    return model

if __name__ == "__main__":
    model = load_churn_model(model_path='catboost_churn_model.bin')
    print(f'Model parameter names: {model.feature_names_}')
    # вызовите функцию load_churn_model с нужным путём
    # ваш код здесь  
    # выведите параметры модели через print(f"Model parameter names: {}") 
    # ваш код здесь 