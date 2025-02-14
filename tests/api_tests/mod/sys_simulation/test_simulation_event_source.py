# -*- coding: utf-8 -*-
# 版权所有 2019 深圳米筐科技有限公司（下称“米筐科技”）
#
# 除非遵守当前许可，否则不得使用本软件。
#
#     * 非商业用途（非商业用途指个人出于非商业目的使用本软件，或者高校、研究所等非营利机构出于教育、科研等目的使用本软件）：
#         遵守 Apache License 2.0（下称“Apache 2.0 许可”），
#         您可以在以下位置获得 Apache 2.0 许可的副本：http://www.apache.org/licenses/LICENSE-2.0。
#         除非法律有要求或以书面形式达成协议，否则本软件分发时需保持当前许可“原样”不变，且不得附加任何条件。
#
#     * 商业用途（商业用途指个人出于任何商业目的使用本软件，或者法人或其他组织出于任何目的使用本软件）：
#         未经米筐科技授权，任何个人不得出于任何商业目的使用本软件（包括但不限于向第三方提供、销售、出租、出借、转让本软件、
#         本软件的衍生产品、引用或借鉴了本软件功能或源代码的产品或服务），任何法人或其他组织不得出于任何目的使用本软件，
#         否则米筐科技有权追究相应的知识产权侵权责任。
#         在此前提下，对本软件的使用同样需要遵守 Apache 2.0 许可，Apache 2.0 许可与本许可冲突之处，以本许可为准。
#         详细的授权流程，请联系 public@ricequant.com 获取。


__config__ = {
    "base": {
        "start_date": "2015-04-10",
        "end_date": "2015-04-20",
        "frequency": "1d",
        "accounts": {
            "stock": 1000000,
        }
    },
    "extra": {
        "log_level": "error",
    },
    "mod": {
        "sys_progress": {
            "enabled": True,
            "show": True,
        },
    },
}


def test_open_auction():
    def init(context):
        context.s = "000001.XSHE"
        context.fired = False
        context.open_auction_prices = ()

    def open_auction(context, bar_dict):
        bar = bar_dict[context.s]
        assert (not hasattr(bar, "close"))
        context.open_auction_prices = (bar.open, bar.limit_up, bar.limit_down, bar.prev_close)
        if not context.fired:
            order_shares(context.s, 1000)
            assert get_position(context.s).quantity == 1000
            assert get_position(context.s).avg_price == bar.open
            context.fired = True

    def handle_bar(context, bar_dict):
        bar = bar_dict[context.s]
        assert hasattr(bar, "close")
        assert context.open_auction_prices == (bar.open, bar.limit_up, bar.limit_down, bar.prev_close)

    return locals()


def test_open_auction_1m():
    """ 测试分钟回测下的open_auction """

    try:
        import rqalpha_plus
    except ImportError:
        print("非本地不执行分钟频率测试")
        return {}

    __config__ = {
        "base": {
            "start_date": "2023-03-17",
            "end_date": "2023-03-17",
            "frequency": "1m",
            "accounts": {
                "stock": 100000,
                "future": 1000000,
            }
        },
        "mod": {
            "ricequant_data": {
                "enabled": True,
            }
        }
    }

    def init(context):
        subscribe("AU2306")
        subscribe("000001.XSHE")

    def open_auction(context, bar_dict):
        buy_open("AU2306", 1)
        order_shares("000001.XSHE", 100)
        assert bar_dict["AU2306"].last == 432.58, "期货分钟频率open_auction价格有误"
        assert bar_dict["000001.XSHE"].last == 12.99, "股票分钟频率open_auction价格有误"

    def handle_bar(context, bar_dict):
        pos = get_position("AU2306")
        assert pos.avg_price == 432.58, "期货分钟频率open_auction价格有误"
        pos = get_position("000001.XSHE")
        assert pos.avg_price == 12.99, "股票分钟频率open_auction价格有误"

    return locals()
