<!--
  THIS FILE IS EXCLUSIVELY MAINTAINED IN THE NAMESPACE ROOT PACKAGE. CHANGES HAVE TO BE DONE THERE.
  All changes will be deployed automatically to all the portions of this namespace package.
-->
# enaml_app portion of ae namespace package

[![GitLabPipeline](https://img.shields.io/gitlab/pipeline/ae-group/ae_enaml_app/master?logo=python)](
    https://gitlab.com/ae-group/ae_enaml_app)
[![PyPIVersion](https://img.shields.io/pypi/v/ae_enaml_app)](
    https://pypi.org/project/ae-enaml-app/#history)

>The portions (modules and sub-packages) of the Application Environment for Python are within
the `ae` namespace and are providing helper methods and classes for to develop
full-featured applications with Python.

[![Coverage](https://ae-group.gitlab.io/ae_enaml_app/coverage.svg)](
    https://ae-group.gitlab.io/ae_enaml_app/coverage/ae_enaml_app_py.html)
[![MyPyPrecision](https://ae-group.gitlab.io/ae_enaml_app/mypy.svg)](
    https://ae-group.gitlab.io/ae_enaml_app/lineprecision.txt)
[![PyLintScore](https://ae-group.gitlab.io/ae_enaml_app/pylint.svg)](
    https://ae-group.gitlab.io/ae_enaml_app/pylint.log)

[![PyPIImplementation](https://img.shields.io/pypi/implementation/ae_enaml_app)](
    https://pypi.org/project/ae-enaml-app/)
[![PyPIPyVersions](https://img.shields.io/pypi/pyversions/ae_enaml_app)](
    https://pypi.org/project/ae-enaml-app/)
[![PyPIWheel](https://img.shields.io/pypi/wheel/ae_enaml_app)](
    https://pypi.org/project/ae-enaml-app/)
[![PyPIFormat](https://img.shields.io/pypi/format/ae_enaml_app)](
    https://pypi.org/project/ae-enaml-app/)
[![PyPIStatus](https://img.shields.io/pypi/status/ae_enaml_app)](
    https://libraries.io/pypi/ae-enaml-app)
[![PyPIDownloads](https://img.shields.io/pypi/dm/ae_enaml_app)](
    https://pypi.org/project/ae-enaml-app/#files)


## installation


Execute the following command for to use the ae.enaml_app sub-package in your
application. It will install ae.enaml_app into your python (virtual) environment:
 
```shell script
pip install ae-enaml-app
```

If you instead want to contribute to this portion then first fork
[the ae_enaml_app repository at GitLab](https://gitlab.com/ae-group/ae_enaml_app "ae.enaml_app code repository"),
then pull it to your machine and finally execute the following command in the root folder
of this repository (ae_enaml_app):

```shell script
pip install -e .[dev]
```

The last command will install this sub-package portion into your virtual environment, along with
the tools you need to develop and run tests or for to extend the portion documentation.
For to contribute only to the unit tests or the documentation of this portion replace
the setup extras key `dev` in the above command with `tests` or `docs` respectively.


## namespace portion documentation

More info on the features and usage of this portion are available at
[ReadTheDocs](https://ae.readthedocs.io/en/latest/_autosummary/ae.enaml_app.html#module-ae.enaml_app
"ae_enaml_app documentation").

<!-- Common files version 0.0.48 deployed  version 0.0.1 (with 0.0.48)
     to https://gitlab.com/ae-group as ae_enaml_app sub-package as well as
     to https://ae-group.gitlab.io with CI check results as well as
     to https://pypi.org/project as ae-enaml-app package.
-->