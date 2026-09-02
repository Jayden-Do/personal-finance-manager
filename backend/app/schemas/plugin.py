from pydantic import BaseModel


class PluginResponse(BaseModel):
    key: str
    name: str
    icon: str
    description: str
    color_theme: str
    enabled: bool


class PluginUpdateRequest(BaseModel):
    plugin_keys: list[str]
