from myapp.db.database import Base, engine

import myapp.models.user
import myapp.models.food_entry
import myapp.models.goal
import myapp.models.meal_plan

Base.metadata.create_all(bind=engine)
print(" Tables created successfully.")
