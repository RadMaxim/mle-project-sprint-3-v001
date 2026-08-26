from catboost import CatBoostRegressor
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import (
    PolynomialFeatures,

)
import joblib

BASE_DIR = Path(__file__).resolve().parent.parent
class FastApiHandler:

    def __init__(self):
        self.poly_path = BASE_DIR / "models" / "poly_transformer.pkl"
        print(self.poly_path)
        self.poly = joblib.load(str(self.poly_path))
        print(self.poly)

        self.param_types = {
            "user_id": str,
            "prediction": dict
        }
        self.model_path = BASE_DIR / "models" / "final_model.cbm"
        self.load_churn_model(model_path=self.model_path)
        
        self.required_model_params = [
                'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Type', 'PaperlessBilling', 'PaymentMethod', 
                'MonthlyCharges', 'TotalCharges', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'days', 'services'
            ]

    def load_churn_model(self, model_path: str):
       
        try:
            self.model = CatBoostRegressor()
            self.model.load_model(model_path)
        except Exception as e:
            print(f"Failed to load model: {e}")

      
        
    def check_required_query_params(self, query_params: dict) -> bool:
        if "user_id" not in query_params or "model_params" not in query_params:
            return False

        if not isinstance(query_params["user_id"], self.param_types["user_id"]):
            return False

        if not isinstance(query_params["model_params"], self.param_types["model_params"]):
            return False

        return True
    def check_required_model_params(self, model_params: dict) -> bool:
       
        if set(model_params.keys()) == set(self.required_model_params):
            return True
        return False
    def validate_params(self, params: dict) -> bool:
    
        if self.check_required_query_params(params):
            print("All query params exist")
        else:
            print("Not all query params exist")
            return False
    
        if self.check_required_model_params(params["model_params"]):
            print("All model params exist")
        else:
            print("Not all model params exist")
            return False
        return True
        
    def handle(self, params):
        response = {}

        try:
            # if not self.validate_params(params):
            #     return {"Error": "Problem with parameters"}

            model_params = params["model_params"]
            user_id = params["user_id"]
            X = pd.DataFrame([model_params])
            print(X)
            X_generated = self.poly.transform(X)
            print("erg")
            self.required_model_index_column = [
                    95,
                    90,
                    9,
                    7,
                    64,
                    55,
                    29,
                    124,
                    120,
                    115,
                    114,
                    113,
                    106,
                    101,
                    0
            ]
            X_selected = X_generated[
                :,
                self.required_model_index_column
            ]
            print(X_selected)
            y_pred = float(
                        self.model.predict(X_selected)
                    )

            print(y_pred)
            response = {"user_id": user_id, "prediction":y_pred}

        except Exception:
            return {"Error": "Problem with request"}

        else:
            return response
    