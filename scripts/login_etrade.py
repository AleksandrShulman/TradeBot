import logging

from common.exchange.etrade.etrade_connector import ETradeConnector

logger = logging.getLogger(__name__)

# API Guide
# https://apisb.etrade.com/docs/api/order/api-order-v1.html#/definition/orderPreview

if __name__ == "__main__":
    symbol = "GE"

    connector = ETradeConnector()
    session, base_url = connector.load_connection()

    url = base_url + "/v1/market/quote/" + symbol + ".json"

    # Make API call for GET request
    response = session.get(url)
    logger.debug("Request Header: %s", response.equity_request.headers)
    print("Hi")