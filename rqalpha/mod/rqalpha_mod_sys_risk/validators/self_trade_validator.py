# -*- coding: utf-8 -*-
# 版权所有 2019 深圳米筐科技有限公司（下称“米筐科技”）
#
# 除非遵守当前许可，否则不得使用本软件。
#
#     * 非商业用途（非商业用途指个人出于非商业目的使用本软件，或者高校、研究所等非营利机构出于教育、科研等目的使用本软件）：
#         遵守 Apache License 2.0（下称“Apache 2.0 许可”），您可以在以下位置获得 Apache 2.0 许可的副本：http://www.apache.org/licenses/LICENSE-2.0。
#         除非法律有要求或以书面形式达成协议，否则本软件分发时需保持当前许可“原样”不变，且不得附加任何条件。
#
#     * 商业用途（商业用途指个人出于任何商业目的使用本软件，或者法人或其他组织出于任何目的使用本软件）：
#         未经米筐科技授权，任何个人不得出于任何商业目的使用本软件（包括但不限于向第三方提供、销售、出租、出借、转让本软件、本软件的衍生产品、引用或借鉴了本软件功能或源代码的产品或服务），任何法人或其他组织不得出于任何目的使用本软件，否则米筐科技有权追究相应的知识产权侵权责任。
#         在此前提下，对本软件的使用同样需要遵守 Apache 2.0 许可，Apache 2.0 许可与本许可冲突之处，以本许可为准。
#         详细的授权流程，请联系 public@ricequant.com 获取。


from rqalpha.interface import AbstractFrontendValidator
from rqalpha.const import ORDER_TYPE, SIDE, POSITION_EFFECT
from rqalpha.utils.i18n import gettext as _
from rqalpha.utils.logger import user_system_log


class SelfTradeValidator(AbstractFrontendValidator):
    def __init__(self, env):
        self._env = env

    def can_submit_order(self, order, account=None):
        open_orders = [o for o in self._env.get_open_orders(order.order_book_id) if (
                o.side != order.side and o.position_effect != POSITION_EFFECT.EXERCISE
        )]
        if not open_orders:
            return True
        reason = _("Create order failed, there are active orders leading to the risk of self-trade: [{}...]")
        if order.type == ORDER_TYPE.MARKET:
            user_system_log.warn(reason.format(open_orders[0]))
            return False
        if order.side == SIDE.BUY:
            for open_order in open_orders:
                if order.price >= open_order.price:
                    user_system_log.warn(reason.format(open_order))
                    return False
        else:
            for open_order in open_orders:
                if order.price <= open_order.price:
                    user_system_log.warn(reason.format(open_order))
                    return False

    def can_cancel_order(self, order, account=None):
        return True
