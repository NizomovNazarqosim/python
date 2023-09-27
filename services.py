import database as _database
import email_validator as _email_check
import jwt as _jwt
import fastapi as _fastapi
import models as _models
import passlib.hash as _hash
import sqlalchemy.orm as _orm
import schema as _schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

_JWT_SECRET = "thisisnotverysafe"


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# get user by email
async def get_user_by_email(email:str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

        
# create user
async def create_user(user: _schema.UserBase, db: _orm.Session):
    # check email is valid 
    try:
        valid = _email_check.validate_email(email=user.email)
        email = valid.email
    except _email_check.EmailNotValidError:
        raise _fastapi.HTTPException(status_code=404, detail="Please enter valid email")
    hashed_password = _hash.bcrypt.hash(user.password)
    user_obj = _models.User(email=user.email, name=user.name, password=hashed_password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

# create token
async def create_token(user: _models.User):
    user_obj = _schema.UserBase.from_orm(user)
    user_dict = user_obj.dict()
   
    token = _jwt.encode(user_dict, _JWT_SECRET, algorithm='HS256')
    
    return dict(access_token=token, token_type='bearer')

# verify token
async def verify_token(hashed_password):
    return  _jwt.decode(hashed_password, _JWT_SECRET)



# check password is match
async def password_match(user: _schema.UserLogin, password: str):
    return pwd_context.verify(password, user.password)
    

# verify token
async def verify_token(token):
    return _jwt.decode(token, _JWT_SECRET, algorithms=['HS256'])

# user update by token
async def user_update(user: _schema.UserUpdate, token, db: _orm.Session):
    verifyed_user = await verify_token(token.password)
    user_email = verifyed_user['email']
    
    updated_user = db.query(_models.User).filter(_models.User.email == user_email)
    updated_user.first()
    if user.password:
        hashed_password = _hash.bcrypt.hash(user.password)
    
    if updated_user == None:
        raise HTTException(status_code=status.HTT_NOT_FOUND, detail=f'user with such id: {user_email} does not exist')
    else:
        del user.password
        user.password = hashed_password
        updated_user.update(user.dict(), synchronize_session=False)
        db.commit()

    return updated_user.first()
    
# delete user by token
async def delete_user(token, db: _orm.Session):
    verifyed_token = await verify_token(token.password)
    user_email = verifyed_token['email']
    result =  db.query(_models.User).filter(_models.User.email == user_email).delete()
    db.commit()
    return result