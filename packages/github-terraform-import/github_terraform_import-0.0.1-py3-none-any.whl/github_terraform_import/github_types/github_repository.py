from dataclasses import dataclass
from typing import List

from .terraform_types import Resource, Block


@dataclass
class Template(Block):
    owner: str
    repository: str


@dataclass
class GithubRepository(Resource):
    name: str

    description: str = None
    homepage_url: str = None
    private: bool = None

    has_issues: bool = None
    has_projects: bool = None
    has_wiki: bool = None

    is_template: bool = None

    allow_merge_commit: bool = None
    allow_squash_merge: bool = None
    allow_rebase_merge: bool = None

    delete_branch_on_merge: bool = None

    has_downloads: bool = None
    auto_init: bool = None

    gitignore_template: str = None
    license_template: str = None

    default_branch: str = None
    archived: bool = None

    topics: List[str] = None

    template: Template = None
