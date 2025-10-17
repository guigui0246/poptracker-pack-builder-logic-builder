import pip


def install_all(file: str) -> None:
    """Install all packages listed in a requirements file using pip."""
    pip.main(['install', '-r', file])


__all__ = ["install_all"]
