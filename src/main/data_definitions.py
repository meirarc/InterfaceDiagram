""" This module contains data classes used for storing and transforming interface data. """
from dataclasses import dataclass, field
from typing import List


@dataclass
class SourceStructure:  # pylint: disable=too-many-instance-attributes
    """ Represents the initial structure of source data. """
    code_id: str
    direction: str
    app_type: str
    app_name: str
    format: str
    connection_app: str
    connection_detail: str
    interface_id: str
    interface_url: str


@dataclass
class Connection:
    """ Represents a connection between applications. """
    app: str
    detail: str


@dataclass
class Interface:
    """ Represents interface details. """
    interface_id: str
    interface_url: str


@dataclass
class App:
    """ Represents an application with its attributes. """
    app_type: str
    app_name: str
    format: str
    connection: Connection
    interface: Interface


@dataclass
class InterfaceStructure:
    """ Represents the final nested structure of interfaces. """
    code_id: str
    direction: str
    apps: List[App] = field(default_factory=list)


@dataclass
class SizeParameters:
    """ Represents the Size parameters used on the interface diagram class """
    y_protocol: float
    y_protocol_start: float
    app_height: float
    page_width: float


@dataclass
class ProtocolConfig:
    """Protocol Configuration to diagram class"""
    app_name: str
    direction: str
    row: int
    app_format: str
    position: float


@dataclass
class ConnectionConfig:
    """Connection Config for Diagram class"""
    source: str
    target: str
    row: int
    direction: str


@dataclass
class DetailConfig:
    """Detail config for the Diagram Class"""
    source: str
    target: str
    row: int
    text: str


@dataclass
class LinkConfig:
    source: str
    target: str
    row: int
    text: str
    url: str
