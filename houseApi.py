from fastapi import FastAPI
from pydantic import BaseModel , Field
from typing import Annotated
from fastapi.responses import JSONResponse
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pickle 

#load model
with open("houseprediction.pkl", "rb") as f:
    data = pickle.load(f)
model = data['model']
scale = data['scaler']
encoder = data['encoders']

#validate data
class houseprediction(BaseModel):
    mainroad :Annotated[str , Field(...)]
    parking :Annotated[int , Field(...)]
    area :Annotated[int , Field(...)]
    bedrooms:Annotated[int , Field(...)]
    bathroom :Annotated[int , Field(...)]
    stories :Annotated[int , Field(...)]
    preference_area:Annotated[str , Field(...)]
    aircondition :Annotated[str , Field(...)]
    guestroom :Annotated[str , Field(...)]
    basement:Annotated[str , Field(...)]


app =FastAPI()
@app.post('/prediction')
def house_prediction(data : houseprediction):
    #scale the data (area)
    scaled_are= scale.transform([[data.area]])[0][0]
    #encode
    mainroad_end = encoder['mainroad'].transform([data.mainroad])[0]
    guest_end = encoder['guestroom'].transform([data.guestroom])[0]
    basement_end = encoder['basement'].transform([data.basement])[0]
    aircondition_end = encoder['airconditioning'].transform([data.aircondition])[0]
    prefarea_end = encoder['prefarea'].transform([data.preference_area])[0]

    
    user_data =pd.DataFrame([{
       "mainroad_encoder":mainroad_end,
        "parking":data.parking,
        "area_scaled" : scaled_are,
        "bedrooms" :data.bedrooms,
        "bathrooms" :data.bathroom,
        "stories" : data.stories,
        "prefarea_encoder" :prefarea_end,
        "airconditioning_encoder" :aircondition_end,
        "guestroom_encoder" :guest_end,
        "basement_encoder" :basement_end
    }])
    result = model.predict(user_data)[0]
  
    return JSONResponse(status_code=200 , content={'predict': round(result,2) })


