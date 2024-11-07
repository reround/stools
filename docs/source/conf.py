# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "TOOLS"
copyright = "2024, Shun"
author = "Shun"
release = "0.1.1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# extensions = []

import os, sys

sys.path.insert(0, os.path.abspath("../.."))

extensions = [
    "sphinx.ext.mathjax",
    "sphinxcontrib.video",
    "sphinx.ext.autodoc",
]


templates_path = ["_templates"]
exclude_patterns = []

language = "zh_CN"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]


# -- Options for LaTeX output ---------------------------------------------
latex_engine = "xelatex"  # 使用 xelatex
latex_documents = [
    ("index", "TOOLS.tex", "PY\_TOOLS", "Shun", "manual"),
]
mathjax_config = {
    "TeX": {
        "extensions": ["amsmath"],
    }
}

# \singlespacing         % 单倍行距
# \onehalfspacing        % 1.5倍行距
# \doublespacing         % 双倍行距
latex_elements = {
    "preamble": r"""
    \setcounter{tocdepth}{1} %目录编号深度
    \setcounter{secnumdepth}{1} % 章节编号深度
    \usepackage{amsmath}  % 引入 amsmath 包以支持公式编号
    \usepackage{indentfirst} % 首行缩进
    \setlength{\parindent}{2em} % 首行缩进 2 字符
    \usepackage{setspace}  %行距
    \onehalfspacing        % 1.5倍行距
    
    \newcommand{\chapterheadstartnew}{\newpage}
    \newcommand{\afterchaptertitle}{\newpage}
    \newcommand{\sectionheadstartnew}{\newpage}
    """,
    "fontpkg": r"""
        \usepackage{fontspec}
        \setmainfont{SimSun}  % 设置主字体为宋体
        \setsansfont{SimHei}  % 可选：设置无衬线字体为黑体
        \setmonofont{Courier New}  % 可选：设置等宽字体
    """,
    "classoptions": ",openany",  # 章节之间不分页，针对于 "manual"
    "figure_align": "H",
}
# latex_logo = "_static/imgs/logo.png"  # 自定义 logo
