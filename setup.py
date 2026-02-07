# -*- coding: utf-8 -*-

import subprocess
import sys
import os
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


class BuildPy(build_py):
    @staticmethod
    def build():
        build_script = Path("build.cmd")

        if not build_script.exists():
            print(f"Warning: Build script not found {build_script}")
            return True

        print(f"Executing build script: {build_script}")

        try:
            result = subprocess.run(
                [str(build_script)],
                shell=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )

            if result.returncode != 0:
                print(f"Build failed!")
                if result.stderr:
                    print(f"Error output:\n{result.stderr[:1000]}")
                return False
            else:
                print(f"Build successful!")
                if result.stdout and result.stdout.strip():
                    print(f"Output:\n{result.stdout[:500]}")
                return True

        except Exception as e:
            print(f"Error executing build script: {e}")
            return False

    def run(self):
        if not self.build():
            sys.exit(1)
        super().run()


def pyproject():
    try:
        return {
            "name":         "ak-memkit",
            "version":      "0.0.1",
            "author":       "AK",
            "author_email": "akpainkiller32767@gmail.com",
            "description":  "AK32767's mysterious memory reading toolkit",
            "license":      "MIT",
            "classifiers":  [
                "Development Status :: 3 - Alpha",
                "Intended Audience :: Developers",
                "Topic :: Software Development :: Libraries :: Python Modules",
                "Programming Language :: Python :: 3.12",
                "Programming Language :: Python :: 3.13",
                "Programming Language :: Python :: 3.14",
                "Operating System :: Microsoft :: Windows",
            ],


            "python_requires":  ">=3.12",
            "install_requires": [
                f"neac_controller @ git+https://github.com/AK-0x7FFF/NeacController.git",
                f"pyMeow @ git+https://github.com/AK-0x7FFF/pyMeow.git",

                "memprocfs>=5.14.0",
                "numpy",
                "numba",
                "scipy",
                "deprecated",
                "pybind11>=2.6.0",
                "winappdbg @ git+https://github.com/MarioVilas/winappdbg.git",
             ],
        }

    except Exception as e:
        print(f"Warning: Failed to read pyproject.toml: {e}")
        return {}


if __name__ == "__main__":
    pyproject = pyproject()

    setup(**{
        **{k: v for k, v in pyproject.items() if v is not None},
        **{
            "packages": [
                "ak_memkit"
            ],
            "package_dir": {
                "ak_memkit": "src/ak_memkit"
            },
            "package_data": {
                "ak_memkit": [
                    "*.py",
                    "memory/*.py"
                ]
            },
            "zip_safe": False,
        }
    })
