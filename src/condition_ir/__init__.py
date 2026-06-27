"""Typed Common Expression Language (CEL) condition IR, solver, and backends.

Parse CEL source via ``cel-parser``, type-check it against a concept/kind
registry, carry the result as a ``CheckedCondition``, and evaluate or compile
the closed ``ConditionIR`` to multiple backends: Z3 SMT (sat/unsat/definedness,
including TIMEPOINT ordering), parameterized SQL, a Python AST, and an ESTree
AST. A deterministic JSON codec round-trips the IR.
"""

from __future__ import annotations

from condition_ir.cel_frontend import (
    CelError,
    check_cel_expression,
    check_condition_ir,
    condition_ir_from_cel,
)
from condition_ir.cel_types import (
    CelExpr,
    CelRegistryFingerprint,
    to_cel_expr,
    to_cel_exprs,
)
from condition_ir.checked import (
    CheckedCondition,
    CheckedConditionSet,
    checked_condition_set,
    checked_condition_set_from_json,
    checked_condition_set_to_json,
)
from condition_ir.codec import condition_ir_from_json, condition_ir_to_json
from condition_ir.estree_backend import (
    EstreeArrayExpression,
    EstreeBinaryExpression,
    EstreeCallExpression,
    EstreeConditionalExpression,
    EstreeExpression,
    EstreeIdentifier,
    EstreeLiteral,
    EstreeLogicalExpression,
    EstreeMemberExpression,
    EstreeUnaryExpression,
    condition_ir_to_estree,
    evaluate_estree_expression,
)
from condition_ir.ir import (
    ConditionBinary,
    ConditionBinaryOp,
    ConditionChoice,
    ConditionIR,
    ConditionLiteral,
    ConditionMembership,
    ConditionReference,
    ConditionSourceSpan,
    ConditionUnary,
    ConditionUnaryOp,
    ConditionValueKind,
)
from condition_ir.python_backend import (
    condition_ir_to_python_ast,
    evaluate_condition_ir,
)
from condition_ir.registry import (
    ConceptInfo,
    KindType,
    condition_registry_fingerprint,
    scope_condition_registry,
    synthetic_category_concept,
    with_standard_synthetic_bindings,
    with_synthetic_concepts,
)
from condition_ir.solver import (
    DEFAULT_Z3_TIMEOUT_MS,
    ConditionSolver,
    SolverResult,
    SolverSat,
    SolverUnknown,
    SolverUnknownReason,
    SolverUnsat,
    Z3TranslationError,
    Z3UnknownError,
    solver_result_from_z3,
)
from condition_ir.sql_backend import (
    SqlConditionFragment,
    condition_ir_to_sql,
)
from condition_ir.z3_backend import (
    condition_ir_to_z3,
    z3_bindings_for_values,
)

__all__ = [
    "CelError",
    "CelExpr",
    "CelRegistryFingerprint",
    "CheckedCondition",
    "CheckedConditionSet",
    "ConceptInfo",
    "ConditionBinary",
    "ConditionBinaryOp",
    "ConditionChoice",
    "ConditionIR",
    "ConditionLiteral",
    "ConditionMembership",
    "ConditionReference",
    "ConditionSolver",
    "ConditionSourceSpan",
    "ConditionUnary",
    "ConditionUnaryOp",
    "ConditionValueKind",
    "DEFAULT_Z3_TIMEOUT_MS",
    "EstreeArrayExpression",
    "EstreeBinaryExpression",
    "EstreeCallExpression",
    "EstreeConditionalExpression",
    "EstreeExpression",
    "EstreeIdentifier",
    "EstreeLiteral",
    "EstreeLogicalExpression",
    "EstreeMemberExpression",
    "EstreeUnaryExpression",
    "KindType",
    "SolverResult",
    "SolverSat",
    "SolverUnknown",
    "SolverUnknownReason",
    "SolverUnsat",
    "SqlConditionFragment",
    "Z3TranslationError",
    "Z3UnknownError",
    "check_cel_expression",
    "check_condition_ir",
    "checked_condition_set",
    "checked_condition_set_from_json",
    "checked_condition_set_to_json",
    "condition_ir_from_cel",
    "condition_ir_from_json",
    "condition_ir_to_estree",
    "condition_ir_to_json",
    "condition_ir_to_python_ast",
    "condition_ir_to_sql",
    "condition_ir_to_z3",
    "condition_registry_fingerprint",
    "evaluate_condition_ir",
    "evaluate_estree_expression",
    "scope_condition_registry",
    "solver_result_from_z3",
    "synthetic_category_concept",
    "to_cel_expr",
    "to_cel_exprs",
    "with_standard_synthetic_bindings",
    "with_synthetic_concepts",
    "z3_bindings_for_values",
]
