from .github_actions_secret import GithubActionsSecret
from .github_branch_protection import GithubBranchProtection
from .github_issue_label import GithubIssueLabel
from .github_membership import GithubMembership
from .github_organization_block import GithubOrganizationBlock
from .github_organization_project import GithubOrganizationProject
from .github_organization_webhook import GithubOrganizationWebhook
from .github_project_column import GithubProjectColumn
from .github_repository_collaborator import GithubRepositoryCollaborator
from .github_repository_deploy_key import GithubRepositoryDeployKey
from .github_repository_project import GithubRepositoryProject
from .github_repository_webhook import GithubRepositoryWebhook
from .github_repository import GithubRepository, Template
from .github_team_membership import GithubTeamMembership
from .github_team_repository import GithubTeamRepository
from .github_team import GithubTeam

from .shared import Configuration
from .terraform_types import Resource, Block


__all__ = [
    "github_actions_secret",
    "github_branch_protection",
    "github_issue_label",
    "github_membership",
    "github_organization_block",
    "github_organization_project",
    "github_organization_webhook",
    "github_project_column",
    "github_repository",
    "github_repository_collaborator",
    "github_repository_deploy_key",
    "github_repository_project",
    "github_repository_webhook",
    "github_team",
    "github_team_membership",
    "github_team_repository",
]

RESOURCES = [
    GithubActionsSecret,
    GithubBranchProtection,
    GithubIssueLabel,
    GithubMembership,
    GithubOrganizationBlock,
    GithubOrganizationProject,
    GithubOrganizationWebhook,
    GithubProjectColumn,
    GithubRepository,
    GithubRepositoryCollaborator,
    GithubRepositoryDeployKey,
    GithubRepositoryProject,
    GithubRepositoryWebhook,
    GithubTeam,
    GithubTeamMembership,
    GithubTeamRepository,
]
