from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class Vault:
    def __init__(self, vault_url: str):
        self.vault_url = vault_url
        self.credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)

    def get_secret(self, secret_name: str):
        secret = self.client.get_secret(secret_name)
        return secret.value
