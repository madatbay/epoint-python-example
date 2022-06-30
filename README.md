# Epoint Python Example

Ready-to-use python example for [epoint](https://epoint.az/) payment gateway that can be used in any types of python
projects.

## How to use?

### 1. Get the project files
I don't have leisure time to create python package to make it much more simple. But as example itself is simple enough, we can tolerate for now 🤯
Just clone to repository 
```shell
git clone https://github.com/madatbay/epoint-python-example.git
```

### 2. Install requirements

```shell
python3 -m venv venv
pip3 install -r requirements.txt
```

### 3. Create environment variables
Create `.env` file to save your variables
```shell
touch .env
```
Include Epoint **private and public** keys into your `.env` file. As this example is very simple, perhaps, you'll have
different project structure. So, make sure you environment variables are accessible from `epoint.py`. You can get your keys from [Epoint dashboard](https://epoint.az/en/profile/api)

| Key                | Value                       |
|--------------------|-----------------------------|
| EPOINT_PUBLIC_KEY  | i000000001                  |
| EPOINT_PRIVATE_KEY | xxxxxxxxxxxxxxxxxxxxxxxxxxx |

> These are just sample values. You need to use your own keys

### 4. Make payments
All are ready to start making you payments via Epoint payment processor.
```python
from epoint import epoint

class Invoice:
    def __init__(self):
        self.id = 1
        self.amount = 10

invoice = Invoice()

data = epoint.save_card()
print(f"New payment method {data['card_id']} created 💳")

data = epoint.save_card_and_pay(invoice)
print(f"Payment made and payment method {data['card_id']} saved 💳")

data = epoint.pay_with_saved_card(invoice)
print(f"Payment made with saved card 💳")
```

### Contributions:
Example is not perfectly written, yet working so far. Feel free to make any contributions
