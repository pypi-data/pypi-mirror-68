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
        name = 'Concern',
        version = '13',
        description = 'Control FoxDot or pym2149 using Vim',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/Concern',
        author = 'Andrzej Cichocki',
        packages = packages,
        py_modules = ['concern'],
        install_requires = ['aridity', 'lagoon', 'timelyOSC'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        scripts = [],
        entry_points = {'console_scripts': ['Concern=concern:main_Concern']},
        **ext_modules())
