# Changelog

## 0.1.0

Initial extraction from the reference implementation.

- Closed semantic condition IR (`ir.py`): `ConditionIR` union over
  `ConditionLiteral`, `ConditionReference`, `ConditionUnary`, `ConditionBinary`,
  `ConditionMembership`, and `ConditionChoice`, with `ConditionSourceSpan`,
  `ConditionValueKind`, and the `ConditionUnaryOp` / `ConditionBinaryOp` operator
  enums. `ConditionReference.concept_id` is a plain `str`: the upstream
  `ConceptId` `NewType` and `to_concept_id` normalization are dropped, and ids
  are normalized with `str()`.
- Concept registry (`registry.py`): `ConceptInfo`, the `KindType` enum
  (QUANTITY, CATEGORY, BOOLEAN, STRUCTURAL, TIMEPOINT), a deterministic
  `condition_registry_fingerprint`, and the synthetic-binding helpers. The
  synthetic binding vocabulary is no longer hardcoded:
  `with_standard_synthetic_bindings(registry, synthetic_binding_names=())` takes
  the names from the caller (empty by default).
- Type-checked carriers (`checked.py`): `CheckedCondition` and
  `CheckedConditionSet` plus their JSON codecs.
- Deterministic JSON codec (`codec.py`): `condition_ir_to_json` /
  `condition_ir_from_json`.
- CEL frontend (`cel_frontend.py`): parse CEL via `cel-parser`, type-check
  against the registry (`check_cel_expression`, `CelError`), and lower to IR
  (`condition_ir_from_cel`, `check_condition_ir`).
- Solver (`solver.py`): `ConditionSolver` answering satisfiability,
  disjointness, equivalence, implication, and equivalence-class partitioning,
  with `SolverSat` / `SolverUnsat` / `SolverUnknown` results and Z3 error
  surfaces. TIMEPOINT concepts get `valid_from <= valid_until` ordering
  constraints.
- Backends: Z3 SMT (`z3_backend.py`, definedness-aware projection incl.
  division-by-zero and TIMEPOINT ordering), parameterized SQL
  (`sql_backend.py`), Python AST (`python_backend.py`), and ESTree
  (`estree_backend.py`) with an in-process ESTree evaluator.
- Typed CEL source carriers (`cel_types.py`): `CelExpr`,
  `CelRegistryFingerprint`, `to_cel_expr`, `to_cel_exprs`.
- No dependency on the originating reference implementation. Depends on
  `cel-parser` and `z3-solver`.
