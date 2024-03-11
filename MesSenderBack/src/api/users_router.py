from fastapi import APIRouter, Request, Body
from src.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
session_factory : AsyncSession

router = APIRouter(
    prefix="/api/users",
    tags=["Users"]
)  # создание роутера


