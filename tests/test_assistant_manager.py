import pytest
from openai_manager import AssistantManager
from unittest.mock import Mock



def test_init_with_valid_parameters():
    mock_client = Mock()
    # Mock any necessary methods or attributes of the client
    manager = AssistantManager(client=mock_client, assistant_id="valid_id")
    assert manager is not None
    assert manager.assistant is not None


def test_init_with_invalid_parameters():
    with pytest.raises(TypeError):
        AssistantManager()

    with pytest.raises(ValueError):
        AssistantManager(client=None)

    with pytest.raises(ValueError):
        AssistantManager(client=None, assistant_id=None, assistant_params=None)

    mock_client = Mock()

    with pytest.raises(ValueError):
        AssistantManager(client=mock_client, assistant_id=None, assistant_params=None)

