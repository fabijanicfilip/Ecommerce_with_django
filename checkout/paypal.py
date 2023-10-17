import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AXY31oZW5CQr9jEKJs6T1ESFe51QZvhZf8SJnlbWa5QbNNCUvq4ETIbOqZqGX3knYdVViGO1xbjm6Npp"
        self.client_secret = "ENvvXVatyI7WfyXH7-CtckWZgA_XvSbwyg_qTtEeJiW8weWDD6hAttDG0-yAPJc0x_f9JHkG_gSZnfEn"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)