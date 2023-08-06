import requests
from urllib.parse import urlsplit, urlunsplit

from ..util import cache

HEADERS = "application/vnd.github.mercy-preview+json, application/vnd.github.zzzax-preview+json, application/vnd.github.giant-sentry-fist-preview+json, application/vnd.github.inertia-preview+json"


class EndpointLoader:
    API = "https://api.github.com"

    def __init__(self, token, organization):
        self._token = token
        self._organization = organization

    def get_resource(self, endpoint):
        """Follow links for a resource to get all the resources"""
        response = requests.get(
            f"{EndpointLoader.API}{endpoint}",
            headers={
                "Authorization": f"token {self._token}",
                # to allow access to the topics field
                "Accept": HEADERS,
            },
        )
        # ignore empty things rather than causing an error
        if response.status_code == 204:
            return {}
        if response.status_code != 200:
            response.raise_for_status()
        users = response.json()

        links = response.links
        if "next" in links:
            parts = ("", "", *urlsplit(links["next"]["url"])[2:])
            link = urlunsplit(parts)
            users += self.get_resource(link)

        return users
    
    def cache_load(cache_id):
        def _decorator(method):
            def wrapper(self, *args, **kwargs) :
                id_ = self._organization + "/" + cache_id
                
                return cache(id_)(method)(self, *args, **kwargs)
            return wrapper
        return _decorator     

    @cache_load("actions-secret")
    def load_github_actions_secret(self, repository):
        return self.get_resource(
            f"/repos/{self._organization}/{repository}/actions/secrets"
        )["secrets"]

    @cache_load("repositories")
    def load_repositories(self):
        return self.get_resource(f"/orgs/{self._organization}/repos")

    @cache_load("repository")
    def load_github_repository(self, repository):
        return self.get_resource(f"/repos/{self._organization}/{repository}")

    @cache_load("webhook")
    def load_github_repository_webhook(self, repository):
        return self.get_resource(f"/repos/{self._organization}/{repository}/hooks")

    @cache_load("branch-protections")
    def load_github_branch_protection(self, repository):
        protection = self.get_resource(
            f"/repos/{self._organization}/{repository}/branches?protected=true"
        )

        protections = []
        for branch in protection:
            name = branch["name"]
            branch.update(
                self.get_resource(
                    f"/repos/{self._organization}/{repository}/branches/{name}/protection"
                )
            )
            require_signed = self.get_resource(
                f"/repos/{self._organization}/{repository}/branches/{name}/protection/required_signatures"
            )
            branch["required_signed_commits"] = require_signed

            protections.append(branch)

        return protections

    @cache_load("issue-labels")
    def load_github_issue_label(self, repository):
        return self.get_resource(f"/repos/{self._organization}/{repository}/labels")

    @cache_load("membership")
    def load_github_membership(self):
        members = self.get_resource(f"/orgs/{self._organization}/members?role=member")
        admins = self.get_resource(f"/orgs/{self._organization}/members?role=admin")

        for member in members:
            member["role"] = "member"
        for admin in admins:
            admin["role"] = "admin"

        return members + admins

    @cache_load("blocked")
    def load_github_organization_block(self):
        return self.get_resource(f"/orgs/{self._organization}/blocks")

    @cache_load("projects")
    def load_github_organization_project(self):
        return self.get_resource(f"/orgs/{self._organization}/projects")

    @cache_load("project-columns")
    def load_github_project_column(self, project):
        return self.get_resource(f"/projects/{project}/columns")

    @cache_load("projects")
    def load_github_repository_project(self, repository):
        return self.get_resource(f"/repos/{self._organization}/{repository}/projects")

    @cache_load("webhooks")
    def load_github_organization_webhook(self):
        return self.get_resource(f"/orgs/{self._organization}/hooks")

    @cache_load("collaborators")
    def load_github_repository_collaborator(self, repository):
        return self.get_resource(
            f"/repos/{self._organization}/{repository}/collaborators?affiliation=direct"
        )

    @cache_load("deploy-key")
    def load_github_repository_deploy_key(self, repository):
        return self.get_resource(f"/repos/{self._organization}/{repository}/keys")

    @cache_load("teams")
    def load_github_team(self):
        return self.get_resource(f"/orgs/{self._organization}/teams")

    @cache_load("team-members")
    def load_github_team_membership(self, team):
        members = self.get_resource(
            f"/orgs/{self._organization}/teams/{team}/members?role=member"
        )
        maintainers = self.get_resource(
            f"/orgs/{self._organization}/teams/{team}/members?role=maintainer"
        )

        for member in members:
            member["role"] = "member"
        for maintainer in maintainers:
            maintainer["role"] = "maintainer"

        return maintainers + members

    @cache_load("team-repositories")
    def load_github_team_repository(self, team):
        return self.get_resource(f"/orgs/{self._organization}/teams/{team}/repos")
