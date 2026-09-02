from unittest.mock import Mock

from app.db.models.user_plugin import UserPlugin
from app.repositories.user_plugin import UserPluginRepository


def test_create():
    session = Mock()

    user_plugin = UserPlugin(
        id=1,
        user_id=1,
        plugin_id=1,
    )

    repository = UserPluginRepository(session)

    result = repository.create(user_plugin)

    assert result == user_plugin

    session.add.assert_called_once_with(user_plugin)
    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(user_plugin)


def test_delete():
    session = Mock()

    user_plugin = UserPlugin(
        id=1,
        user_id=1,
        plugin_id=1,
    )

    session.exec.return_value.first.return_value = user_plugin

    repository = UserPluginRepository(session)

    repository.delete(
        user_id=1,
        plugin_id=1,
    )

    session.delete.assert_called_once_with(user_plugin)
    session.commit.assert_called_once()


def test_delete_not_found():
    session = Mock()

    session.exec.return_value.first.return_value = None

    repository = UserPluginRepository(session)

    repository.delete(
        user_id=1,
        plugin_id=999,
    )

    session.delete.assert_not_called()
    session.commit.assert_not_called()
