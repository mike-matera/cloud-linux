"""
Some helpful validators
"""

import grp
from pathlib import Path
import pwd
import re
from textual.validation import ValidationResult, Validator


class ExistingPath(Validator):
    """A path that must exist."""

    def validate(self, value: str) -> ValidationResult:
        p = Path(value.strip())
        if p.exists():
            return self.success()
        else:
            return self.failure(f"The path '{value}' does not exist.")


class AbsolutePath(Validator):
    """A path that must be absolute."""

    def validate(self, value: str) -> ValidationResult:
        p = Path(value.strip())
        if p.is_absolute():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not an absolute path.")


class RelativePath(Validator):
    """A path that must be relative."""

    def validate(self, value: str) -> ValidationResult:
        p = Path(value.strip())
        if p.is_absolute():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a relative path.")


class PathIsDir(Validator):
    """A path that must be a directory."""

    def validate(self, value: str) -> ValidationResult:
        p = Path(value.strip())
        if p.exists() and not p.is_symlink() and p.is_dir():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a directory.")


class PathIsFile(Validator):
    """A path that must be a file."""

    def validate(self, value: str) -> ValidationResult:
        p = Path(value.strip())
        if p.exists() and not p.is_symlink() and p.is_file():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a file.")


class PathIsSymlink(Validator):
    """A path that must be a symbolic link."""

    def validate(self, value: str) -> ValidationResult:
        p = Path(value.strip())
        if p.exists() and p.is_symlink():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a symbolic link.")


class IsUser(Validator):
    """Check for a valid username"""

    def validate(self, value: str) -> ValidationResult:
        try:
            pwd.getpwnam(value)
            return self.success()
        except KeyError:
            return self.failure(f"There is no user named {value}")


class IsGroup(Validator):
    """Check for a valid group name"""

    def validate(self, value: str) -> ValidationResult:
        try:
            grp.getgrnam(value)
            return self.success()
        except KeyError:
            return self.failure(f"There is no group named {value}")


class IsPermission(Validator):
    """Check for a mode string."""

    @staticmethod
    def from_string(value: str) -> int:
        if (
            m := re.match(
                r"[-dlbcsp]?([-r][-w][-x])([-r][-w][-x])([-r][-w][-x])",
                value,
            )
        ) is not None:
            trans = str.maketrans("-rwx", "0111")
            return int(
                "".join([x.translate(trans) for x in m.groups()]), base=2
            )

        permvalue = int(value, base=8)
        if 0 <= permvalue <= 0o777:
            return permvalue
        else:
            raise ValueError("Invalid permission string.")

    def validate(self, value: str) -> ValidationResult:
        try:
            IsPermission.from_string(value)
            return self.success()
        except ValueError:
            return self.failure(
                "Invalid permission value. Valid examples look like 644 or '-rwxr--r--'"
            )
