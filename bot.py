from binance.client import Client
import os
from dotenv import load_dotenv
import time

# Cargar claves desde archivo .env
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

# Usar Binance Testnet
client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

symbol = "BTCUSDT"
check_interval = 10
stop_loss_percent = 0.5

highest_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
stop_price = highest_price * (1 - stop_loss_percent)
holding = True
sold_price = None

print(f"▶️ Precio inicial: {highest_price:.2f} | Stop: {stop_price:.2f}")

while True:
    try:
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])
        print(f"📉 Precio actual: {price:.2f}")

        if holding:
            if price > highest_price:
                highest_price = price
                stop_price = highest_price * (1 - stop_loss_percent)
                print(f"🔼 Nuevo máximo: {highest_price:.2f} | Stop: {stop_price:.2f}")
            elif price <= stop_price:
                print("🚨 Stop activado: vendiendo BTC (simulado)")
                sold_price = price
                holding = False
        else:
            if price >= sold_price:
                print("🛒 Recompra activada: comprando BTC (simulado)")
                highest_price = price
                stop_price = highest_price * (1 - stop_loss_percent)
                holding = True

        time.sleep(check_interval)

    except Exception as e:
        print("❌ Error:", e)
        time.sleep(60)
