import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import pymongo
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel, Field, ValidationError

from .ftCommon import add_one_to_db

router = APIRouter(
    tags=["users"],
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

ERROR_MSG_OBJECT = "User"


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class User(BaseModel):
    username: str = Field(frozen=True)
    email: str | None = None
    full_name: str | None = None


class UserInDB(User):
    hashed_password: str
    permitted_scopes: list[str] = Field(default=["user"])
    disabled: bool | None = None


class UpdatedUser(User):
    new_password: str


class NewUser(User):
    password: str


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="users/token",
    scopes={
        "user": "Read and write user information.",
        "read_animals": "Read information about an animal object.",
        "write_animals": "Write information about an animal object.",
        "read_devices": "Read information about a device object.",
        "write_devices": "Write information about a device object.",
        "read_embryo": "Read information about an embryo object.",
        "write_embryo": "Write information about an embryo object.",
        "read_feed_storage": "Read information about a feed storage object.",
        "write_feed_storage": "Write information about a feed storage object.",
        "read_feed": "Read information about a feed object.",
        "write_feed": "Write information about a feed object.",
        "read_machines": "Read information about a machine object.",
        "write_machines": "Write information about a machine object.",
        "read_medicine": "Read information about a medicine object.",
        "write_medicine": "Write information about a medicine object.",
        "read_points": "Read information about a points object.",
        "write_points": "Write information about a points object.",
        "read_polygons": "Read information about a polygons object.",
        "write_polygons": "Write information about a polygons object.",
        "read_ration": "Read information about a ration object.",
        "write_ration": "Write information about a ration object.",
        "read_semen_straw": "Read information about a semen straw object.",
        "write_semen_straw": "Write information about a semen straw object.",
        "read_samples": "Read information about a samples object.",
        "write_samples": "Write information about a samples object.",
        "read_sensors": "Read information about a sensors object.",
        "write_sensors": "Write information about a sensors object.",
        "read_attachments": "Read information about an attachments object.",
        "write_attachments": "Write information about an attachments object.",
        "read_feeding": "Read information about a feeding event.",
        "write_feeding": "Write information about a feeding event.",
        "read_group": "Read information about a group event.",
        "write_group": "Write information about a group event.",
        "read_health": "Read information about a health event.",
        "write_health": "Write information about a health event.",
        "read_milking": "Read information about a milking event.",
        "write_milking": "Write information about a milking event.",
        "read_movement": "Read information about a movement event.",
        "write_movement": "Write information about a movement event.",
        "read_observations": "Read information about an observations event.",
        "write_observations": "Write information about an observations event.",
        "read_performance": "Read information about a performance event.",
        "write_performance": "Write information about a performance event.",
        "read_reproduction": "Read information about a reproduction event.",
        "write_reproduction": "Write information about a reproduction event.",
        "read_attention": "Read information about an attention event.",
        "write_attention": "Write information about an attention event.",
        "read_withdrawal": "Read information about a withdrawal event.",
        "write_withdrawal": "Write information about a withdrawal event.",
        "read_measurements": "Read information about sensor objects and sample events.",
        "write_measurements": "Write information about sensor objects and sample events.",
    },
)

password_hash = PasswordHash.recommended()

load_dotenv()
SECRET_KEY = os.getenv("FT_SECRET_KEY")
ALGORITHM = os.getenv("FT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("FT_ACCESS_TOKEN_EXPIRE_MINUTES"))


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


async def get_user(db, username: str):
    user = await db.find_one({"username": username})
    return UserInDB(**user)


async def authenticate_user(db, username: str, password: str):
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    request: Request,
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        scope: str = payload.get("scope", "")
        token_scopes = scope.split(" ")
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = await get_user(request.app.state.users, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/register", response_description="Register user", response_model=User)
async def register_user(request: Request, new_user: NewUser):
    db = request.app.state.users
    user = UserInDB(
        hashed_password=get_password_hash(new_user.password),
        disabled=True,
        **new_user.model_dump(),
    )
    try:
        _ = await db.insert_one(user.model_dump(by_alias=True))
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=404, detail="User already exists")
    return new_user.model_dump(exclude=["password"])


@router.patch(
    "/update",
    response_description="Update your own user information",
    response_model=User,
)
async def update_user_information(
    request: Request,
    updated_user: UpdatedUser,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    db = request.app.state.users
    user = UserInDB(
        hashed_password=get_password_hash(updated_user.new_password),
        **updated_user.model_dump(),
    )
    await db.update_one(
        {"username": current_user.username},
        {"$set": user.model_dump(by_alias=True)},
        upsert=False,
    )
    return updated_user.model_dump(exclude=["new_password"])


@router.delete(
    "/remove", response_description="Delete your own user account", response_model=User
)
async def delete_user(
    request: Request,
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    db = request.app.state.users
    await db.delete_one({"username": current_user.username})
    return current_user


@router.get(
    "/me",
    response_description="Retrieve your own user information",
    response_model=User,
)
async def get_user_details(
    current_user: Annotated[User, Security(get_current_active_user, scopes=["user"])],
):
    return current_user


@router.post("/token", response_description="Retrieve JWT token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], request: Request
) -> Token:
    user = await authenticate_user(
        request.app.state.users, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    masked_scopes = mask_scopes(user.permitted_scopes, form_data.scopes)
    if len(masked_scopes) > 0:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "scope": " ".join(masked_scopes)},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type="bearer")
    else:
        raise HTTPException(status_code=400, detail="No valid scopes found")


def mask_scopes(permitted, requested):
    scopes = []
    for scope in requested:
        if (
            scope in permitted
        ):  # Returns a list of requested AND allowed scopes, ignoring others
            scopes.append(scope)
    return scopes
