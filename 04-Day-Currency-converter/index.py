exchange_rates = {
    "USD" : 1.0,
    "THB" : 35.0,
    "JPY" : 150.0,
    "EUR" : 0.92
}

print("--- Currency Converter ---")
print("Availble Currencies:", ", ".join(exchange_rates.keys()))

while True:
    try:
        # เพิ่มค่าของสกุลเงิน
        update_exchange = input("How many currencies to update (Type '0' for skip): ")

        if update_exchange.isdigit():
            update_count = int(update_exchange)

            if update_count == 0:
                print("Skipping Update...")
            else:
                for x in range(update_count):
                    print(f"\n --- Update # {x+1} ---")
                    key = input("Enter currencies code (e.g., KWR): ").upper()
                    value = float(input(f"Enter rate for {key} (1 USD = ?): "))

                    exchange_rates.update({key : value})
                    print(f"Successfully updated {key}!")
        else:
            print("Invalid input, skipping update section.")


        amount = float(input("\n Enter amount: "))
        from_currency = input("From currency (e.g., USD): ").upper()
        to_currency = input("To currency (e.g., THB):  ").upper()

        if from_currency in exchange_rates and to_currency in exchange_rates:
            # แปลงค่าตั้งต้นเป็น USD
            amount_in_usd = amount / exchange_rates[from_currency]
            # แปลงจาก USD เป็นสกุลที่ต้องการ
            converted_amount = amount_in_usd * exchange_rates[to_currency]

            print(f"\n {amount:,.2f} {from_currency} = {converted_amount:,.2f} {to_currency}")
        else:
            print("Error: Invalid currency code.")

    except ValueError:
        print("Error: Please enter a valid number.")