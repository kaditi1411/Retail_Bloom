from prophet.serialize import model_to_json, model_from_json
from prophet import Prophet
import pandas as pd

def get_industry_holidays(industry_name="general"):
    # Add domain-specific logic
    if industry_name == "textile":
        holidays = [
            {"holiday": "diwali", "ds": "2024-11-01"},
            {"holiday": "christmas", "ds": "2024-12-25"},
            {"holiday": "eid", "ds": "2024-04-11"},
        ]
    elif industry_name == "electronics":
        holidays = [
            {"holiday": "dussehra", "ds": "2024-10-11"},
            {"holiday": "diwali", "ds": "2024-11-01"},
            {"holiday": "new_year", "ds": "2025-01-01"},
        ]
    else:
        holidays = []

    return pd.DataFrame(holidays)
