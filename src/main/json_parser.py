"""
This module provides functionalities to parse JSON data.
"""
from typing import List

from src.main.data_definitions import (
    SourceStructure, Connection, Interface,
    App, InterfaceStructure
)

from src.main.logging_utils import debug_logging

# pylint: disable=too-few-public-methods


class JSONParser:
    """
    A class to parse JSON data.
    """

    @staticmethod
    @debug_logging
    def json_to_object(data: List[SourceStructure]) -> List[InterfaceStructure]:
        """
        Transform JSON to a formatted object.

        :param data: List of dictionaries representing the JSON data.
        :return: List of dictionaries representing the transformed data.
        """
        transformed_data = []

        for initial in data:
            # Create nested objects
            connection = Connection(
                app=initial.connection_app, detail=initial.connection_detail)

            interface = Interface(interface_id=initial.interface_id,
                                  interface_url=initial.interface_url)
            app = App(
                app_type=initial.app_type,
                app_name=initial.app_name,
                format=initial.format,
                connection=connection,
                interface=interface
            )

            # Create FinalData object
            final_data = InterfaceStructure(
                code_id=initial.code_id, direction=initial.direction, apps=[app])
            transformed_data.append(final_data)

        return transformed_data
