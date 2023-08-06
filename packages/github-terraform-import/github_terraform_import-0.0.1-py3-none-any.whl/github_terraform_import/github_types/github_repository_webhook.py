from dataclasses import dataclass
from typing import List

from .terraform_types import Resource, Block
from .shared import Configuration


@dataclass
class GithubRepositoryWebhook(Resource):
    repository: str
    events: List[str]

    configuration: Configuration

    active: bool = None
    _name: str = "web"

    _id: str = None
