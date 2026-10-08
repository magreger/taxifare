
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the TaxiFare API!"}

@app.get("/predict")
def predict(
    pickup_datetime: str,
    pickup_longitude: float,
    pickup_latitude: float,
    dropoff_longitude: float,
    dropoff_latitude: float,
    passenger_count: int
):
    fare = float(passenger_count * 2.5)
    return {"fare": fare}
