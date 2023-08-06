from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubProjectColumn(Resource):
    project_id: str
    name: str
