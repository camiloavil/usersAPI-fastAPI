from sqlmodel import SQLModel

class ResponseModel(SQLModel):
    message  : str
    class Config:
        schema_extra = {
            'example': {
                'message' : 'Response',
            }
        }