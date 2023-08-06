import os
import json
import shlex
import subprocess

from .github_types import (
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
)
from .visitor import VisitMethodInjector
from .util import convert_type_to_method


class ImportException(Exception):
    pass


class ImportVisitor(metaclass=VisitMethodInjector):
    ignore_missing = False

    def __init__(self, organization):
        self._organization = organization

    def visit_github_actions_secret(self, secrets: GithubActionsSecret):
        raise ImportException("github_actions_secret is not a supported import")

    def visit_github_branch_protection(self, protection: GithubBranchProtection):
        return f"{protection.repository}:{protection.branch}"

    def visit_github_issue_label(self, label: GithubIssueLabel):
        return f"{label.repository}:{label.name}"

    def visit_github_membership(self, membership: GithubMembership):
        return f"{self._organization}:{membership.username}"

    def visit_github_organization_block(self, block: GithubOrganizationBlock):
        raise ImportException("github_organization_block is not a supported import")

    def visit_github_organization_project(self, project: GithubOrganizationProject):
        raise ImportException("github_organization_project is not a supported import")

    def visit_github_organization_webhook(self, hook: GithubOrganizationWebhook):
        raise ImportException("github_organization_webhook is not a supported import")

    def visit_github_project_column(self, column: GithubProjectColumn):
        raise ImportException("github_project_column is not a supported import")

    def visit_github_repository_collaborator(self, collaborator: GithubRepositoryCollaborator):
        return f"{collaborator.repository}:{collaborator.username}"
    
    def visit_github_repository_deploy_key(self, key: GithubRepositoryDeployKey):
        return f"{key.repository}:{key._id}"

    def visit_github_repository_project(self, project: GithubRepositoryProject):
        return f"{project.repository}/{project._id}"

    def visit_github_repository_webhook(self, hook: GithubRepositoryWebhook):
        return f"{hook.repository}/{hook._id}"

    def visit_github_repository(self, repository: GithubRepository):
        return repository.name

    def visit_github_team_membership(self, membership: GithubTeamMembership):
        return f"{membership.team_id}:{membership.username}"

    def visit_github_team_repository(self, repository: GithubTeamRepository):
        return f"{repository.team_id}:{repository.repository}"

    def visit_github_team(self, team: GithubTeam):
        return f"{team._team_id}"


class TerraformImporter:

    def __init__(self, token, organization):
        self._token = token
        self._env = os.environ.copy()
        self._env["GITHUB_TOKEN"] = token
        self._env["GITHUB_ORGANIZATION"] = organization

        self._organization = organization
        self._visitor = ImportVisitor(organization)

    def _terraform_initialised(self, directory):
        state_file = os.path.join(directory, "terraform.tfstate")
        if not os.path.exists(state_file):
            return False

    def _resource_exists(self, directory, resource_type, resource_name):
        state_file = os.path.join(directory, "terraform.tfstate")
        if not os.path.exists(state_file):
            return False

        with open(state_file, "r") as file:
            try:
                state = json.load(file)
            except json.JSONDecodeError:
                return False

            for resource in state["resources"]:
                if resource["name"] == resource_name and resource["type"] == resource_type:
                    return True
        
        return False

    def import_resource(self, directory, resource_name, resource):
        if not os.path.exists(directory):
            raise ImportException(f"{directory} does not exist")

        resource_type = convert_type_to_method(type(resource))
        exists = self._resource_exists(directory, resource_type, resource_name)
        if exists:
            return

        init_cmd = "terraform init"
        if not self._terraform_initialised(directory):
            subprocess.run(init_cmd.split(" "), env=self._env, cwd=directory)

        visit_method = getattr(self._visitor, f"visit_{resource_type}")
        resource_id = visit_method(resource)
        cmd = f'terraform import {resource_type}.{resource_name} "{resource_id}"'

        subprocess.run(shlex.split(cmd), env=self._env, cwd=directory)

    def cleanse_state(self, directory, expected):
        state_file = os.path.join(directory, "terraform.tfstate")
        if not os.path.exists(state_file):
            return

        extra_resources = []

        with open(state_file, "r") as file:
            try:
                state = json.load(file)
            except json.JSONDecodeError:
                return False

            for resource in state["resources"]:
                if resource["type"] in {"terraform_remote_state"}:
                    continue
                if resource["name"] not in expected:
                    extra_resources.append(resource)
        
        if len(extra_resources) == 0:
            return

        for resource in extra_resources:
            cmd = f"terraform state rm {resource['type']}.{resource['name']}"
            print(directory, cmd)
            subprocess.run(shlex.split(cmd), env=self._env, cwd=directory)