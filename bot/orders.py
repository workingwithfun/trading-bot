import logging

class OrderService:
    def __init__(self, client):
        self.client = client

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            logging.info(f"Placing order: {symbol} {side} {order_type} qty={quantity} price={price}")

            params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity
            }

            if order_type == "LIMIT":
                params["price"] = price
                params["timeInForce"] = "GTC"

            response = self.client.futures_create_order(**params)

            logging.info(f"Order response: {response}")

            return {
                "success": True,
                "data": response
            }

        except Exception as e:
            logging.error(f"Order failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }