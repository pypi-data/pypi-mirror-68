from dataclasses import dataclass

from .terraform_types import Resource, Block


@dataclass
class GithubActionsSecret(Resource):
    repository: str
    secret_name: str
    plaintext_value: str
