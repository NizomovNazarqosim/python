from pydantic import BaseModel

class UserBase(BaseModel):
    name:str
    email:str
    password:str
    
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email:str
    password:str
    
    class Config:
        from_attributes = True
        
class UserToken(BaseModel):
    password:str
    
    class Config:
        from_attributes = True
    
class UserUpdate(BaseModel):
    name:str or None
    email:str or None
    password:str or None
    
    class Config:
        from_attributes = True