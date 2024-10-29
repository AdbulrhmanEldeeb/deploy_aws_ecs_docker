from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import uvicorn 
# Load the pre-trained model and vectorizer
model = joblib.load('ml_models/stacking_model.pkl')
vectorizer = joblib.load('ml_models/count_vectorizer.pkl')
model_version='__0.1.0__'
# Define the prediction function
def predict_class(text: str):
    text_vector = vectorizer.transform([text])
    class_value = model.predict(text_vector)[0]
    probability = model.predict_proba(text_vector)
    class_name = 'ايجابي' if class_value == 1 else 'سلبي'
    return {"class_name": class_name, "probability": round(probability[0][class_value], 2)}

# FastAPI app instance
app = FastAPI()

# Define Pydantic model for the input
class TextInput(BaseModel):
    text: str = Field(..., example="الخدمة جيدة ، شكرا لكم")


@app.get('/')
async def welcome(): 
    return {
        'Health':"ok",
        "model_version":model_version  
            }


# POST endpoint for prediction
@app.post("/predict", response_model=dict)
async def predict(input_data: TextInput):
    try:
        result = predict_class(input_data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__=='__main__': 
    uvicorn.run(app,host='0.0.0.0',port=8080)