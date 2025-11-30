from datetime import date
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional, Generator

from backend.models import Driver, Car, FuelLog
from backend.database import Session  


from sqlalchemy.orm import Session as DBSession

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# database dependency
def get_db():
   
    db = Session()  # create a  session
    try:
        yield db
    finally:
        db.close()


# schemas for request bodies and responses using Pydantic
class DriverSchema(BaseModel):
    name: str
    gender: str
    dob: date 
    doj: date
    license_number: str
    car_id: Optional[str] = None


class EditDriverSchema(BaseModel):
    id: int
    name: Optional[str] = None
    license_number: Optional[str] = None
    car_id: Optional[str] = None


class CarSchema(BaseModel):
    car_id: str
    company: str
    model: str
    fuel_type_name: str


class EditCarSchema(BaseModel):
    car_id: str
    company: Optional[str] = None
    model: Optional[str] = None
    fuel_type_name: Optional[str] = None


class FuelLogSchema(BaseModel):
    driver_id: int
    car_id: str
    fuel_type_name: str
    fuel_get: float
    total_fuel: float
    latest_spent: float
    petrol_pump_name: str
    place: str


class EditFuelLogSchema(BaseModel):
    log_id: int
    fuel_get: Optional[float] = None
    total_fuel: Optional[float] = None
    latest_spent: Optional[float] = None
    petrol_pump_name: Optional[str] = None
    place: Optional[str] = None


# HTML route handlers for connecting  frontend home pages
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# driver page
@app.get("/driver")
def driver_page(request: Request):
    return templates.TemplateResponse("driver.html", {"request": request})

# car page
@app.get("/car")
def car_page(request: Request):
    return templates.TemplateResponse("car.html", {"request": request})

# fuel log page
@app.get("/fuel")
def fuel_page(request: Request):
    return templates.TemplateResponse("fuel_log.html", {"request": request})

# view logs page
@app.get("/view_logs")
def view_logs_page(request: Request):
    return templates.TemplateResponse("view_logs.html", {"request": request})


# driver CRUD operations
# post is used to create new entries
@app.post("/driver/add")
def add_driver(data: DriverSchema, db: DBSession = Depends(get_db)):
    driver = Driver(
        name=data.name,
        gender=data.gender,
        dob=data.dob,
        doj=data.doj,
        license_number=data.license_number,
        car_id=data.car_id
    )
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return {"message": "Driver Added", "id": driver.id}

# get is used to read entries

@app.get("/driver/get_all")
def get_all_drivers(db: DBSession = Depends(get_db)):
    drivers = db.query(Driver).all()
    return [
        {
            "id": d.id,
            "name": d.name,
            "gender": d.gender,
            "dob": str(d.dob),
            "doj": str(d.doj),
            "license": d.license_number,
            "car_id": d.car_id
        } for d in drivers
    ]

# delete is used to delete entries
@app.delete("/driver/delete/{driver_id}")
def delete_driver(driver_id: int, db: DBSession = Depends(get_db)):
    d = db.query(Driver).filter_by(id=driver_id).first()
    if not d:
        raise HTTPException(404, "Driver not found")
    db.delete(d)
    db.commit()
    return {"message": "Driver Deleted"}

# put is used to update entries
@app.put("/driver/edit")
def edit_driver(data: EditDriverSchema, db: DBSession = Depends(get_db)):
    d = db.query(Driver).filter_by(id=data.id).first()
    if not d:
        raise HTTPException(404, "Driver not found")

    if data.name:
        d.name = data.name
    if data.license_number:
        d.license_number = data.license_number
    if data.car_id is not None:
        d.car_id = data.car_id

    db.commit()
    return {"message": "Driver Updated"}


# car CRUD operations
# post is used to create new entries
@app.post("/car/add")
def add_car(data: CarSchema, db: DBSession = Depends(get_db)):
    car = Car(
        car_id=data.car_id,
        company=data.company,
        model=data.model,
        fuel_type_name=data.fuel_type_name
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return {"message": "Car Added"}


# get is used to read entries
@app.get("/car/get_all")
def get_all_cars(db: DBSession = Depends(get_db)):
    cars = db.query(Car).all()
    return [
        {
            "car_id": c.car_id,
            "company": c.company,
            "model": c.model,
            "fuel_type": c.fuel_type_name
        } for c in cars
    ]

# delete is used to delete entries
@app.delete("/car/delete/{car_id}")
def delete_car(car_id: str, db: DBSession = Depends(get_db)):
    c = db.query(Car).filter_by(car_id=car_id).first()
    if not c:
        raise HTTPException(404, "Car not found")
    db.delete(c)
    db.commit()
    return {"message": "Car Deleted"}

# put is used to update entries
@app.put("/car/edit")
def edit_car(data: EditCarSchema, db: DBSession = Depends(get_db)):
    c = db.query(Car).filter_by(car_id=data.car_id).first()
    if not c:
        raise HTTPException(404, "Car not found")

    if data.company:
        c.company = data.company
    if data.model:
        c.model = data.model
    if data.fuel_type_name:
        c.fuel_type_name = data.fuel_type_name

    db.commit()
    return {"message": "Car Updated"}


# fuel log CRUD operations
@app.post("/fuel/add")
def add_fuel_log(data: FuelLogSchema, db: DBSession = Depends(get_db)):
    log = FuelLog.add_fuel_log(
        session=db,
        driver_id=data.driver_id,
        car_id=data.car_id,
        fuel_type_name=data.fuel_type_name,
        fuel_get=data.fuel_get,
        total_fuel=data.total_fuel,
        latest_spent=data.latest_spent,
        petrol_pump_name=data.petrol_pump_name,
        place=data.place
    )
    # The FuelLog.add_fuel_log commits itself, but we return the created id
    return {"message": "Fuel Log Added", "log_id": log.log_id}


@app.get("/fuel/get_all")
def get_all_fuel_logs(db: DBSession = Depends(get_db)):
    logs = db.query(FuelLog).all()
    return [
        {
            "log_id": f.log_id,
            "driver_id": f.driver_id,
            "car_id": f.car_id,
            "fuel_type": f.fuel_type_name,
            "fuel_get": f.fuel_get,
            "total_fuel": f.total_fuel,
            "spent": f.latest_spent,
            "pump": f.petrol_pump_name,
            "place": f.place
        } for f in logs
    ]


@app.delete("/fuel/delete/{log_id}")
def delete_fuel_log(log_id: int, db: DBSession = Depends(get_db)):
    f = db.query(FuelLog).filter_by(log_id=log_id).first()
    if not f:
        raise HTTPException(404, "Fuel log not found")
    db.delete(f)
    db.commit()
    return {"message": "Fuel Log Deleted"}


@app.put("/fuel/edit")
def edit_fuel_log(data: EditFuelLogSchema, db: DBSession = Depends(get_db)):
    f = db.query(FuelLog).filter_by(log_id=data.log_id).first()
    if not f:
        raise HTTPException(404, "Fuel log not found")

    if data.fuel_get is not None:
        f.fuel_get = data.fuel_get
    if data.total_fuel is not None:
        f.total_fuel = data.total_fuel
    if data.latest_spent is not None:
        f.latest_spent = data.latest_spent
    if data.petrol_pump_name is not None:
        f.petrol_pump_name = data.petrol_pump_name
    if data.place is not None:
        f.place = data.place

    db.commit()
    return {"message": "Fuel Log Updated"}
