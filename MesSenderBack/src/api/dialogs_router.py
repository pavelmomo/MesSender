from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated
from src.api.dependencies import (UOW,
                                  AbstractUOW,
                                  DialogService)

from src.schemas.dialog_schemas import DialogDTO, DialogAddDTO

router = APIRouter(
    prefix="/api/dialogs",
    tags=["Dialogs"]
)  # создание роутера


@router.get("/")  # получение списка диалогов
async def get_user_dialogs(user_id: int, uow: UOW):
    result = await DialogService.get_user_dialogs(uow,user_id)
    return result


@router.post("/")  # добавление диалога
async def add_dialog(dialog: DialogAddDTO, uow: Annotated[AbstractUOW, Depends(UOW)]):
    pass
    # session.add(Dialog(name=dialog.name,is_multiuser=dialog.is_multiuser))
    # res = await session.commit()
    # return {"Success":True}


@router.delete("/{id}")  # удаление диалога
async def delete_dialog(id: int, uow: Annotated[AbstractUOW, Depends(UOW)]):
    pass
    # res = await session.get(Dialog,[id])
    # if res != None:
    #     await session.delete(res)
    #     await session.commit()
    #     res = {"Success":True}
    # else:
    #     res = {"Success":False}
    #
    # return res


