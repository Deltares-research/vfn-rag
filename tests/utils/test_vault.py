import os
from unittest.mock import patch, MagicMock
import pytest

from vfn_rag.utils import vault


class DummySecret:
    def __init__(self, value):
        self.value = value


def test_get_secret_success():
    # Arrange: mock SecretClient to return a secret with .value
    mock_client = MagicMock()
    mock_client.get_secret.return_value = DummySecret("super-secret-value")

    with patch("vfn_rag.utils.vault.DefaultAzureCredential") as mock_cred, \
         patch("vfn_rag.utils.vault.SecretClient") as mock_secret_client:
        mock_cred.return_value = MagicMock()
        mock_secret_client.return_value = mock_client

        v = vault.Vault("https://example.vault")

        # Act
        val = v.get_secret("SOME_SECRET")

        # Assert
        assert val == "super-secret-value"
        mock_client.get_secret.assert_called_once_with("SOME_SECRET")


def test_get_secret_fallback_to_env():
    # Arrange: SecretClient raises ResourceNotFoundError, env var present
    mock_client = MagicMock()
    from azure.core.exceptions import ResourceNotFoundError

    mock_client.get_secret.side_effect = ResourceNotFoundError("not found")

    with patch("vfn_rag.utils.vault.DefaultAzureCredential") as mock_cred, \
         patch("vfn_rag.utils.vault.SecretClient") as mock_secret_client:
        mock_cred.return_value = MagicMock()
        mock_secret_client.return_value = mock_client

        os.environ["MY_ENV_SECRET"] = "env-secret-value"

        v = vault.Vault("https://example.vault")

        # Act
        val = v.get_secret("MY_ENV_SECRET")

        # Assert
        assert val == "env-secret-value"
        mock_client.get_secret.assert_called_once_with("MY_ENV_SECRET")

        # Cleanup
        del os.environ["MY_ENV_SECRET"]


def test_get_secret_missing_raises():
    # Arrange: SecretClient raises ResourceNotFoundError, env var absent
    mock_client = MagicMock()
    from azure.core.exceptions import ResourceNotFoundError

    mock_client.get_secret.side_effect = ResourceNotFoundError("not found")

    with patch("vfn_rag.utils.vault.DefaultAzureCredential") as mock_cred, \
         patch("vfn_rag.utils.vault.SecretClient") as mock_secret_client:
        mock_cred.return_value = MagicMock()
        mock_secret_client.return_value = mock_client

        v = vault.Vault("https://example.vault")

        # Act / Assert
        with pytest.raises(ValueError):
            v.get_secret("NON_EXISTENT_SECRET")


def test_init_raises_when_client_fails():
    # Simulate SecretClient raising during initialization
    with patch("vfn_rag.utils.vault.DefaultAzureCredential") as mock_cred, \
         patch("vfn_rag.utils.vault.SecretClient") as mock_secret_client:
        mock_cred.return_value = MagicMock()
        mock_secret_client.side_effect = Exception("init failed")

        with pytest.raises(Exception):
            vault.Vault("https://example.vault")
