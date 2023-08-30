"""
Utility functions for Excel operations.
"""

from openpyxl import Workbook
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.worksheet import Worksheet

from src.main.logging_utils import debug_logging


@debug_logging
def create_excel_table(workbook: Workbook, sheet_name: str = 'Sheet1') -> None:
    """
    Creates an Excel table in the given worksheet.

    Parameters:
        workbook (Workbook): The Excel workbook object.
        sheet_name (str, optional): The name of the sheet where the table will be 
        created. Defaults to 'Sheet1'.

    Returns:
        None
    """
    worksheet: Worksheet = workbook[sheet_name]

    # Define a table and add it to the worksheet
    table = Table(displayName="Table1", ref=worksheet.dimensions)

    # Add a default style to the table
    style = TableStyleInfo(
        name="TableStyleMedium9",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False
    )
    table.tableStyleInfo = style

    worksheet.add_table(table)
