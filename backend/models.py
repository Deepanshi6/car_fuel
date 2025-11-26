from sqlalchemy import Column, Integer, String,Date, DateTime,Float, ForeignKey,func
from sqlalchemy.orm import relationship
from backend.database import Base
from datetime import datetime

#Driver table
class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    dob = Column(Date)
    doj = Column(Date)       #date of joining

    #foreign keys
    license_number = Column(String, ForeignKey("driving_license.license_number"), unique=True)        #driver table also has driving license object in it (Composition) which is Foreign key for table
    car_id = Column(String, ForeignKey("cars.car_id"), unique=True, nullable=True)                                   #Driver table also has car object in it (Association) which is Foreign key for table   #you can have extra_1, extra_2 for those not assigned to any car

    #relationships
    dlicense = relationship("DrivingLicense", back_populates="driver", uselist=False)                 #it is one to one relationship so uselist=False
    fuel_logs = relationship("FuelLog", back_populates="driver")
    car = relationship("Car", back_populates="driver", uselist=False)                                 #one to one relationship with Car table

    #functions
    @classmethod
    def add_driver(cls, session, name, gender, dob, doj, license_number, car_id=None):
        driver = cls(name=name, gender=gender, dob=dob, doj=doj,
                     license_number=license_number, car_id=car_id)
        session.add(driver)
        session.commit()
        return driver

    @classmethod
    def remove_driver(cls, session, driver_id):
        driver = session.query(cls).filter_by(id=driver_id).first()
        if driver:
            session.delete(driver)
            session.commit()
        else:
            raise ValueError("Driver not found")

    @classmethod
    def assign_car(cls, session, driver_id, new_car_id):
        driver = session.query(cls).filter_by(id=driver_id).first()
        if driver:
            driver.car_id = new_car_id
            session.commit()
        else:
            raise ValueError("Driver not found")

#Driving License table
class DrivingLicense(Base):
    __tablename__ = "driving_license"

    license_number = Column(String, primary_key=True)                         #string because license number can have alphabets too
    issue_date = Column(Date)
    expiry_date = Column(Date)

    # one to one relationship with Driver table
    driver = relationship("Driver", back_populates="dlicense")


#Car table
class Car(Base):
    __tablename__ = "cars"

    car_id = Column(String, primary_key=True)                    #car_id is number plate here      #string because car id can have alphabets too
    company = Column(String)
    model = Column(String)

    fuel_type_name = Column(String, ForeignKey("fuel_types.fuel_name"))

    # Relationships
    fuel_type_rel = relationship("FuelType")
    fuel_logs = relationship("FuelLog", back_populates="car")
    driver = relationship("Driver", back_populates="car", uselist=False)                             #one to one relationship with Driver table

    #functions
    @classmethod
    def add_car(cls, session, car_id, company, model, fuel_type_name):
        car = cls(car_id=car_id, company=company, model=model,
                  fuel_type_name=fuel_type_name)
        session.add(car)
        session.commit()
        return car

    @classmethod
    def remove_car(cls, session, car_id):
        car = session.query(cls).filter_by(car_id=car_id).first()
        if car:
            session.delete(car)
            session.commit()
        else:
            raise ValueError("Car not found")

    @classmethod
    def change_fuel_type(cls, session, car_id, new_fuel_type):
        car = session.query(cls).filter_by(car_id=car_id).first()
        if not car:
            raise ValueError("Car not found")
        car.fuel_type_name = new_fuel_type
        session.commit()
        return car

class FuelType(Base):
    __tablename__ = "fuel_types"

    fuel_name = Column(String, primary_key=True)
    fuel_price = Column(Float)

    fuel_logs = relationship("FuelLog", back_populates="fuel_type_rel")

    @classmethod
    def update_price(cls, session, fuel_name, new_price):
        fuel = session.query(cls).filter_by(fuel_name=fuel_name).first()
        if not fuel:
            raise ValueError("Fuel type not found")
        fuel.fuel_price = new_price
        session.commit()
        return fuel

#fuel logs
class FuelLog(Base):
    __tablename__ = "fuel_logs"

    log_id = Column(Integer, primary_key=True)
    
    driver_id = Column(Integer, ForeignKey("drivers.id",ondelete="SET NULL"),nullable=True)
    car_id = Column(String, ForeignKey("cars.car_id",ondelete="SET NULL"),nullable=True)
    fuel_type_name = Column(String, ForeignKey("fuel_types.fuel_name"))

    fuel_get = Column(Float)
    total_fuel = Column(Float)
    latest_spent = Column(Float)
    latest_timestamp = Column(DateTime, server_default=func.now(),server_onupdate=func.now())
    petrol_pump_name = Column(String)
    place = Column(String)

    # Relationships
    driver = relationship("Driver", back_populates="fuel_logs", passive_deletes=True)
    car = relationship("Car", back_populates="fuel_logs", passive_deletes=True)
    fuel_type_rel = relationship("FuelType", back_populates="fuel_logs")

    #functions
    @classmethod
    def add_fuel_log(cls, session, driver_id, car_id, fuel_type_name,
                     fuel_get, total_fuel, latest_spent,
                      petrol_pump_name, place):
        log = cls(
            driver_id=driver_id,
            car_id=car_id,
            fuel_type_name=fuel_type_name,
            fuel_get=fuel_get,
            total_fuel=total_fuel,
            latest_spent=latest_spent,
            petrol_pump_name=petrol_pump_name,
            place=place
        )
        session.add(log)
        session.commit()
        return log

    @classmethod
    def remove_fuel_log(cls, session, log_id):
        log = session.query(cls).filter_by(log_id=log_id).first()
        if log:
            session.delete(log)
            session.commit()
        else:
            raise ValueError("Fuel log not found")
        
    @classmethod
    def edit_fuel_log(cls, session, log_id, fuel_get=None, total_fuel=None, latest_spent=None, petrol_pump_name=None, place=None):
        log = session.query(cls).filter_by(log_id=log_id).first()
        if log:
            if fuel_get is not None:
                log.fuel_get = fuel_get
            if total_fuel is not None:
                log.total_fuel = total_fuel
            if latest_spent is not None:
                log.latest_spent = latest_spent
            if petrol_pump_name is not None:
                log.petrol_pump_name = petrol_pump_name
            if place is not None:
                log.place = place
            session.commit()
            return log
        else:
            raise ValueError("Fuel log not found")