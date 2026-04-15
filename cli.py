import click
import logging

from bot.client import BinanceClient
from bot.orders import OrderService
from bot.validators import *
from bot.logging_config import setup_logger


setup_logger()

@click.command()
@click.option("--symbol", required=True, help="Trading pair (e.g., BTCUSDT)")
@click.option("--side", required=True, help="BUY or SELL")
@click.option("--type", "order_type", required=True, help="MARKET or LIMIT")
@click.option("--quantity", required=True, type=float)
@click.option("--price", type=float, default=None)
def trade(symbol, side, order_type, quantity, price):
    try:
        # Validation
        validate_side(side)
        validate_order_type(order_type)
        validate_quantity(quantity)
        validate_price(order_type, price)

        # Init client
        client = BinanceClient().get_client()
        order_service = OrderService(client)

        # Print summary
        print("\n--- ORDER REQUEST ---")
        print(f"Symbol: {symbol}")
        print(f"Side: {side}")
        print(f"Type: {order_type}")
        print(f"Quantity: {quantity}")
        print(f"Price: {price}")

        # Place order
        result = order_service.place_order(
            symbol, side, order_type, quantity, price
        )

        if result["success"]:
            data = result["data"]

            print("\n--- ORDER RESPONSE ---")
            print(f"Order ID: {data.get('orderId')}")
            print(f"Status: {data.get('status')}")
            print(f"Executed Qty: {data.get('executedQty')}")
            print(f"Avg Price: {data.get('avgPrice')}")

            print("\n✅ Order placed successfully")

        else:
            print("\n❌ Order failed")
            print(result["error"])

    except Exception as e:
        logging.error(str(e))
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    trade()