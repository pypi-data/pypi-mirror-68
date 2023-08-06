from dataclasses import dataclass
from typing import List

from .terraform_types import Resource, Block


@dataclass
class GithubRepositoryProject(Resource):
    name: str
    repository: str

    body: str = None
    _id: str = None