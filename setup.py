# setup.py
import subprocess
import sys
import os
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


class BuildCommand:
    @staticmethod
    def run_build_script():
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
                if result.stdout.strip():
                    print(f"Output:\n{result.stdout[:500]}")
                return True

        except Exception as e:
            print(f"Error executing build script: {e}")
            return False


class CustomBuildPy(build_py, BuildCommand):
    def run(self):
        if not self.run_build_script():
            sys.exit(1)
        super().run()


class CustomDevelop(develop, BuildCommand):
    def run(self):
        if not self.run_build_script():
            sys.exit(1)
        super().run()


class CustomEggInfo(egg_info, BuildCommand):
    def run(self):
        if not self.run_build_script():
            sys.exit(1)
        super().run()


# Package configuration
PACKAGES = [
    "NeacController",
    "pyMeow",
    "ak_memkit"
]

PACKAGE_DIR = {
    "": ".",
    "NeacController": "libs/NeacController/NeacController",
    "pyMeow": "libs/pyMeow",
    "ak_memkit": "src/ak_memkit"
}

PACKAGE_DATA = {
    "*": ["*.pyd"],
}


# Read metadata from pyproject.toml
def read_pyproject_metadata():
    try:
        import tomllib
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)

        project = data.get("project", {})

        metadata = {
            "name":                          project.get("name", "ak-memkit"),
            "version":                       project.get("version", "0.0.1"),
            "author":                        project.get("authors", [{}])[0].get("name", ""),
            "author_email":                  project.get("authors", [{}])[0].get("email", ""),
            "description":                   project.get("description", ""),
            "long_description":              open("README.md").read() if os.path.exists("README.md") else "",
            "long_description_content_type": "text/markdown",
            "url":                           project.get("urls", {}).get("Homepage", ""),
            "license":                       project.get("license", {}).get("text", "MIT"),
            "classifiers":                   project.get("classifiers", []),
            "python_requires":               project.get("requires-python", ">=3.12"),
            "install_requires":              project.get("dependencies", []),
        }

        return metadata
    except Exception as e:
        print(f"Warning: Failed to read pyproject.toml: {e}")
        return {}


if __name__ == "__main__":
    # Read metadata
    metadata = read_pyproject_metadata()

    # Setup arguments
    setup_kwargs = {
        # Basic package configuration
        "packages": PACKAGES,
        "package_dir": PACKAGE_DIR,
        "include_package_data": True,
        "package_data": PACKAGE_DATA,

        # Custom commands
        "cmdclass": {
            "build_py": CustomBuildPy,
            "develop": CustomDevelop,
            "egg_info": CustomEggInfo,
        },

        # Metadata from pyproject.toml
        "name": metadata.get("name", "ak-memkit"),
        "version": metadata.get("version", "0.0.1"),
        "author": metadata.get("author", "AK"),
        "author_email": metadata.get("author_email", "akpainkiller32767@gmail.com"),
        "description": metadata.get("description", "AK32767's mysterious memory reading toolkit"),
        "long_description": metadata.get("long_description", ""),
        "long_description_content_type": metadata.get("long_description_content_type"),
        "url": metadata.get("url", ""),
        "license": metadata.get("license", "MIT"),
        "classifiers": metadata.get("classifiers", []),
        "python_requires": metadata.get("python_requires", ">=3.12"),
        "install_requires": metadata.get("install_requires", []),

        # Other configuration
        "zip_safe": False,
    }

    # Clean None values
    setup_kwargs = {k: v for k, v in setup_kwargs.items() if v is not None}

    # Call setup
    setup(**setup_kwargs)