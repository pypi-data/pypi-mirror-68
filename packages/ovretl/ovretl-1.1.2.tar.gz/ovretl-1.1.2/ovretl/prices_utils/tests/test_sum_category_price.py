import pandas as pd
from ovretl.prices_utils.sum_category_price import sum_category_price


def sum_category_prices():
    df = pd.DataFrame(
        data={
            "category": [
                "departure_truck_freight",
                "arrival_truck_freight",
                "departure_fees",
                "freight",
                "arrival_fees",
            ],
            "price_in_eur": [1336.05, 680, 108.59, 3651, 95],
            "margin_price_in_eur": [0, 20, 32.49, 534.42, 0],
            "vat_price_in_eur": [0, 10, 0, 20, 0],
        },
    )
    assert sum_category_price(df, "price_in_eur") == sum([1336.05, 680, 108.59, 3651, 95])
    assert sum_category_price(df, "vat_price_in_eur") == sum([0, 10, 0, 20, 0])
    assert sum_category_price(df, "margin_price_in_eur", "departure_fees") == 32.49
