"""
This module contains data classes used for storing and transforming interface data.
"""
from dataclasses import dataclass, field
from typing import List

# Data class for representing the initial structure of the source data

# pylint: disable=too-many-instance-attributes


@dataclass
class SourceStructure:
    """
    Represents the initial structure of source data.
    """
    code_id: str
    direction: str
    app_type: str
    app_name: str
    format: str
    connection_app: str
    connection_detail: str
    interface_id: str
    interface_url: str

# Data classes for the final nested structure


@dataclass
class Connection:
    """
    Represents a connection between applications.
    """
    app: str
    detail: str


@dataclass
class Interface:
    """
    Represents interface details.
    """
    interface_id: str
    interface_url: str


@dataclass
class App:
    """
    Represents an application with its attributes.
    """
    app_type: str
    app_name: str
    format: str
    connection: Connection
    interface: Interface


@dataclass
class InterfaceStructure:
    """
    Represents the final nested structure of interfaces.
    """
    code_id: str
    direction: str
    apps: List[App] = field(default_factory=list)
