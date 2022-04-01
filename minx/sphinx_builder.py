from sphinx.application import Sphinx
from sphinx.util.docutils import patch_docutils, docutils_namespace


class MySphinx(Sphinx):
    pass


def make_app():
    confdir = sourcedir = "docs"
    outputdir = doctreedir = "docs/_build"
    builder = "html"
    confoverrides = {}
    status = warning = None
    freshenv = False
    warningiserror = False
    tags = []
    verbosity = 0
    jobs = 0
    keep_going = False
    force_all = False
    filenames = []
    patch_docutils(confdir)
    docutils_namespace()
    app2 = MySphinx(
        srcdir=sourcedir,
        confdir=confdir,
        outdir=outputdir,
        buildername="html",
        doctreedir=doctreedir,
    )
    return app2
