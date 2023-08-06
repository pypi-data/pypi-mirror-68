from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubOrganizationProject(Resource):
    name: str
    body: str = None
    _id: str = None
