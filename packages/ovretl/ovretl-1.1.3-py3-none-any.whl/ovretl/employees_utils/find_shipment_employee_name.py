import pandas as pd


def find_shipment_employee_name(employees_associated_df: pd.DataFrame, role: str):
    if len(employees_associated_df) == 0:
        return None
    mask_employees = employees_associated_df["role"] == role
    employees_associated_df_filtered = employees_associated_df[
        mask_employees
    ].reset_index(drop=True)
    if len(employees_associated_df_filtered) > 0:
        return employees_associated_df_filtered.loc[0, "name"]
    return None


def add_employees_to_shipment(
    shipment: pd.Series, employees_shipment_with_name_df: pd.DataFrame
):
    mask_shipment = (
        employees_shipment_with_name_df["shipment_id"] == shipment["shipment_id"]
    )
    shipment["sales"] = find_shipment_employee_name(
        employees_associated_df=employees_shipment_with_name_df[mask_shipment],
        role="sales_owner",
    )
    shipment["operations"] = find_shipment_employee_name(
        employees_associated_df=employees_shipment_with_name_df[mask_shipment],
        role="operations_owner",
    )
    return shipment
