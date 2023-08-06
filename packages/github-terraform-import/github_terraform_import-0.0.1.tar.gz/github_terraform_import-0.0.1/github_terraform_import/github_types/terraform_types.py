from dataclasses import dataclass
from typing import List


class TerraformSyntax:
    pass


@dataclass
class Resource(TerraformSyntax):
    pass


@dataclass
class Block(TerraformSyntax):
    pass
