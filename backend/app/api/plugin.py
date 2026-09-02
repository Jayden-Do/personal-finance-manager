from fastapi import APIRouter, Depends
from app.db.models.user import User
from app.schemas.plugin import PluginResponse, PluginUpdateRequest
from app.dependencies.auth import get_current_user
from app.services.plugin import PluginService
from app.dependencies.plugin import get_plugin_service


router = APIRouter(
    prefix="/plugins",
    tags=["Plugins"],
)


@router.get(
    "/",
    response_model=list[PluginResponse],
)
def get_plugins(
    current_user: User = Depends(get_current_user),
    service: PluginService = Depends(get_plugin_service),
) -> list[PluginResponse]:
    return service.get_plugins_for_user(current_user.id)


@router.put(
    "/",
    response_model=list[PluginResponse],
)
def update_plugins(
    request: PluginUpdateRequest,
    current_user: User = Depends(get_current_user),
    service: PluginService = Depends(get_plugin_service),
) -> list[PluginResponse]:
    return service.update_plugins_for_user(
        user_id=current_user.id,
        plugin_keys=request.plugin_keys,
    )
