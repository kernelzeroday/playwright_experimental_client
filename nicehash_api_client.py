import requests

class NiceHashAPIClient:
    def __init__(self, api_key: str, api_secret: str, organization_id: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.organization_id = organization_id
        self.base_url = "https://api2.nicehash.com"
    