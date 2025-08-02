from pydantic import BaseModel, Field
from typing import Annotated, Literal

class UserInput(BaseModel):
    
    age : Annotated[int, Field(..., title='Age', description='Age of individual', gt=0, lt=130)]
    gender : Annotated[Literal['male', 'female'], Field(..., title='Gender', description='Gender of individual')]
    weight_kg : Annotated[float, Field(..., title='Weight', description='Weight of individual (in Kgs)', gt=0)]
    diet : Annotated[Literal['healthy', 'unhealthy'], Field(..., title='Diet', description='Diet that you take', examples=['healthy', 'unhealthy'])]
    sleep_hours : Annotated[float, Field(..., title='Sleep Hours', description='How many hours do you sleep?', gt=0)]
    water_intake_liters : Annotated[float, Field(..., title='Water Intake', description='Water Intake (in liters)')]
    smoking_or_vaping : Annotated[Literal['yes', 'no'], Field(..., title='Smoke or Vape', description='Do you smoke or vape?', examples=['yes', 'no'])]

