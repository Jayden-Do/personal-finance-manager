from unittest.mock import Mock

from app.db.models.plugin import Plugin
from app.repositories.plugin import PluginRepository


def test_get_all():
    session = Mock()
    plugins = [
        Plugin(
            id=1,
            key="expense",
            name="Expense",
            icon="wallet",
            description="Track expenses",
            color_theme="green",
        ),
        Plugin(
            id=2,
            key="saving",
            name="Saving",
            icon="piggy-bank",
            description="Track savings",
            color_theme="blue",
        ),
    ]

    session.exec.return_value.all.return_value = plugins

    repository = PluginRepository(session)

    result = repository.get_all()

    assert result == plugins
    session.exec.assert_called_once()


def test_get_by_id_success():
    session = Mock()
    plugin = Plugin(
        id=1,
        key="expense",
        name="Expense",
        icon="wallet",
        description="Track expenses",
        color_theme="green",
    )

    session.exec.return_value.first.return_value = plugin

    repository = PluginRepository(session)

    result = repository.get_by_id(1)

    assert result == plugin
    session.exec.assert_called_once()


def test_get_by_id_not_found():
    session = Mock()

    session.exec.return_value.first.return_value = None

    repository = PluginRepository(session)

    result = repository.get_by_id(999)

    assert result is None
    session.exec.assert_called_once()


def test_get_by_keys_success():
    session = Mock()

    plugins = [
        Plugin(
            id=1,
            key="expense",
            name="Expense",
            icon="wallet",
            description="Track expenses",
            color_theme="green",
        ),
        Plugin(
            id=2,
            key="saving",
            name="Saving",
            icon="piggy-bank",
            description="Track savings",
            color_theme="blue",
        ),
    ]

    session.exec.return_value.all.return_value = plugins

    repository = PluginRepository(session)

    result = repository.get_by_keys(["expense", "saving"])

    assert result == plugins
    session.exec.assert_called_once()


def test_get_by_keys_not_found():
    session = Mock()

    session.exec.return_value.all.return_value = []

    repository = PluginRepository(session)

    result = repository.get_by_keys(["unknown"])

    assert result == []
    session.exec.assert_called_once()


def test_get_all_with_user_status():
    session = Mock()

    expense = Plugin(
        id=1,
        key="expense",
        name="Expense",
        icon="wallet",
        description="Track expenses",
        color_theme="green",
    )

    saving = Plugin(
        id=2,
        key="saving",
        name="Saving",
        icon="piggy-bank",
        description="Track savings",
        color_theme="blue",
    )

    investment = Plugin(
        id=3,
        key="investment",
        name="Investment",
        icon="chart",
        description="Track investments",
        color_theme="purple",
    )

    results = [
        (expense, 1),
        (saving, None),
        (investment, None),
    ]

    session.exec.return_value.all.return_value = results

    repository = PluginRepository(session)

    result = repository.get_all_with_user_status(1)

    assert result == results

    assert result[0][0] == expense
    assert result[0][1] == 1

    assert result[1][0] == saving
    assert result[1][1] is None

    assert result[2][0] == investment
    assert result[2][1] is None

    session.exec.assert_called_once()
