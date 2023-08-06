#!/usr/bin/env python3

import os
import importlib
import subprocess
from setuptools import setup, find_packages
from distutils.command.build import build as build_orig
from setuptools.command.sdist import sdist as sdist_orig


STATIC_VERSION_PATH = ('kwantspectrum', '_kwant_spectrum_version.py')

distr_root = os.path.dirname(os.path.abspath(__file__))


# Get the long description from the README file.
with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


def check_versions():
    global version, version_is_from_git

    # Let kwantspectrum itself determine its own version.
    # We cannot simply import kwantspectrum, as it is not built yet.
    spec = importlib.util.spec_from_file_location('version', 'kwantspectrum/version.py')
    version_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version_module)

    version_module.ensure_python()
    version = version_module.version
    version_is_from_git = version_module.version_is_from_git


def write_version(fname):
    # This could be a hard link, so try to delete it first.  Is there any way
    # to do this atomically together with opening?
    try:
        os.remove(fname)
    except OSError:
        pass
    with open(fname, 'w') as f:
        f.write("# This file has been created by setup.py.\n")
        f.write("version = '{}'\n".format(version))


class build(build_orig):
    def run(self):
        super().run()
        write_version(os.path.join(self.build_lib, *STATIC_VERSION_PATH))


def git_lsfiles():
    if not version_is_from_git:
        return

    try:
        p = subprocess.Popen(['git', 'ls-files'], cwd=distr_root,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return

    if p.wait() != 0:
        return
    return p.communicate()[0].decode().split('\n')[:-1]


# Make the command "sdist" depend on "build".  This verifies that the
# distribution in the current state actually builds.  It also makes sure that
# the Cython-made C files will be up-to-date and included in the source.
class sdist(sdist_orig):
    sub_commands = [('build', None)] + sdist_orig.sub_commands

    def run(self):
        """Create MANIFEST.in from git if possible, otherwise check that
        MANIFEST.in is present.

        Right now (2015) generating MANIFEST.in seems to be the only way to
        include files in the source distribution that setuptools does not think
        should be there.  Setting include_package_data to True makes setuptools
        include *.pyx and other source files in the binary distribution.
        """
        manifest_in_file = 'MANIFEST.in'
        manifest = os.path.join(distr_root, manifest_in_file)
        names = git_lsfiles()
        if names is None:
            if not (os.path.isfile(manifest) and os.access(manifest, os.R_OK)):
                print("Error:", manifest_in_file,
                      "file is missing and Git is not available"
                      " to regenerate it.", file=sys.stderr)
                sys.exit(1)
        else:
            with open(manifest, 'w') as f:
                for name in names:
                    a, sep, b = name.rpartition('/')
                    if b == '.gitignore':
                        continue
                    stem, dot, extension = b.rpartition('.')
                    f.write('include {}'.format(name))
                    if extension == 'pyx':
                        f.write(''.join([' ', a, sep, stem, dot, 'c']))
                    f.write('\n')

        super().run()

        if names is None:
            msg = ("Git was not available to generate the list of files to be "
                   "included in the\nsource distribution. The old {} was used.")
            msg = msg.format(manifest_in_file)
            print(banner(' Caution '), msg, banner(), sep='\n', file=sys.stderr)

    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)
        write_version(os.path.join(base_dir, *STATIC_VERSION_PATH))


def main():

    check_versions()

    setup(
        name='kwantspectrum',
        version=version,
        description='Adaptive band structure analyzer for Kwant leads',
        long_description=long_description,
        url='https://gitlab.kwant-project.org/kwant/kwantspectrum',
        author='T. Kloss, C. W. Groth, X. Waintal, et al.',
        author_email='kloss@itp.uni-frankfurt.de',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',
            'Topic :: Software Development',
            'Topic :: Scientific/Engineering',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3 :: Only',
        ],
        keywords='physics kwant bandstructure',
        packages=find_packages('.'),
        cmdclass={'build': build,
                  'sdist': sdist},
        python_requires='>=3.5',
        install_requires=['kwant >= 1.4', 'numpy', 'scipy'],
        extras_require={'test': ['pytest', 'pytest-cov', 'pytest-flake8'], },
    )

if __name__ == '__main__':
    main()
