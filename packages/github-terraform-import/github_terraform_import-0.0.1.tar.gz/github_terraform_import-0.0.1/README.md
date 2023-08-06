# Github Terraform Import

Python library to allow simple programmatic control of importing a Github organization as terraform resources.

The library exposes four key components:
* Dataclass definitions of all terraform resources in the Github Provider (`github_terraform_import.formatter.github_types.*`)
* Formatter to easily convert dataclass types into valid terraform configuration syntax (`github_terraform_import.formatter.Formatter`)
* A metaclass required to implement a visitor pattern for all resources ([`github_terraform_import.visitor.VisitMethodInjector`](#visitmethodinjector))
* An interface with the Github REST API that will dynamically load Github resources based on methods defined in the given visitor class `github_terraform_import.provider.GithubProvider`


## Usage
Create a file for each repository which contains the following repository specific resources `github_repository`, `github_repository_collaborator`, `github_team_repository`.

```python
import os
import sys

from github_terraform_import.visitor import VisitMethodInjector
from github_terraform_import.github_types import (
    GithubRepository,
    GithubRepositoryCollaborator,
    GithubTeamRepository,
)
from github_terraform_import.provider import GithubProvider
from github_terraform_import.formatter import Formatter


class RepositoryConfigurationGenerator(metaclass=VisitMethodInjector):
    def __init__(self, path):
        self._root = path

    def visit_github_repository(self, repository: GithubRepository):
        file_ = os.path.join(self._root, f"{repository.name}.tf")
        with open(file_, "a+") as f:
            Formatter.format(repository.name, repository, out=f)

    def visit_github_repository_collaborator(
        self, collaborator: GithubRepositoryCollaborator
    ):
        file_ = os.path.join(self._root, f"{collaborator.repository}.tf")
        with open(file_, "a+") as f:
            Formatter.format(collaborator.username, collaborator, out=f)

    def visit_github_team_repository(self, team: GithubTeamRepository):
        file_ = os.path.join(self._root, f"{team.repository}.tf")
        with open(file_, "a+") as f:
            Formatter.format(team.team_id, team, out=f)


def main():
    if len(sys.argv) < 4:
        print("Usage: example {token} {organization} {output_directory}")
        exit()

    directory = sys.argv[3]
    if not os.path.exists(directory):
        os.makedirs(directory)

    generator = RepositoryConfigurationGenerator(directory)
    provider = GithubProvider(sys.argv[1], sys.argv[2])
    provider.visit(generator)


if __name__ == "__main__":
    main()
```

## Features
* Wrap around the Github API to provide terraform resources
* Typed resources for each of the terraform resources
* Dynamic resource fetching based on declared visitor methods
* Automatic caching of resources on multiple runs
* Formatting of resource classes to terraform configuration
* Detectable missing visitor methods


## Supported Resources
| Resource | Supported | Notes |
| - | - | - |
| github_actions_secret | :heavy_check_mark: | `plaintext_value` value cannot be imported from Github API, this must be added manually. Defaults to 'WARNING: Secrets cannot be imported via Github API' |
| github_branch |  |
| github_branch_protection | :heavy_check_mark: |
| github_issue_label | :heavy_check_mark: |
| github_membership | :heavy_check_mark: |
| github_organization_block | :heavy_check_mark: |
| github_organization_project | :heavy_check_mark: |
| github_organization_webhook | :heavy_check_mark: |
| github_project_column | :heavy_check_mark: |
| github_repository | :heavy_check_mark: | `delete_branch_on_merge`, `auto_init`, `gitignore_template`, `license_template` are not provided by the API |
| github_repository_collaborator | :heavy_check_mark: |
| github_repository_deploy_key | :heavy_check_mark: |
| github_repository_file |  |
| github_repository_project | :heavy_check_mark: |
| github_repository_webhook | :heavy_check_mark: |
| github_team | :heavy_check_mark: | `ldap_dn` not provided by the API |
| github_team_membership | :heavy_check_mark: |
| github_team_repository | :heavy_check_mark: |
| github_user_gpg_key |  |
| github_user_invitation_accepter |  |
| github_user_ssh_key |  |


## VisitMethodInjector
Use the `VisitMethodInjector` metaclass in your customised visitor class to provide instructions for handling various fetched resources.

### Standard Use
The standard use case for your visitor class is to define a method for each of the resources you wish to import. For example if you wish to import all the repository webhooks, a class like `FetchRepositoryWebhooks` would suffice.

```python
class FetchRepositoryWebhooks(metaclass=VisitMethodInjector):
    def visit_github_repository_webhook(self, webhook: GithubRepositoryWebhook):
        pass
```

Visit methods must be named, as `visit_{resource_name}`.

### Default Method
If there is some method that should be run for every resource without an implemented visitor method, you can use the default method for this purpose.

```python
class FetchWithDefault(metaclass=VisitMethodInjector):
    def visit_github_repository_webhook(self, webhook: GithubRepositoryWebhook):
        pass

    def default(self, resource: Resource):
        print(resource)
```

`FetchWithDefault` will call default for all of the resources except `github_repository_webhook`.

### Validation
If you want to ensure that every resource has an implemented visitor method, then setting the class variable `ignore_missing` to `False` will cause a `TypeError` to be thrown if there are any missing visitor methods.

```python
class FetchWithValidation(metaclass=VisitMethodInjector):
    ignore_missing = False
```

`FetchWithValidation` will throw a type exception when constructed listing all of the missing visit methods.


## Formatter
The `Formatter` class provides a way of converting the supplied dataclasses for each resource into an appropriately formatted Terraform resource.

This is accomplished by calling the `Formatter.format` method. The method can also be used for any custom dataclasses so long as they inherit from `github_terraform_import.github_types.Resource`.

Any member variables starting with an underscore, conventionally private, are not generated in the resource.

```python
@dataclass
class NestedDetails(Block):
    description: str
    topics: List[str]

@dataclass
class MyTerraformResource(Resource):
    name: str
    id: int
    valid: bool

    friends: List[str]

    details: NestedDetails
```

The above `MyTerraformResource` is an example dataclass definition which showcases the various supported types of the formatter.

Executing the following will write the resource to `out.txt`
```python
details = NestedDetails(
    description="Things I like",
    topics=["verification", "optimisation"],
)

resource = MyTerraformResource(
    name="a special resource",
    id="special",
    valid=True,
    friends=[],
    details=details,
)


with open("out.txt", "w") as file:
    Formatter.format("my_resource_name", resource, out=file)
```

The contents of out should then be:
```
resource "my_terraform_resource" "my_resource_name" {
    name = "a special resource"
    id = special
    valid = true
    friends = []
    details {
        description = "Things I like"
        topics = [
            "verification"
            "optimisation"
        ]
    }
}
```

If the `out` keyword argument is omitted from the `Formatter.format` method then the resource will be printed to standard out.
