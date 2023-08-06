from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubOrganizationBlock(Resource):
    username: str
