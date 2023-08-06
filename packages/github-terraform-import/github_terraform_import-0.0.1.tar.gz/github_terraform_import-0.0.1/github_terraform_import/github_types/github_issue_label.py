from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubIssueLabel(Resource):
    repository: str
    name: str
    color: str

    description: str = None
    _url: str = None
