from dataclasses import dataclass
from typing import List

from .terraform_types import Resource, Block


@dataclass
class GithubRepositoryDeployKey(Resource):
    key: str
    read_only: str
    repository: str
    title: str

    _id: str
