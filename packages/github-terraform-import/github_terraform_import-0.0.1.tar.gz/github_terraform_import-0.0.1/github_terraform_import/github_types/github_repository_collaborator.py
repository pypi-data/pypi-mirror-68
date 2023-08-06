from dataclasses import dataclass
from typing import List

from .terraform_types import Resource, Block


@dataclass
class GithubRepositoryCollaborator(Resource):
    repository: str
    username: str

    permission: str = None
