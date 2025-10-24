# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
\t@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
\t@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Build HTML documentation
html:
\t@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
\t@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Generate translation files
gettext:
\t@$(SPHINXBUILD) -b gettext "$(SOURCEDIR)" "$(BUILDDIR)/locale" $(SPHINXOPTS)
\t@echo "Build finished. The message catalogs are in $(BUILDDIR)/locale."

# Update translations
update-i18n: gettext
\tsphinx-intl update -p $(BUILDDIR)/locale -l fr -l ja -l zh_CN

# Build French documentation
html-fr:
\t@$(SPHINXBUILD) -b html -D language=fr "$(SOURCEDIR)" "$(BUILDDIR)/html/fr" $(SPHINXOPTS)

# Build Japanese documentation
html-ja:
\t@$(SPHINXBUILD) -b html -D language=ja "$(SOURCEDIR)" "$(BUILDDIR)/html/ja" $(SPHINXOPTS)

# Build Chinese documentation
html-zh:
\t@$(SPHINXBUILD) -b html -D language=zh_CN "$(SOURCEDIR)" "$(BUILDDIR)/html/zh" $(SPHINXOPTS)

# Build all languages
html-all: html html-fr html-ja html-zh
\t@echo "All documentation built successfully."

