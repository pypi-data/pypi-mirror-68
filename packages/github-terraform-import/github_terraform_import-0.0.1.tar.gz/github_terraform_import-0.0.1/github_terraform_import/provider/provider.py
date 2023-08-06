from .loader import EndpointLoader
from .unwrapper import PacketUnwrapper


class GithubProvider:
    def __init__(self, token, organization):
        self._loader = EndpointLoader(token, organization)

    def visit(self, visitor):
        self._visit(visitor, "github_membership")
        self._visit(visitor, "github_organization_block")

        self.load_repositories(visitor)

        self._visit(
            visitor,
            "github_organization_project",
            resource_callback=self._load_project_columns,
            dependent_resources=("github_project_column",),
        )
        self._visit(visitor, "github_organization_webhook")

        self._visit(
            visitor,
            "github_team",
            resource_callback=self._visit_teams,
            dependent_resources=("github_team_membership", "github_team_repository"),
        )

    def _visit(
        self,
        visitor,
        resource_name,
        loader_args=tuple(),
        unwrapper_args=tuple(),
        resource_callback=None,
        dependent_resources=tuple(),
    ):
        dependent_resources += (resource_name,)
        if all(map(lambda name: name not in visitor.resources, dependent_resources)):
            return

        loader_method = getattr(self._loader, f"load_{resource_name}")
        for resource in loader_method(*loader_args):
            unwrapper = getattr(PacketUnwrapper, f"visit_{resource_name}")
            unwrapped_resource = unwrapper(*unwrapper_args, resource)

            visit_method = getattr(visitor, f"visit_{resource_name}", None)
            if visit_method is not None:
                visit_method(unwrapped_resource)

            if resource_callback is not None:
                resource_callback(visitor, resource, unwrapped_resource)

    def load_repositories(self, visitor):
        for repository in self._loader.load_repositories():
            repo_name = repository["name"]
            repository = self._loader.load_github_repository(repo_name)

            repo = PacketUnwrapper.visit_github_repository(repository)
            if "github_repository" in visitor.resources:
                visitor.visit_github_repository(repo)

            def visit_in_repo(
                resource_name, resource_callback=None, dependent_resources=tuple()
            ):
                self._visit(
                    visitor,
                    resource_name,
                    loader_args=(repo_name,),
                    unwrapper_args=(repository,),
                    resource_callback=None,
                    dependent_resources=dependent_resources,
                )

            visit_in_repo("github_actions_secret")
            visit_in_repo("github_branch_protection")
            visit_in_repo("github_repository_webhook")
            visit_in_repo("github_issue_label")
            visit_in_repo("github_repository_collaborator")
            visit_in_repo("github_repository_deploy_key")

            if repo.has_projects:
                visit_in_repo(
                    "github_repository_project",
                    self._load_project_columns,
                    ("github_project_column",),
                )

    def _load_project_columns(self, visitor, project, _):
        self._visit(
            visitor,
            "github_project_column",
            loader_args=(project["id"],),
            unwrapper_args=(project,),
        )

    def _visit_teams(self, visitor, team, _):
        def visit_in_team(resource_name):
            self._visit(
                visitor,
                resource_name,
                loader_args=(team["slug"],),
                unwrapper_args=(team,),
            )

        visit_in_team("github_team_membership")
        visit_in_team("github_team_repository")
