"""
Some helpful validators
"""

import grp
import pwd
import re
from pathlib import Path

from textual.validation import ValidationResult, Validator


class NotEmpty(Validator):
    """A non empty text field."""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The answer cannot be empty.")
        else:
            return self.success()


class ExistingPath(Validator):
    """A path that must exist."""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The path cannot be empty.")
        p = Path(value.strip())
        if p.exists():
            return self.success()
        else:
            return self.failure(f"The path '{value}' does not exist.")


class AbsolutePath(Validator):
    """A path that must be absolute."""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The path cannot be empty.")
        p = Path(value.strip())
        if p.is_absolute():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not an absolute path.")


class RelativePath(Validator):
    """A path that must be relative."""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The path cannot be empty.")
        p = Path(value.strip())
        if not p.is_absolute():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a relative path.")


class PathIsDir(Validator):
    """A path that must be a directory."""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The path cannot be empty.")
        p = Path(value.strip())
        if p.exists() and not p.is_symlink() and p.is_dir():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a directory.")


class PathIsFile(Validator):
    """A path that must be a file."""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The file name cannot be empty.")
        p = Path(value.strip())
        if p.exists() and not p.is_symlink() and p.is_file():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a file.")


class PathIsSymlink(Validator):
    """A path that must be a symbolic link."""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The link name cannot be empty.")
        p = Path(value.strip())
        if p.exists() and p.is_symlink():
            return self.success()
        else:
            return self.failure(f"The path '{value}' is not a symbolic link.")


class IsUser(Validator):
    """Check for a valid username"""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The user name cannot be empty.")
        try:
            pwd.getpwnam(value)
            return self.success()
        except KeyError:
            return self.failure(f"There is no user named {value}")


class IsGroup(Validator):
    """Check for a valid group name"""

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The group name cannot be empty.")
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

    @staticmethod
    def to_string(value: int) -> str:
        rval = ""
        bit = 0o1000
        letters = ["r", "w", "x"]
        letter = 0
        while (bit := bit >> 1) != 0:
            if value & bit:
                rval += letters[letter]
            else:
                rval += "-"
            letter = (letter + 1) % len(letters)
        return rval

    def validate(self, value: str) -> ValidationResult:
        if not value:
            return self.failure("The answer cannot be empty.")
        try:
            IsPermission.from_string(value)
            return self.success()
        except ValueError:
            return self.failure(
                "Invalid permission value. Valid examples look like 644 or '-rwxr--r--'"
            )
