"""Module containing functions to parse attributes in the source code."""

import ast
import inspect
from functools import lru_cache
from textwrap import dedent
from types import ModuleType
from typing import Any, Iterable, List, Optional, Union

from pytkdocs.objects import Attribute

RECURSIVE_NODES = (ast.If, ast.IfExp, ast.Try, ast.With, ast.ExceptHandler)


def node_is_docstring(node: ast.AST) -> bool:
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Str)


def node_to_docstring(node: Union[ast.Expr, ast.Str]) -> str:
    return node.value.s  # type: ignore


def node_is_assignment(node: ast.AST) -> bool:
    return isinstance(node, ast.Assign)


def node_is_annotated_assignment(node: ast.AST) -> bool:
    return isinstance(node, ast.AnnAssign)


def node_to_names(node: ast.Assign) -> dict:
    names = []
    for target in node.targets:
        if isinstance(target, ast.Attribute):
            names.append(target.attr)
        elif isinstance(target, ast.Name):
            names.append(target.id)
    return {"names": names, "lineno": node.lineno, "type": inspect.Signature.empty}


def node_to_annotated_names(node: ast.AnnAssign) -> dict:
    try:
        name = node.target.id  # type: ignore
    except AttributeError:
        name = node.target.attr  # type: ignore
    lineno = node.lineno
    return {"names": [name], "lineno": lineno, "type": node_to_annotation(node)}


def node_to_annotation(node) -> Union[str, object]:
    if isinstance(node, ast.AnnAssign):
        try:
            annotation = node.annotation.id  # type: ignore
        except AttributeError:
            if isinstance(node.annotation, ast.Str):
                annotation = node.annotation.s
            else:
                annotation = node.annotation.value.id  # type: ignore
        if hasattr(node.annotation, "slice"):
            annotation += f"[{node_to_annotation(node.annotation.slice.value)}]"  # type: ignore
        return annotation
    elif isinstance(node, ast.Subscript):
        return f"{node.value.id}[{node_to_annotation(node.slice.value)}]"  # type: ignore
    elif isinstance(node, ast.Tuple):
        annotations = [node_to_annotation(n) for n in node.elts]
        return ", ".join(a for a in annotations if a is not inspect.Signature.empty)  # type: ignore
    elif isinstance(node, ast.Name):
        return node.id
    return inspect.Signature.empty


def get_attribute_info(node1, node2):
    if node_is_docstring(node2):
        info = {"docstring": node_to_docstring(node2)}
        if node_is_assignment(node1):
            info.update(node_to_names(node1))
            return info
        elif node_is_annotated_assignment(node1):
            info.update(node_to_annotated_names(node1))
            return info
    raise ValueError(f"nodes must be assignment and docstring, not '{node1}' and '{node2}'")


@lru_cache(maxsize=None)
def get_attributes(module: ModuleType) -> List[Attribute]:
    file_path = module.__file__
    with open(file_path) as stream:
        code = stream.read()
    initial_ast_body = ast.parse(code).body
    return _get_attributes(initial_ast_body, name_prefix=module.__name__, file_path=file_path)


def _get_attributes(
    ast_body: Iterable, name_prefix: str, file_path: str, properties: Optional[List[str]] = None
) -> List[Attribute]:
    if not properties:
        properties = []

    documented_attributes = []
    previous_node = None
    body: Any

    for node in ast_body:
        try:
            attr_info = get_attribute_info(previous_node, node)
        except ValueError:
            if isinstance(node, RECURSIVE_NODES):
                documented_attributes.extend(_get_attributes(node.body, name_prefix, file_path, properties))  # type: ignore
                if isinstance(node, ast.Try):
                    for body in [node.handlers, node.orelse, node.finalbody]:
                        documented_attributes.extend(_get_attributes(body, name_prefix, file_path, properties))
                elif isinstance(node, ast.If):
                    documented_attributes.extend(_get_attributes(node.orelse, name_prefix, file_path, properties))

            elif isinstance(node, ast.FunctionDef) and node.name == "__init__":
                documented_attributes.extend(_get_attributes(node.body, name_prefix, file_path))

            elif isinstance(node, ast.ClassDef):
                documented_attributes.extend(
                    _get_attributes(node.body, f"{name_prefix}.{node.name}", file_path, properties=["class-attribute"])
                )
        else:
            for name in attr_info["names"]:
                documented_attributes.append(
                    Attribute(
                        name=name,
                        path=f"{name_prefix}.{name}",
                        file_path=file_path,
                        docstring=dedent(attr_info["docstring"]),
                        properties=properties,
                        attr_type=attr_info["type"],
                    )
                )
        previous_node = node

    return documented_attributes
