from pathlib import Path

from sphinx.testing.util import SphinxTestApp


class MinxApp(SphinxTestApp):
    """Wrapper around Sphinx test app to clean up after builds."""

    def build(
        self, force_all: bool = False, filenames: list[str] | None = None
    ) -> None:
        """Do a build then call clean up."""
        # super().build(force_all=force_all, filenames=filenames)
        super().build()
        self.cleanup()


def make_app(srcdir: Path) -> MinxApp:  # noqa: D103
    # Make a directory in var to build into
    builddir = srcdir.parent.parent.parent / "var" / srcdir.name
    builddir.mkdir(exist_ok=True)
    return MinxApp(srcdir=srcdir, builddir=builddir)
