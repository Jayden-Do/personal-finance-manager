from unittest.mock import Mock

import pytest
from fastapi import HTTPException, status

from app.db.models.plugin import Plugin
from app.db.models.user_plugin import UserPlugin
from app.services.plugin import PluginService
from app.schemas.plugin import PluginResponse


@pytest.fixture
def plugin_repository():
    return Mock()


@pytest.fixture
def user_plugin_repository():
    return Mock()


@pytest.fixture
def plugin_service(plugin_repository, user_plugin_repository):
    return PluginService(
        plugin_repository=plugin_repository,
        user_plugin_repository=user_plugin_repository,
    )


@pytest.fixture
def expense_plugin():
    return Plugin(
        id=1,
        key="expense",
        name="Expense",
        icon="wallet",
        description="Track expenses",
        color_theme="green",
    )


@pytest.fixture
def saving_plugin():
    return Plugin(
        id=2,
        key="saving",
        name="Saving",
        icon="piggy-bank",
        description="Track savings",
        color_theme="blue",
    )


@pytest.fixture
def investment_plugin():
    return Plugin(
        id=3,
        key="investment",
        name="Investment",
        icon="chart",
        description="Track investments",
        color_theme="purple",
    )


def test_get_plugins_for_user(
    plugin_service,
    plugin_repository,
    expense_plugin,
    saving_plugin,
):
    plugin_repository.get_all_with_user_status.return_value = [
        (expense_plugin, 1),
        (saving_plugin, None),
    ]

    result = plugin_service.get_plugins_for_user(user_id=1)

    assert result == [
        PluginResponse(
            key="expense",
            name="Expense",
            icon="wallet",
            description="Track expenses",
            color_theme="green",
            enabled=True,
        ),
        PluginResponse(
            key="saving",
            name="Saving",
            icon="piggy-bank",
            description="Track savings",
            color_theme="blue",
            enabled=False,
        ),
    ]

    plugin_repository.get_all_with_user_status.assert_called_once_with(1)


def test_update_plugins_for_user_add_plugin(
    plugin_service,
    plugin_repository,
    user_plugin_repository,
    expense_plugin,
    saving_plugin,
):
    plugin_repository.get_by_keys.return_value = [
        expense_plugin,
        saving_plugin,
    ]

    user_plugin_repository.get_by_user.return_value = [
        UserPlugin(
            id=1,
            user_id=1,
            plugin_id=expense_plugin.id,
        )
    ]

    plugin_repository.get_all_with_user_status.return_value = [
        (expense_plugin, 1),
        (saving_plugin, 2),
    ]

    result = plugin_service.update_plugins_for_user(
        user_id=1,
        plugin_keys=["expense", "saving"],
    )

    assert result == [
        PluginResponse(
            key="expense",
            name="Expense",
            icon="wallet",
            description="Track expenses",
            color_theme="green",
            enabled=True,
        ),
        PluginResponse(
            key="saving",
            name="Saving",
            icon="piggy-bank",
            description="Track savings",
            color_theme="blue",
            enabled=True,
        ),
    ]

    user_plugin_repository.create.assert_called_once_with(
        UserPlugin(
            user_id=1,
            plugin_id=saving_plugin.id,
        )
    )

    user_plugin_repository.delete.assert_not_called()


def test_update_plugins_for_user_remove_plugin(
    plugin_service,
    plugin_repository,
    user_plugin_repository,
    expense_plugin,
    saving_plugin,
):
    plugin_repository.get_by_keys.return_value = [
        expense_plugin,
    ]

    user_plugin_repository.get_by_user.return_value = [
        UserPlugin(
            id=1,
            user_id=1,
            plugin_id=expense_plugin.id,
        ),
        UserPlugin(
            id=2,
            user_id=1,
            plugin_id=saving_plugin.id,
        ),
    ]

    plugin_repository.get_all_with_user_status.return_value = [
        (expense_plugin, 1),
        (saving_plugin, None),
    ]

    result = plugin_service.update_plugins_for_user(
        user_id=1,
        plugin_keys=["expense"],
    )

    assert result == [
        PluginResponse(
            key="expense",
            name="Expense",
            icon="wallet",
            description="Track expenses",
            color_theme="green",
            enabled=True,
        ),
        PluginResponse(
            key="saving",
            name="Saving",
            icon="piggy-bank",
            description="Track savings",
            color_theme="blue",
            enabled=False,
        ),
    ]

    user_plugin_repository.create.assert_not_called()

    user_plugin_repository.delete.assert_called_once_with(
        user_id=1,
        plugin_id=saving_plugin.id,
    )


