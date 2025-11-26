from backend.database import engine, Base
from backend.models import Driver, DrivingLicense, Car, FuelType, FuelLog

print("Creating tables...")
Base.metadata.create_all(engine)
print("Done!")
