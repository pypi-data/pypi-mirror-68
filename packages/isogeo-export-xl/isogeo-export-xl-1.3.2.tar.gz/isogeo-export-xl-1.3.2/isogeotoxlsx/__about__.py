# Metadata bout the package to easily retrieve informations about it.
# see: https://packaging.python.org/guides/single-sourcing-package-version/

from datetime import date

__all__ = [
    "__title__",
    "__summary__",
    "__uri__",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    "__copyright__",
]

__author__ = "Isogeo"
__copyright__ = "2016 - {0}, {1}".format(date.today().year, __author__)
__email__ = "contact@isogeo.com"
__license__ = "GNU Lesser General Public License v3.0"
__summary__ = "Toolbelt to export metadata from the Isogeo REST API into Microsoft Excel workbooks (.xlsx)."
__title__ = "Isogeo MS Excel Exporter"
__title_clean__ = "".join(e for e in __title__ if e.isalnum())
__uri__ = "https://github.com/isogeo/export-xlsx-py/"

__version__ = "1.3.2"
__version_info__ = tuple(
    [
        int(num) if num.isdigit() else num
        for num in __version__.replace("-", ".", 1).split(".")
    ]
)
