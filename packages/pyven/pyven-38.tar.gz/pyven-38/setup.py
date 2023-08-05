import os, setuptools

def long_description():
    with open('README.md') as f:
        return f.read()

packages = setuptools.find_packages()

def ext_modules():
    def g():
        suffix = '.pyx'
        for package in packages:
            dirpath = package.replace('.', os.sep)
            for name in os.listdir(dirpath):
                if name.endswith(suffix):
                    path = os.path.join(dirpath, name)
                    g = {}
                    with open(path + 'bld') as f:
                        exec(f.read(), g)
                    yield g['make_ext'](package + '.' + name[:-len(suffix)], path)
    paths = list(g())
    if paths:
        # XXX: Can cythonize be deferred?
        from Cython.Build import cythonize
        return dict(ext_modules = cythonize(paths))
    return {}

setuptools.setup(
        name = 'pyven',
        version = '38',
        description = 'Manage development of multiple Python projects',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/pyven',
        author = 'Andrzej Cichocki',
        packages = packages,
        py_modules = ['pkg_resources_lite'],
        install_requires = ['aridity', 'lagoon', 'nose-cov', 'pyflakes', 'twine', 'virtualenv'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        scripts = ['bootstrap', 'foreignsyms'],
        entry_points = {'console_scripts': ['checks=pyven.checks:main_checks', 'tests=pyven.checks:main_tests', 'gclean=pyven.gclean:main_gclean', 'initopt=pyven.initopt:main_initopt', 'pipify=pyven.pipify:main_pipify', 'release=pyven.release:main_release', 'tasks=pyven.tasks:main_tasks', 'travis_ci=pyven.travis_ci:main_travis_ci']},
        **ext_modules())
