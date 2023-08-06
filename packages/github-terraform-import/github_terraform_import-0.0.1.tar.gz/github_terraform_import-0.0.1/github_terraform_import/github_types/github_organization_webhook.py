from dataclasses import dataclass
from typing import List

from .terraform_types import Resource, Block
from .shared import Configuration


@dataclass
class GithubOrganizationWebhook(Resource):
    events: List[str]

    configuration: Configuration

    active: bool = None
    _name: str = "web"

    _id: str = None
