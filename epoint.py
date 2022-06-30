from abc import ABC, abstractmethod
import binascii
import base64
from dotenv import load_dotenv
from hashlib import sha1
import requests
import os
import json

load_dotenv()  # take environment variables from .env.

# Include your epoint public and private keys into .env file
EPOINT_PUBLIC_KEY = os.environ.get("EPOINT_PUBLIC_KEY")
EPOINT_PRIVATE_KEY = os.environ.get("EPOINT_PRIVATE_KEY")


class PaymentProcessor(ABC):
    @abstractmethod
    def save_card(self):
        pass

    @abstractmethod
    def pay_with_saved_card(self, card_uid, invoice, amount):
        pass

    @abstractmethod
    def save_card_and_pay(self, invoice, amount):
        pass


class EpointPaymentProcessor(PaymentProcessor):
    EPOINT_BASE_URL = "https://epoint.az/api/1/"

    def __init__(self):
        self.public_key = EPOINT_PUBLIC_KEY
        self.private_key = EPOINT_PRIVATE_KEY

    def _send_request(self, url_suffix, data, signature):
        url = self.EPOINT_BASE_URL + url_suffix
        res = requests.post(url, {"data": data, "signature": signature})
        return res

    def format_data_signature(self, json_obj: dict) -> tuple[str, str]:
        json_string = json.dumps(json_obj)
        data = base64.b64encode(json_string.encode())

        sgn_string = self.private_key + data.decode() + self.private_key
        signature = binascii.b2a_base64(sha1(sgn_string.encode()).digest()).decode()

        return data.decode(), signature

    def save_card(self):
        data, signature = self.format_data_signature({
            "public_key": self.public_key,
            "language": "en",
        })

        return self._send_request("card-registration", data, signature)

    def pay_with_saved_card(self, card_uid, invoice, amount):
        data, signature = self.format_data_signature({
            "public_key": self.public_key,
            "language": "en",
            "card_uid": card_uid,
            "order_id": invoice.id,
            "amount": invoice.amount,
            "currency": "AZN"
        })
        return self._send_request("execute-pay", data, signature)

    def save_card_and_pay(self, invoice, amount):
        data, signature = self.format_data_signature({
            "public_key": self.public_key,
            "language": "en",
            "order_id": invoice.id,
            "amount": invoice.amount,
            "currency": "AZN",
            "description": invoice.id  # endpoint requires but optional in docs
        })

        return self._send_request("card-registration-with-pay", data, signature)


class PaymentGateway:
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor

    def save_card(self):
        return self.processor.save_card()

    def pay_with_saved_card(self, card_uid, invoice, amount):
        return self.processor.pay_with_saved_card(card_uid, invoice, amount)

    def save_card_and_pay(self, invoice, amount):
        return self.processor.save_card_and_pay(invoice, amount)


epoint_processor = EpointPaymentProcessor()
epoint = PaymentGateway(epoint_processor)
