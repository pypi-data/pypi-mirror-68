from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubMembership(Resource):
    username: str
    role: str
