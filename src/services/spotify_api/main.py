from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from src.platforms.spotify.spotify_bot_assign_space import SpotifyBotAssignSpace

app = FastAPI(title="Subsy Bot Endpoints", version="1.0.0")


class SuscriptionRequest(BaseModel):
    email: str
    password: str
    has_paid: bool


class SuscriptionResponse(BaseModel):
    invitation_link: str
    admin_adress: str

"""
@app.post("/new_account", status_code=status.HTTP_201_CREATED)
async def create_account(user_data: SuscriptionRequest):
    try:

        success = True 
        if not success:
            raise Exception("No se pudo crear la cuenta")

        return JSONResponse(
            status_code=201,
            content={"message": "Cuenta creada exitosamente"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""


@app.post("/add_user", response_model=SuscriptionResponse, status_code=status.HTTP_201_CREATED)
async def add_user(user_data: SuscriptionRequest):
    try:
        #Usando la logica de automatizacion 
        bot = SpotifyBotAssignSpace()
        invitation_link, admin_adress = bot.SpotifyBotAssignSpace.assign_space(
            user_data.email,
            user_data.password,
            user_data.has_paid
        )

        return SuscriptionResponse(
            invitation_link=invitation_link,
            admin_adress=admin_adress,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al asignar espacio: {str(e)}")

"""
@app.post("/remove_user", status_code=status.HTTP_200_OK)
async def remove_user(user_data: SuscriptionRequest):
    try:

        removed = True  
        if not removed:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        return {"message": "Usuario eliminado correctamente"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
"""


