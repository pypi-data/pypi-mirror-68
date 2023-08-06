from dataclasses import dataclass
from typing import List

from .terraform_types import Resource, Block


@dataclass
class RequiredStatusChecks(Block):
    strict: bool = None
    contexts: List[str] = None


@dataclass
class RequiredPullRequestReviews(Block):
    dismiss_stale_reviews: bool = None
    dismissal_users: List[str] = None
    dismissal_teams: List[str] = None

    require_code_owner_reviews: bool = None
    required_approving_review_count: int = None


@dataclass
class Restrictions(Block):
    users: List[str] = None
    teams: List[str] = None
    apps: List[str] = None


@dataclass
class GithubBranchProtection(Resource):
    repository: str
    branch: str

    enforce_admins: bool = None
    require_signed_commits: bool = None

    required_status_checks: RequiredStatusChecks = None
    required_pull_request_reviews: RequiredPullRequestReviews = None
    restrictions: Restrictions = None
