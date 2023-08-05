import ast
from good_smell import implemented_smells, SmellWarning


class GoodSmellFlake8:
    name = "good-smell"
    version = "0.1"

    def __init__(self, tree: ast.AST, filename: str):
        self.tree = tree
        self.filename = filename

    def run(self):
        for smell in implemented_smells:
            warnings = smell(tree=self.tree, path=self.filename).check_for_smell()
            warning: SmellWarning
            yield from (
                (warning.row, warning.col, f"{warning.code} {warning.msg}")
                for warning in warnings
            )
