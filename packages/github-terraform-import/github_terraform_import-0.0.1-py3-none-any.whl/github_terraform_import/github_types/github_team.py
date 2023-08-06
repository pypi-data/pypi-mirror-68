from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubTeam(Resource):
    name: str

    description: str = None
    privacy: str = None

    parent_team_id: str = None
    ldap_dn: str = None

    _team_id: str = None
    _team_slug: str = None