def test_update_plugins_for_user_add_and_remove_plugins(
    plugin_service,
    plugin_repository,
    user_plugin_repository,
    expense_plugin,
    saving_plugin,
    investment_plugin,
):
    plugin_repository.get_by_keys.return_value = [
        expense_plugin,
        investment_plugin,
    ]

    user_plugin_repository.get_by_user.return_value = [
        UserPlugin(
            id=1,
            user_id=1,
            plugin_id=expense_plugin.id,
        ),
        UserPlugin(
            id=2,
            user_id=1,
            plugin_id=saving_plugin.id,
        ),
    ]

    plugin_repository.get_all_with_user_status.return_value = [
        (expense_plugin, 1),
        (saving_plugin, None),
        (investment_plugin, 3),
    ]

    result = plugin_service.update_plugins_for_user(
        user_id=1,
        plugin_keys=["expense", "investment"],
    )

    assert result == [
        PluginResponse(
            key="expense",
            name="Expense",
            icon="wallet",
            description="Track expenses",
            color_theme="green",
            enabled=True,
        ),
        PluginResponse(
            key="saving",
            name="Saving",
            icon="piggy-bank",
            description="Track savings",
            color_theme="blue",
            enabled=False,
        ),
        PluginResponse(
            key="investment",
            name="Investment",
            icon="chart",
            description="Track investments",
            color_theme="purple",
            enabled=True,
        ),
    ]

    user_plugin_repository.create.assert_called_once_with(
        UserPlugin(
            user_id=1,
            plugin_id=investment_plugin.id,
        )
    )

    user_plugin_repository.delete.assert_called_once_with(
        user_id=1,
        plugin_id=saving_plugin.id,
    )


def test_update_plugins_for_user_no_changes(
    plugin_service,
    plugin_repository,
    user_plugin_repository,
    expense_plugin,
    saving_plugin,
):
    plugin_repository.get_by_keys.return_value = [
        expense_plugin,
        saving_plugin,
    ]

    user_plugin_repository.get_by_user.return_value = [
        UserPlugin(
            id=1,
            user_id=1,
            plugin_id=expense_plugin.id,
        ),
        UserPlugin(
            id=2,
            user_id=1,
            plugin_id=saving_plugin.id,
        ),
    ]

    plugin_repository.get_all_with_user_status.return_value = [
        (expense_plugin, 1),
        (saving_plugin, 2),
    ]

    result = plugin_service.update_plugins_for_user(
        user_id=1,
        plugin_keys=["expense", "saving"],
    )

    assert result == [
        PluginResponse(
            key="expense",
            name="Expense",
            icon="wallet",
            description="Track expenses",
            color_theme="green",
            enabled=True,
        ),
        PluginResponse(
            key="saving",
            name="Saving",
            icon="piggy-bank",
            description="Track savings",
            color_theme="blue",
            enabled=True,
        ),
    ]

    user_plugin_repository.create.assert_not_called()
    user_plugin_repository.delete.assert_not_called()


def test_update_plugins_for_user_plugin_not_found(
    plugin_service,
    plugin_repository,
    user_plugin_repository,
):
    plugin_repository.get_by_keys.return_value = []

    with pytest.raises(HTTPException) as exc_info:
        plugin_service.update_plugins_for_user(
            user_id=1,
            plugin_keys=["unknown"],
        )

    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == "One or more plugins not found"

    user_plugin_repository.get_by_user.assert_not_called()
    user_plugin_repository.create.assert_not_called()
    user_plugin_repository.delete.assert_not_called()


def test_update_plugins_for_user_duplicate_keys(
    plugin_service,
    plugin_repository,
    user_plugin_repository,
):
    with pytest.raises(HTTPException) as exc_info:
        plugin_service.update_plugins_for_user(
            user_id=1,
            plugin_keys=["expense", "expense"],
        )

    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "Duplicate plugin keys are not allowed"

    plugin_repository.get_by_keys.assert_not_called()
    user_plugin_repository.get_by_user.assert_not_called()
