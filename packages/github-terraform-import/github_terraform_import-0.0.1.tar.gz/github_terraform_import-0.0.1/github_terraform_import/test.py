import sys
import unittest
from io import StringIO
from unittest import TestCase

from .github_types.github_branch_protection import (
    GithubBranchProtection,
    RequiredStatusChecks,
    RequiredPullRequestReviews,
    Restrictions,
)
from .formatter import Formatter

from .provider import GithubProvider
from .visitor import VisitMethodInjector


class TestBranchProtection(TestCase):
    EXEMPLAR = """resource "github_branch_protection" "example" {
    repository = "${github_repository.example.name}"
    branch = "master"
    enforce_admins = true
    required_status_checks {
        strict = false
        contexts = [
            "ci/travis"
        ]
    }
    required_pull_request_reviews {
        dismiss_stale_reviews = true
        dismissal_users = [
            "foo-user"
        ]
        dismissal_teams = [
            "${github_team.example.slug}"
            "${github_team.second.slug}"
        ]
    }
    restrictions {
        users = [
            "foo-user"
        ]
        teams = [
            "${github_team.example.slug}"
        ]
        apps = [
            "foo-app"
        ]
    }
}
"""

    SMALL_RESOURCE = """resource "github_branch_protection" "small_example" {
    repository = "github-terraform-importer"
    branch = "master"
}
"""

    def setUp(self):
        self.maxDiff = 1000
        self._exemplar = GithubBranchProtection(
            repository="${github_repository.example.name}",
            branch="master",
            enforce_admins=True,
            required_status_checks=RequiredStatusChecks(
                strict=False, contexts=["ci/travis"]
            ),
            required_pull_request_reviews=RequiredPullRequestReviews(
                dismiss_stale_reviews=True,
                dismissal_users=["foo-user"],
                dismissal_teams=[
                    "${github_team.example.slug}",
                    "${github_team.second.slug}",
                ],
            ),
            restrictions=Restrictions(
                users=["foo-user"],
                teams=["${github_team.example.slug}"],
                apps=["foo-app"],
            ),
        )
        self._small = GithubBranchProtection(
            repository="github-terraform-importer", branch="master"
        )

    def test_encoding(self):
        output = StringIO()
        Formatter.format("example", self._exemplar, out=output)

        self.assertEqual(TestBranchProtection.EXEMPLAR, output.getvalue())

    def test_small_encoding(self):
        output = StringIO()
        Formatter.format("small_example", self._small, out=output)

        self.assertEqual(TestBranchProtection.SMALL_RESOURCE, output.getvalue())


class DummyVisitor(metaclass=VisitMethodInjector):
    ignore_missing = True

    def default(self, resource):
        Formatter.format("test", resource)


class TestVisitor(metaclass=VisitMethodInjector):
    ignore_missing = True

    def visit_github_project_column(self, resource):
        Formatter.format("thing", resource)

    # def visit_github_team(self, resource):
    #     Formatter.format(f"{resource.name}", resource)

    # def visit_github_team_membership(self, resource):
    #     Formatter.format(f"{resource.username}", resource)

    # def visit_github_team_repository(self, resource):
    #     Formatter.format(f"{resource.repository}", resource)


class TestGithubProvider(TestCase):
    TOKEN = ""

    def test_all_providers(self):
        provider = GithubProvider(TestGithubProvider.TOKEN, "Canva")

        visitor = TestVisitor()
        provider.visit(visitor)


def main():
    TestGithubProvider.TOKEN = sys.argv[1]
    sys.argv[1:] = sys.argv[2:]
    unittest.main()


if __name__ == "__main__":
    main()
