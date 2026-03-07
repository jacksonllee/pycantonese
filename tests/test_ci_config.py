import os

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

REPO_DIR = os.path.dirname(os.path.dirname(__file__))


def test_cargo_toml_rustling_has_no_path():
    """Cargo.toml must not have a path for rustling.

    CI uses the released rustling from crates.io.
    Local dev uses .cargo/config.toml to patch in the local path.
    """
    with open(os.path.join(REPO_DIR, "Cargo.toml"), "rb") as f:
        cargo = tomllib.load(f)
    rustling_dep = cargo["dependencies"]["rustling"]
    if isinstance(rustling_dep, dict):
        assert "path" not in rustling_dep, (
            "Cargo.toml must not specify a path for rustling. "
            "Use .cargo/config.toml [patch.crates-io] for local dev instead."
        )


def test_ci_workflows_have_uv_no_sources():
    """CI workflows using uv must set UV_NO_SOURCES to avoid local path overrides."""
    workflows_dir = os.path.join(REPO_DIR, ".github", "workflows")
    for name in ("python.yml",):
        with open(os.path.join(workflows_dir, name), "rb") as f:
            content = f.read()
        assert b"UV_NO_SOURCES" in content, (
            f"{name} must set UV_NO_SOURCES to prevent uv from using "
            "[tool.uv.sources] path overrides in CI."
        )
