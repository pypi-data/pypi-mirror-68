from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubTeamMembership(Resource):
    _team_name: str
    _team_slug: str
    team_id: str
    username: str

    role: str = None
