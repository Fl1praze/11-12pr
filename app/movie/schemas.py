from pydantic import BaseModel



class MovieSchemas(BaseModel):
    title: str

    class Config:
        from_attributes = True