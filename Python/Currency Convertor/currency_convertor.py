#!/usr/bin/env python3
import sys
import requests

def convert_currency(from_currency, to_currency, amount):
    API_URL = f"https://hexarate.paikama.co/api/rates/latest/{from_currency}?target={to_currency}"
    response = requests.get(API_URL)
    data = response.json()
    result = amount*(data["data"]["mid"])

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}")

    return result

def main():
    if len(sys.argv) != 4:
        print("Usage: python currency_converter.py <FROM> <TO> <AMOUNT>")
        print("Example: python currency_converter.py USD EUR 100")
        sys.exit(1)

    from_currency = sys.argv[1]
    to_currency = sys.argv[2]
    amount = float(sys.argv[3])

    try:
        result = convert_currency(from_currency, to_currency, amount)
        print(f"{amount:.2f} {from_currency.upper()} = {result:.2f} {to_currency.upper()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
