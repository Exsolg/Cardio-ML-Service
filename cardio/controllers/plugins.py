from fastapi import APIRouter, Depends

from cardio.services.models.plugins import Plugin, PluginsPage, PluginsFilter
from cardio.controllers.utils.responses import OK, NOT_FOUND 

from cardio.services import plugins


plugins_api = APIRouter(
    prefix='/plugins',
    tags=['plugins'],
    responses=OK
)


@plugins_api.get('/')
def get_list(filter: PluginsFilter = Depends(PluginsFilter.get_filter)) -> PluginsPage:
    return plugins.get_list(filter)


@plugins_api.get('/{name}', responses=NOT_FOUND)
def get(name: str) -> Plugin:
    return plugins.get(name)
