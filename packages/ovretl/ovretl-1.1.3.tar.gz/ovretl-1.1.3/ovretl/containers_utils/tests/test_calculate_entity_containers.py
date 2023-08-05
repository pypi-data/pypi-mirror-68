import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal
from ovretl.containers_utils.calculate_entity_containers import (
    calculate_shipments_propositions_containers,
)


def test_calculate_entity_containers():
    containers_df = pd.DataFrame(
        data={
            "container_type": [
                "twenty_standard",
                "twenty_standard",
                "fortyfive_highcube",
                "fortyfive_highcube",
            ],
            "proposition_id": ["0", "1", np.nan, np.nan],
            "shipment_id": [np.nan, np.nan, "2", "3"],
        }
    )
    entity_with_containers = pd.DataFrame(
        data={
            "teus": [1, 1, 2, 2],
            "tc": [1, 1, 1, 1],
            "proposition_id": ["0", "1", np.nan, np.nan],
            "shipment_id": [np.nan, np.nan, "2", "3"],
        }
    )
    containers_df = calculate_shipments_propositions_containers(
        containers_df
    ).reset_index(drop=True)
    assert_frame_equal(
        containers_df, entity_with_containers, check_dtype=False, check_like=True
    )
