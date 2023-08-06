from dataclasses import dataclass

from .terraform_types import Block


@dataclass
class Configuration(Block):
    url: str
    content_type: str
    insecure_ssl: bool
    secret: str = None
