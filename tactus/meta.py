"""Module for resolving the distribution name and version of the calling context."""

import importlib.metadata
from inspect import stack


def _resolve_distribution_name() -> str:
    """Resolve the distribution name of the calling context.

    Done by walking the call stack and matching the top-level package name
    against installed distributions.

    Returns the distribution name of the first recognisable caller, or falls
    back to package A's own distribution name if no external caller is found.
    """
    own_top_level = __name__.split(".", maxsplit=1)[0]

    for frame_info in stack():
        module_name = frame_info.frame.f_globals.get("__name__", "")
        top_level_package = module_name.split(".")[0]

        # Skip internals, this package itself, and empty/dunder names
        if not top_level_package or top_level_package in ("__main__", own_top_level):
            continue

        try:
            packages_map = importlib.metadata.packages_distributions()
            distributions = packages_map.get(top_level_package)
            if distributions:
                return distributions[0]
        except (importlib.metadata.PackageNotFoundError, ValueError):
            continue

    # Fallback: return package A's own distribution name
    return own_top_level


def _resolve_distribution_version(distribution_name: str) -> str:
    """Resolve the installed version for the given distribution name.

    Args:
        distribution_name: The PyPI distribution name to look up

    Returns:
        The version string (e.g. "1.2.3"), or "0.0.0" if it cannot be determined.
    """
    try:
        return importlib.metadata.version(distribution_name)
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"


# ---------------------------------------------------------------------------
# Module-level constants — resolved once at import time in the caller's context
# ---------------------------------------------------------------------------

#: The distribution name of whichever package is at the top of the call stack.
#: Resolves to "package-b" when imported from package B, "package-a" otherwise.
PACKAGE_NAME: str = _resolve_distribution_name()

#: The installed version of that same distribution (e.g. "1.2.3").
PACKAGE_VERSION: str = _resolve_distribution_version(PACKAGE_NAME)
