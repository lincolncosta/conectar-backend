from fastapi import APIRouter, Request, Depends, Response
import typing as t

from db.session import get_db
from db.area.crud import (
    create_area,
    delete_area,
    edit_area,
    get_area_by_id,
    get_area_by_name,
    get_areas,
    get_area_and_subareas
)
from db.area.schemas import Area, AreaCreate, AreaEdit, AreasAndSubareas
from core.auth import get_current_active_pessoa

area_router = r = APIRouter()


@r.get(
    "/areas",
    response_model=t.List[AreasAndSubareas],
    response_model_exclude_none=True,
)
async def areas_list(
    response: Response,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get all areas
    """
    areas = await get_areas(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(areas)}"
    return areas


@r.get(
    "/areas/id/{area_id}",
    response_model=Area,
    response_model_exclude_none=True,
)
async def area_details_id(
    request: Request,
    area_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any area details by its id
    """
    area = await get_area_by_id(db, area_id)
    return area

@r.get(
    "/areas/name/{area_name}",
    response_model=t.List[Area],
    response_model_exclude_none=True,
)
async def area_details_name(
    request: Request,
    area_name: str,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Get any area details by its name
    """
    area = await get_area_by_name(db, area_name)
    return area


@r.post("/areas", response_model=Area, response_model_exclude_none=True)
async def area_create(
    request: Request,
    area: AreaCreate,
    db=Depends(get_db),
):
    """
    Create a new area
    """
    return await create_area(db, area)


@r.put(
    "/areas/{area_id}",
    response_model=AreaEdit,
    response_model_exclude_none=True,
)
async def area_edit(
    request: Request,
    area_id: int,
    area: AreaEdit,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Update existing area
    """
    return await edit_area(db, area_id, area)


@r.delete(
    "/areas/{area_id}",
    response_model=Area,
    response_model_exclude_none=True,
)

async def area_delete(
    request: Request,
    area_id: int,
    db=Depends(get_db),
    current_pessoa=Depends(get_current_active_pessoa),
):
    """
    Delete an existing area
    """
    return await delete_area(db, area_id)
