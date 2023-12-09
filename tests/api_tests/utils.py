from six import iteritems


def assert_order(order, **kwargs):
    for field, value in iteritems(kwargs):
        assert (
            getattr(order, field) == value
        ), f"order.{field} is wrong, {getattr(order, field)} != {value}"
