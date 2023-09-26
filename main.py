import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from schema import UserBase, UserLogin, UserToken
import services as _services
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm

app = _fastapi.FastAPI()
models.Base.metadata.create_all(bind=engine)    
    
  
      
# create user  
@app.post("/user/create")
async def create_user(user: UserBase, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    if db_user:
        return _fastapi.HTTPException(
            status_code=400,
            detail="User already exist with this email"
        )
    user = await _services.create_user(user=user, db=db)
    return await _services.create_token(user=user)

# login user
@app.post('/user/login')
async def all(user: UserLogin,  db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = await _services.get_user_by_email(email=user.email, db=db)
    if not db_user:
        return _fastapi.HTTPException(
            status_code=400,
            detail="User did not registered yet "
        )
    password_matches = await _services.password_match(user=db_user, password=user.password)
    
    if password_matches:
        return await _services.create_token(user=db_user)
    else:
        raise _fastapi.HTTPException(
            status_code=401, detail="Incorrect password"
        ) 
        
# get current user by passing token
@app.put('/user/update')
async def update_user(user: UserBase,token:UserToken, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    result = await _services.user_update(user=user, token=token, db=db)
    
    return result

# delete user 
@app.delete('/user/delete')
async def delete_user(token:UserToken, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.delete_user(token=token, db=db)