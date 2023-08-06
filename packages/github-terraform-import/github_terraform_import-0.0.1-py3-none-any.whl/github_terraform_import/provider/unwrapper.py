from ..github_types import Configuration, Template

from ..github_types import (
    GithubActionsSecret,
    GithubRepository,
    GithubRepositoryWebhook,
    GithubBranchProtection,
    GithubIssueLabel,
    GithubMembership,
    GithubOrganizationBlock,
    GithubOrganizationProject,
    GithubOrganizationWebhook,
    GithubProjectColumn,
    GithubRepositoryProject,
    GithubRepositoryCollaborator,
    GithubRepositoryDeployKey,
    GithubTeam,
    GithubTeamMembership,
    GithubTeamRepository,
)
from ..github_types.github_branch_protection import (
    RequiredStatusChecks,
    RequiredPullRequestReviews,
    Restrictions,
)


def max_permissions(permissions):
    for level in ("admin", "push", "pull"):
        if permissions[level]:
            return level


class PacketUnwrapper:
    @staticmethod
    def visit_github_actions_secret(repository, secret):
        return GithubActionsSecret(
            repository=repository["name"],
            secret_name=secret["name"],
            plaintext_value="WARNING: Secrets cannot be imported via Github API",
        )

    @staticmethod
    def visit_github_repository(repository):
        repo = GithubRepository(
            name=repository["name"],
            description=repository["description"],
            homepage_url=repository["homepage"],
            private=repository["private"],
            has_issues=repository["has_issues"],
            has_projects=repository["has_projects"],
            has_wiki=repository["has_wiki"],
            is_template=repository.get("is_template"),
            allow_merge_commit=repository["allow_merge_commit"],
            allow_squash_merge=repository["allow_squash_merge"],
            allow_rebase_merge=repository["allow_rebase_merge"],
            delete_branch_on_merge=repository["delete_branch_on_merge"],
            has_downloads=repository["has_downloads"],
            # TODO: auto_init missing from API
            # TODO: gitignore_template missing from API
            # TODO: license_template missing from API
            default_branch=repository["default_branch"],
            archived=repository["archived"],
            topics=repository["topics"],
        )
        if repository.get("template_repository"):
            repo.template = Template(
                owner=repository["template_repository"]["owner"]["login"],
                repository=repository["template_repository"]["name"],
            )

        return repo

    @staticmethod
    def visit_github_branch_protection(repository, branch):
        protection = GithubBranchProtection(
            repository=repository["name"],
            branch=branch["name"],
            enforce_admins=branch.get("enforce_admins", {}).get("enabled"),
            require_signed_commits=branch.get("require_signed_commits", {}).get(
                "enabled"
            ),
        )

        status_checks = branch.get("required_status_checks")
        if status_checks:
            protection.required_status_checks = RequiredStatusChecks(
                strict=status_checks["strict"], contexts=status_checks["contexts"]
            )

        reviews = branch.get("required_pull_request_reviews")
        if reviews:
            users = reviews.get("dismissal_restrictions", {}).get("users", [])
            teams = reviews.get("dismissal_restrictions", {}).get("teams", [])
            protection.required_pull_request_reviews = RequiredPullRequestReviews(
                dismiss_stale_reviews=reviews.get("dismiss_stale_reviews"),
                dismissal_users=[user["login"] for user in users],
                dismissal_teams=[team["slug"] for team in teams],
                require_code_owner_reviews=reviews.get("require_code_owner_reviews"),
                required_approving_review_count=reviews.get(
                    "required_approving_review_count"
                ),
            )

        restrictions = branch.get("restrictions")
        if restrictions:
            protection.restrictions = Restrictions(
                users=[user["login"] for user in restrictions["users"]],
                teams=[team["slug"] for team in restrictions["teams"]],
                apps=[app["slug"] for app in restrictions["apps"]],
            )

        return protection

    @staticmethod
    def visit_github_issue_label(repository, issue):
        return GithubIssueLabel(
            repository=repository["name"],
            name=issue["name"],
            color=issue["color"],
            description=issue["description"],
            _url=issue["url"],
        )

    @staticmethod
    def visit_github_repository_webhook(repository, webhook):
        hook = GithubRepositoryWebhook(
            repository=repository["name"],
            events=webhook["events"],
            configuration=Configuration(
                url=webhook["config"]["url"],
                content_type=webhook["config"]["content_type"],
                insecure_ssl=webhook["config"]["insecure_ssl"] == "true",
            ),
            active=webhook["active"],
            _name=webhook["name"],
            _id=webhook["id"],
        )
        return hook

    @staticmethod
    def visit_github_membership(membership):
        return GithubMembership(username=membership["login"], role=membership["role"])

    @staticmethod
    def visit_github_organization_block(membership):
        return GithubOrganizationBlock(username=membership["login"])

    @staticmethod
    def visit_github_organization_project(project):
        return GithubOrganizationProject(name=project["name"], body=project["body"], _id=project["id"])

    @staticmethod
    def visit_github_repository_project(repository, project):
        return GithubRepositoryProject(
            name=project["name"], repository=repository["name"], body=project["body"],
            _id=project["id"]
        )

    @staticmethod
    def visit_github_organization_webhook(webhook):
        config = webhook.get("config", {})
        hook = GithubOrganizationWebhook(
            events=webhook["events"],
            configuration=Configuration(
                config["url"],
                config["content_type"],
                config.get("insecure_ssl", False),
                config.get("secret"),
            ),
            name=webhook["name"],
            active=webhook["active"],
            _id=webhook["id"],
        )

        return hook

    @staticmethod
    def visit_github_project_column(project, column):
        return GithubProjectColumn(project_id=project["id"], name=column["name"])

    @staticmethod
    def visit_github_repository_collaborator(repository, collaborator):
        return GithubRepositoryCollaborator(
            repository=repository["name"],
            username=collaborator["login"],
            permission=max_permissions(collaborator["permissions"]),
        )

    @staticmethod
    def visit_github_repository_deploy_key(repository, deploy_key):
        return GithubRepositoryDeployKey(
            key=deploy_key["key"],
            read_only=deploy_key["read_only"],
            repository=repository["name"],
            title=deploy_key["title"],
            _id=deploy_key["id"],
        )

    @staticmethod
    def visit_github_team(team):
        parent = team["parent"] or {}
        return GithubTeam(
            name=team["name"],
            description=team["description"],
            privacy=team["privacy"],
            parent_team_id=parent.get("id", None),
            ldap_dn=None,  # TODO: what this
            _team_id=team["id"],
            _team_slug=team["slug"],
        )

    @staticmethod
    def visit_github_team_membership(team, member):
        return GithubTeamMembership(
            _team_name=team["name"],
            _team_slug=team["slug"],
            team_id=team["id"],
            username=member["login"],
            role=member["role"]
        )

    @staticmethod
    def visit_github_team_repository(team, repository):
        return GithubTeamRepository(
            _team_name=team["name"],
            _team_slug=team["slug"],
            team_id=team["id"],
            repository=repository["name"],
            permission=max_permissions(repository["permissions"]),
        )
