# Contributor and AI Agent Guide

## Project scope

This repository contains a Python driver for the Morningstar TriStar TS-MPPT-60 solar
charge controller. The package is published as `tsmppt60-driver` and uses a `src/`
layout.

All repository-authored documentation, code comments, and user-facing text must be written
in English. Preserve protocol names and register identifiers exactly as specified.

## Repository layout

- `src/tsmppt60_driver/`: installable package source.
- `src/tsmppt60_driver/hal/`: low-level HTTP/Modbus transport and register decoding.
- `src/tsmppt60_driver/controller/`: status-oriented domain controllers.
- `test/test_hal/`: transport, register, and scaling tests.
- `test/test_controller/`: controller and public status behavior tests.
- `docs/okf/tsmppt-modbus/`: OKF knowledge bundle for the protocol.
- `README.md`: public installation and usage documentation.
- `pyproject.toml`: package metadata, supported Python versions, development tools, and Ruff configuration.

Keep new package modules under `src/tsmppt60_driver/`. Keep tests under the corresponding
`test/` subtree. Do not add importable modules at the repository root.

## Python and tooling

- Treat `pyproject.toml` as the single source of truth for supported Python versions,
  package metadata, runtime dependencies, development dependencies, and Ruff configuration.
- Treat `mise.toml` as the source of truth for the local toolchain version and
  `poetry.toml` as the source of truth for Poetry virtual-environment behavior.
- Use the in-project `.venv` managed by Poetry when available.
- Use the `src` package import path in tests and examples.
- Read and follow the current Ruff settings from `pyproject.toml`; do not duplicate or
  override those settings in `AGENTS.md` unless the project configuration changes.
- Prefer standard-library solutions and small focused changes. Avoid adding a dependency for functionality already provided by the standard library.

Useful validation commands:

```bash
poetry run pytest
poetry run ruff check .
poetry run ruff format --check .
```

Run the relevant tests after every behavioral change. Run the full suite and Ruff checks
before submitting a change when the environment permits it.

## Coding conventions

- Preserve the public API exported by `tsmppt60_driver.__init__` and `tsmppt60_driver.hal` unless the task explicitly requests an API change.
- Use type annotations for new or modified interfaces and keep functions focused.
- Preserve the existing dataclass-based `Register`, `RegisterMap`, and `RegisterValue` model where applicable.
- Keep network access behind the existing transport abstraction. Tests must mock HTTP connections and must not contact a real controller.
- Preserve the existing status dictionary keys, group names, units, rounding behavior, and public output shape unless intentionally changing them with corresponding tests and README updates.
- Do not silently swallow malformed device responses. Validate response lengths and values where the surrounding code already does so.
- Keep retry and timeout behavior explicit; do not introduce unbounded retries or sleeps.

## Modbus knowledge

For TriStar MPPT Modbus implementation and review work, read
`docs/okf/tsmppt-modbus/index.md` first, followed by the relevant linked documents.

When handling register values, verify the PDU address, Logical Address, word order,
V_PU/I_PU scaling, signedness, and read/write access. If the OKF documents and
implementation conflict, check the source recorded in `docs/okf/tsmppt-modbus/source.md`
and do not resolve ambiguity by guessing.

The source specification contains known internal inconsistencies. In particular, the
hourmeter HI/LO order differs between the register table and the page-25 example, and the
`EVa_ref_fixed_init` priority note appears inconsistent with its address mapping. Keep
these discrepancies documented and verify against target firmware or hardware before
making a protocol-level decision.

EEPROM writes, coil commands that clear state, slave control, and fixed array-voltage
control can affect a live charger. Keep write operations separate from read-only paths,
require explicit calls, and add tests for safety-relevant behavior.

## Documentation and dependency consistency

When changing protocol behavior, update the relevant OKF document and tests. When changing
installation or public usage behavior, update `README.md` and `pyproject.toml` together.
Do not assume a dependency mentioned only in README is installed; the project metadata is
the authoritative dependency declaration.

Do not commit generated build artifacts, virtual environments, caches, or local secrets.
