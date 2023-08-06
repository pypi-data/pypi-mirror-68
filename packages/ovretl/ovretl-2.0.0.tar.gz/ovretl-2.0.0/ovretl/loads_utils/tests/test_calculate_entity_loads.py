import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal
from ovretl.loads_utils.calculate_entity_loads import calculate_shipments_propositions_loads


def test_calculate_entity_loads():
    loads_df = pd.DataFrame(
        data={
            "unit_weight": [10, 100, 10, 10],
            "unit_length": [120, 120, 120, 120],
            "unit_height": [100, 100, 100, 100],
            "unit_width": [80, 80, 80, 80],
            "unit_number": [1, 1, 1, 1],
            "total_weight": [200, np.nan, 200, 200],
            "total_volume": [0.9, 0.9, 1, np.nan],
            "proposition_id": ["0", "1", np.nan, np.nan],
            "shipment_id": [np.nan, np.nan, "2", "3"],
        }
    )
    entity_with_loads = pd.DataFrame(
        data={
            "total_weight": [200, 100, 200, 200],
            "total_volume": [0.9, 0.9, 1, 0.96],
            "proposition_id": ["0", "1", np.nan, np.nan],
            "shipment_id": [np.nan, np.nan, "2", "3"],
            "taxable_weight": [200, 150, 200, 200],
            "weight_measurable": [1, 1, 1, 1],
        }
    )
    loads_df = calculate_shipments_propositions_loads(loads_df).reset_index(drop=True)
    assert_frame_equal(loads_df, entity_with_loads, check_dtype=False, check_like=True)
