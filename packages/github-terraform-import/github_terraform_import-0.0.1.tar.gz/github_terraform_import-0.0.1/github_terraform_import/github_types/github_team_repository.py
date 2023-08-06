from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubTeamRepository(Resource):
    _team_name: str
    _team_slug: str
    team_id: str
    repository: str

    permission: str = None
