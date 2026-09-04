# Contributor and AI Agent Guide

## Project scope

This repository contains a Python driver for the Morningstar TriStar TS-MPPT-60 solar
charge controller. The project uses a `src/` layout and is published as
`tsmppt60-driver`.

All repository-authored documentation, code comments, and user-facing text must be written
in English. Preserve protocol names, register identifiers, and externally visible behavior
exactly unless the task explicitly requests a change.

## Project structure

- Keep importable package code under `src/tsmppt60_driver/`.
- Keep automated tests under `test/`, organized consistently with the code they cover.
- Keep protocol knowledge and source provenance under `docs/okf/tsmppt-modbus/`.
- Use the existing repository structure and public module boundaries before introducing new ones.
- Do not add importable modules at the repository root.

## Python and tooling

- Treat `pyproject.toml` as the single source of truth for supported Python versions,
  package metadata, dependencies, test configuration, and Ruff configuration.
- Treat `mise.toml` as the source of truth for the local toolchain and `poetry.toml` as
  the source of truth for Poetry virtual-environment behavior.
- Use the project's in-project `.venv` when available.
- Read and follow the current tool settings from the configuration files; do not duplicate
  their details in this document.
- Prefer the standard library and small, focused changes. Add dependencies only when
  necessary, and declare them in the project configuration.

Typical validation commands are:

```bash
poetry run pytest
poetry run ruff check .
poetry run ruff format --check .
```

Run relevant tests after behavioral changes. Run the full test suite and configured checks
before submitting a change when the environment permits it.

## General development principles

- Preserve public APIs and externally visible data formats unless an API change is explicitly requested.
- Keep responsibilities separated according to the existing architecture; avoid moving
  transport, protocol decoding, and domain behavior across boundaries without a clear reason.
- Use type annotations for new or modified interfaces and keep functions focused.
- Do not silently accept malformed external data. Preserve or improve validation at input boundaries.
- Keep retry, timeout, and error-handling behavior explicit. Do not introduce unbounded
  retries, blocking waits, or silent exception handling.
- Keep network and hardware access behind the existing abstractions. Tests must not require
  access to a real controller.
- Update tests and user-facing documentation when changing observable behavior.

## TriStar Modbus knowledge

For TriStar MPPT Modbus work, read `docs/okf/tsmppt-modbus/index.md` first and then the
relevant linked documents. Use `source.md` to identify the authoritative source and its
provenance.

When handling register values, verify the PDU address, Logical Address, word order,
scaling, signedness, units, and read/write access. Do not infer a protocol detail from
similar-looking registers without checking the source documentation.

The source specification contains documented internal inconsistencies. Keep those
discrepancies visible in the OKF documents and verify against target firmware or hardware
before making a protocol-level decision.

Writes that alter controller settings or operating state can affect a live charger. Keep
such operations explicit, separate from read-only paths, and covered by appropriate tests.

## Documentation and repository hygiene

- Keep technical documentation and source comments in English.
- When changing protocol behavior, update the relevant OKF document and tests.
- When changing installation or public usage behavior, update `README.md` and the project
  configuration together.
- The project configuration is authoritative for dependencies; do not assume a dependency
  mentioned only in README is installed.
- Do not commit generated build artifacts, virtual environments, caches, or local secrets.
