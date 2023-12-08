from typing import Optional

from rqalpha.interface import AbstractFrontendValidator
from rqalpha.utils.logger import user_system_log
from rqalpha.model.order import Order
from rqalpha.portfolio.account import Account


class MarginInstrumentValidator(AbstractFrontendValidator):
    """ 融资下单品种限制: 当开启股票池限制且有融资余额时只能交易股票和ETF """

    def can_cancel_order(self, order, account=None):
        return True

    def can_submit_order(self, order, account=None):
        if account.cash_liabilities <= 0:
            return True
        user_system_log.warn(
            f"Order Creation Failed: cash liabilities > 0, {order.order_book_id} not support submit order"
        )
        return False
