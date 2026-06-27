# condition-ir

A typed **Common Expression Language (CEL)** condition IR. Parse CEL source with
[`cel-parser`](https://github.com/ctoth/cel-parser), type-check it against a
concept/kind registry, carry the result as a `CheckedCondition`, and then
evaluate or compile the closed `ConditionIR` to several backends. A deterministic
JSON codec round-trips the IR so a checked condition can be persisted and
re-loaded without reparsing.

The IR is the single chokepoint: every backend consumes the same closed
`ConditionIR` union, and the **Z3 SMT** backend is the one place that answers
satisfiability, disjointness, equivalence, and implication questions.

Requires Python 3.11+. Depends on `cel-parser` and `z3-solver`.

## Install

```powershell
uv add condition-ir
```

## Pipeline

```python
from condition_ir import (
    ConceptInfo,
    KindType,
    ConditionSolver,
    check_condition_ir,
    condition_ir_to_json,
)

# 1. Describe the concepts a condition may reference.
registry = {
    "fundamental_frequency": ConceptInfo(
        "concept:f0", "fundamental_frequency", KindType.QUANTITY
    ),
    "task": ConceptInfo(
        "concept:task", "task", KindType.CATEGORY,
        category_values=["speech", "singing"], category_extensible=True,
    ),
}

# 2. Parse + type-check CEL into a CheckedCondition (carries the IR + a
#    registry fingerprint + any non-fatal warnings).
checked = check_condition_ir(
    "fundamental_frequency > 200 && task == 'singing'", registry
)

# 3. Ask semantic questions through the Z3 solver.
solver = ConditionSolver(registry)
assert solver.is_condition_satisfied(
    checked, {"fundamental_frequency": 220, "task": "singing"}
)

# 4. Persist the IR deterministically.
payload = condition_ir_to_json(checked.ir)
```

## The IR

`ConditionIR` is a closed union of frozen dataclasses, each carrying a
`ConditionSourceSpan`:

- `ConditionLiteral` — a `bool` / `int` / `float` / `str` with a
  `ConditionValueKind` (`NUMERIC`, `TIMEPOINT`, `STRING`, `BOOLEAN`).
- `ConditionReference` — a named concept reference (`concept_id` is a plain
  `str`), its value kind, and optional category metadata.
- `ConditionUnary` / `ConditionBinary` — operators from `ConditionUnaryOp` /
  `ConditionBinaryOp`.
- `ConditionMembership` — `element in [options...]`.
- `ConditionChoice` — `condition ? when_true : when_false`.

`condition_ir_to_json` / `condition_ir_from_json` are a versioned, deterministic
codec for this union.

## Registry

`ConceptInfo` records the minimal information needed to type-check a reference: an
id, a canonical name, a `KindType` (`QUANTITY`, `CATEGORY`, `BOOLEAN`,
`STRUCTURAL`, `TIMEPOINT`), and category values/extensibility. `TIMEPOINT` is
numeric like `QUANTITY` but semantically distinct.

`condition_registry_fingerprint(registry)` is a deterministic
`CelRegistryFingerprint` over the condition-relevant semantics; a
`CheckedCondition` records the fingerprint it was validated against, and the
solver refuses conditions validated against a different registry.

The synthetic-binding vocabulary is **not** owned by this package.
`with_standard_synthetic_bindings(registry, synthetic_binding_names=())` seeds
extra non-concept bindings only for the names the caller supplies (empty by
default); `scope_condition_registry`, `with_synthetic_concepts`, and
`synthetic_category_concept` round out the registry helpers.

## CEL frontend

- `check_cel_expression(source, registry) -> list[CelError]` type-checks CEL
  against the registry, distinguishing hard errors from warnings (e.g. an
  out-of-set literal for an *extensible* category is a warning).
- `condition_ir_from_cel(source, registry) -> ConditionIR` lowers checked source
  to the IR.
- `check_condition_ir(source, registry) -> CheckedCondition` does both and
  bundles the IR with the registry fingerprint and warnings.

## Backends

- **Z3 SMT** (`condition_ir_to_z3`, and the full `ConditionSolver`): a
  definedness-aware projection into a single Z3 context. The solver answers
  `is_condition_satisfied`, `are_disjoint`, `are_equivalent`, `implies`, and
  `partition_equivalence_classes`, returning `SolverSat` / `SolverUnsat` /
  `SolverUnknown`. Division guards against divide-by-zero, and when both
  `<concept>_from` and `<concept>_until` TIMEPOINT concepts are present the
  solver adds the `from <= until` ordering constraint automatically.
- **SQL** (`condition_ir_to_sql`): a parameterized `SqlConditionFragment`
  (`ConditionChoice` is not projectable to SQL).
- **Python AST** (`condition_ir_to_python_ast`, `evaluate_condition_ir`): compile
  to an `ast.Expression` or evaluate directly against a bindings mapping.
- **ESTree** (`condition_ir_to_estree`, `evaluate_estree_expression`): an ESTree
  expression tree plus an in-process evaluator.

## Seams from the source extraction

This package was extracted from a larger reference implementation. Two seams were
generalized so it carries no host-specific vocabulary:

1. Concept ids are plain `str` (the host's `ConceptId` `NewType` is dropped).
2. The standard synthetic binding names are a caller-supplied parameter rather
   than a hardcoded list.

## License

MIT
