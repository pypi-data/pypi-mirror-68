# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['otk',
 'otk.asbp',
 'otk.asbp.test',
 'otk.draw2',
 'otk.rt1',
 'otk.rt1.test',
 'otk.rt2',
 'otk.rt2.test',
 'otk.rtm4',
 'otk.sdb',
 'otk.sdb.npscalar',
 'otk.sdb.numba',
 'otk.sdb.test',
 'otk.sdb.webex',
 'otk.test']

package_data = \
{'': ['*']}

install_requires = \
['cairocffi>=1.1.0,<2.0.0',
 'chardet>=3.0.4,<4.0.0',
 'gizeh>=0.1.11,<0.2.0',
 'ipython>=7.14.0,<8.0.0',
 'mathx>=0.2,<0.3',
 'matplotlib>=3.2.1,<4.0.0',
 'numba>=0.49.1,<0.50.0',
 'numpy>=1.18.4,<2.0.0',
 'opt_einsum>=3.2.1,<4.0.0',
 'pyfftw>=0.12.0,<0.13.0',
 'pyopengl>=3.1.5,<4.0.0',
 'pyqt5>=5.12,<6.0',
 'pyqtgraph_extensions>=0.4.0,<0.5.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['view-zmx = otk.rt2.cli:view_zmx']}

setup_kwargs = {
    'name': 'otk',
    'version': '0.1.0',
    'description': 'Optics Tool Kit',
    'long_description': '# otk - optics toolkit\n\nToolkit for doing optics in Python\n\n<img src="screenshots/zemax_conic_telecentric_lens.png" width="400  " title="conic telecentric lens with rays"><img src="screenshots/cell-phone-lens.png" width="160" title="cell phone lens"><img src="screenshots/csg.png" width="160" title="cell phone lens">\n\nFeatures include\n\n* 3D engine based on [sphere tracing](https://link.springer.com/article/10.1007/s003710050084) for simple robust implicit surfaces and constructive solid geometry,\n* nonsequential ray tracing engine,\n* programmatic lookup of full [RefractiveIndex.INFO](https://refractiveindex.info/) database,\n* import of lenses and glass catalogs from Zemax.\n\n## Installation\n\nInstallation methods include:\n\n* Clone repository and interact with it using [Poetry](https://python-poetry.org/) e.g. `poetry run view-zmx <zemax-file>` or `poetry shell`.\n* Install in development mode with pip: `pip install -e <path-to-local-repo>`.\n* Install from package repository (e.g. PyPi) with pip: `pip install otk`.\n* Development mode with [: `poetry add <path-to-local-repo>`.\n* From package repository (e.g. PyPi) with Poetry: `poetry add otk`.\n\n## Getting started\n\n1. Check out the scripts in [examples](./examples).\n2. View one of the lenses in [designs](./designs) with the command line tool `view-zmx`.\n\n## Documentation\n\n(Yep, this is it at the moment.)\n\n### Command line tools\n\n`view-zmx <zemaxfile>` launches a viewer of a Zemax lens.\n\n### Packages\n\n* `otk.sdb` - Geometry library based on signed distance bounds.\n* `otk.rt1` - First attempt at ray tracing package. Superseded by otk.rt2.\n* `otk.rt2` - Ray tracing package with flexible geometry based on otk.sdb. See also `otk.rt2_scalar_qt`.\n* `otk.asbp` - Angular spectrum beam propagation.\n* `otk.abcd` - 1D ray transfer matrix ("ABCD matrices") tools.\n* `otk.rtm4` - abstractions for 1D ray transfer matrices, building upon `otk.abcd`.\n* `otk.pgb` - parabasal Gaussian routines for doing wave optical calculations with ray tracing results. Builds upon `otk.rt1`.\n* `otk.h4t` - homogeneous 4x4 transformation matrices.\n* `otk.paraxial` - basic paraxial optics calculations.\n* `otk.math` - various optics-specific math functions.\n* `otk.pov` - tools for generating POV-Ray scenes of optical setups.\n* `otk.pov` - for calculating properties of prisms.\n* `otk.qt` - Qt-related utilities\n* `otk.ri` - refractive index tools.\n* `otk.trains` - axially symmetric optical systems\n* `otk.v3` - operations on homogeneous vectors in 2D\n* `otk.v4` - operations on homogeneous vectors in 3D\n* `otk.v4b` - broadcasting operations on homogeneous vectors in 3D\n* `otk.zemax` - reading Zemax files\n\n## Folder contents\n\n* `otk` - the Python package itself.\n* `examples` - example scripts.\n* `properties` - material properties databases.\n* `notes` - miscellaneous notes including derivations.\n\n## Package management\n\notk uses [Poetry](https://python-poetry.org/) for package management. This means that dependencies, version, entry points etc are all defined in [`pyproject.toml`](./pyproject.toml). [`setup.py`](./setup.py) is generated using `dephell deps convert` to support pip development mode installation.\n\n### Using [PyPi test instance](test.pypi.org)\n\nTo setup, add test.pypi.org to your Poetry configuration with `poetry config repositories.test https://test.pypi.org/legacy/`. Note the [trailing slash](https://github.com/python-poetry/poetry/issues/742).\n\nTo publish (after `poetry build`), `poetry publish -r test`.\n\nTo test that it installs properly,\n1. create and activate a virtual environment, and\n2. per [instructions](https://packaging.python.org/guides/using-testpypi/), `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple otk`.\n\nHowever, I was unable to re-upload the same version (i.e. to correct a mistake) to test.pypi.org (even after logging in to the website and deleting the release).\n\n## Testing\n\nTest framework is [pytest](https://docs.pytest.org/en/latest/) and [tox](https://tox.readthedocs.io/en/latest/).\n\n## Contributing\n\nPlease do.\n',
    'author': 'Dane Austin',
    'author_email': 'dane_austin@fastmail.com.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/draustin/otk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
