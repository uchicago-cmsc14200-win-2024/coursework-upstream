"""
Module providing base classes for implementing validators,
as well as a couple of useful validators.

Examples:

    Creating a validator that checks whether a file
    exists:

        v = FileExistsValidator("/home/jrandom", "hello.tct")

    The `valid` property will tell us whether the check
    passed or not:

        if v.valid:
            print("File found!)

    If the check didn't pass, the `error_msg` property
    will provide a helpful error message:

        if not v.valid:
            print(v.error_msg)
"""
import re
import os.path
from abc import ABC, abstractmethod
from typing import Optional, Collection
from pathlib import Path

import git


class Validator(ABC):
    """
    Base class for a validator

    To implement a validator, you must implement the _validate
    method, which performs some sort of validation (see the
    _validate method for more details)

    Note that the _validate method will be called at the
    time the object is constructed.
    """

    _valid: Optional[bool]
    _error_msg: Optional[str]
    _hint: Optional[str]

    def __init__(
        self,
        hint: Optional[str] = None,
        depends: Optional[Collection["Validator"]] = None,
    ):
        """
        Constructor.

        Args:
            hint: An optional hint if the validation fails
            depends: Other Validator objects that this Validator
              depends on (the validator will run only if all
              the validators in "depends" pass)
        """
        self._valid = None
        self._error_msg = None
        self._hint = hint

        if depends is None or all(v.valid for v in depends):
            self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """
        Performs a validation task. The subclass must implement
        this method to perform a specific validation task,
        and must set the _valid and _error_msg attributes
        appropriately. The values of these attributes can
        be access with the valid and error_msg properties.

        Returns: None
        """
        raise NotImplementedError

    @property
    def valid(self) -> Optional[bool]:
        """Property for _valid"""
        return self._valid

    @property
    def error_msg(self) -> Optional[str]:
        """
        Returns an error message, and a hint if available.

        Returns: the error message
        """
        if self._hint is not None:
            return f"{self._error_msg}. {self._hint}"
        else:
            return self._error_msg


class FileValidator(Validator, ABC):
    """
    Base class for validators that relate to a specific file
    """

    _base_dir: Path
    _filename: str
    _path: Path

    def __init__(
        self,
        base_dir: Path,
        filename: str,
        hint: Optional[str] = None,
        depends: Optional[Collection["Validator"]] = None,
    ):
        """
        Constructor

        Args:
            base_dir: Base directory (not necessarily the directory
            the file is directly contained it)
            filename: Filename path (relative to the base directory
            hint: See Validator
            depends: See Validator
        """
        self._base_dir = base_dir
        self._filename = filename
        self._path = base_dir / filename
        super().__init__(hint, depends)


class FileExistsValidator(FileValidator):
    """
    Validator for checking whether a file exists
    """

    def _validate(self) -> None:
        """Validation method. See Validator for more details"""
        if not os.path.exists(self._path):
            self._valid = False
            self._error_msg = f"No such file: {self._filename}"
        else:
            self._valid = True


class FileDoesntContainValidator(FileValidator):
    """
    Validator for checking whether a file does not
    contain a given text
    """

    _text: str

    def __init__(
        self,
        base_dir: Path,
        filename: str,
        text: str,
        hint: Optional[str] = None,
        depends: Optional[Collection["Validator"]] = None,
    ):
        """
        Constructor

        Args:
            base_dir: See FileValidator
            filename: See FileValidator
            text: Text to check for
            hint: See Validator
            depends: See Validator
        """
        self._text = text
        super().__init__(base_dir, filename, hint, depends)

    def _validate(self) -> None:
        """Validation method. See Validator for more details"""
        with open(self._path) as f:
            f_txt = f.read()
            if self._text in f_txt:
                self._valid = False
                self._error_msg = (
                    f"{self._filename} " f"contains the text '{self._text}'"
                )
            else:
                self._valid = True


class FileContainsValidator(FileValidator):
    """
    Validator for checking whether a file contains a given
    text (with support for regular expressions)
    """

    _pattern: str
    _regex: bool
    _exact: bool

    def __init__(
        self,
        base_dir: Path,
        filename: str,
        pattern: str,
        regex: bool = False,
        exact: bool = False,
        hint: Optional[str] = None,
        depends: Optional[Collection["Validator"]] = None,
    ):
        """
        Constructor

        Args:
            base_dir: See FileValidator
            filename: See FileValidator
            pattern: Text to check for (or regular expression if regex
                parameter is True)
            regex: Specifies whether to interpret the pattern parameter
                as a regular expression.
            exact: Look for an exact match (i.e., the file must contain
                exactly the provided text, and nothing else, allowing for
                trailing newlines/space)
            hint: See Validator
            depends: See Validator
        """
        self._pattern = pattern
        self._regex = regex
        self._exact = exact
        super().__init__(base_dir, filename, hint, depends)

    def _validate(self) -> None:
        """Validation method. See Validator for more details"""
        with open(self._path) as f:
            f_txt = f.read()

            self._valid = True
            if self._exact:
                if f_txt.rstrip() != self._pattern:
                    self._error_msg = (
                        f"{self._filename} must contain "
                        f"exactly the following: '{self._pattern}'"
                    )
                    self._valid = False
            elif self._regex:
                s = re.search(self._pattern, f_txt)
                if s is None:
                    self._error_msg = (
                        f"{self._filename} does not have the expected contents"
                    )
                    self._valid = False
            else:
                if self._pattern not in f_txt:
                    self._error_msg = (
                        f"{self._filename} must contain "
                        f"the following: '{self._pattern}'"
                    )
                    self._valid = False


class GitRepoValidator(Validator):
    """
    Validator for checking a directory contains
    a Git repository
    """

    _repo_dir: Path

    def __init__(
        self,
        repo_dir: Path,
        hint: Optional[str] = None,
        depends: Optional[Collection["Validator"]] = None,
    ):
        """
        Constructor

        Args:
            repo_dir: Directory to check
            hint: See Validator
            depends: See Validator
        """

        self._repo_dir = repo_dir
        super().__init__(hint, depends)

    def _validate(self) -> None:
        """Validation method. See Validator for more details"""
        try:
            _ = git.Repo(self._repo_dir)
            self._valid = True
        except git.InvalidGitRepositoryError:
            self._valid = False
            self._error_message = f"This directory is not a Git repo: {self._repo_dir}"


class GitRepoFileValidator(Validator):
    """
    Validator for checking whether a Git repository contains
    a file (and that the file has no unstaged changes)
    """

    _repo: git.Repo
    _file_path: str

    def __init__(
        self,
        repo_dir: Path,
        file_path: str,
        hint: Optional[str] = None,
        depends: Optional[Collection["Validator"]] = None,
    ):
        """
        Constructor

        Args:
            repo_dir: Directory containing Git repository
            file_path: Path to file to check
            hint: See Validator
            depends: See Validator
        """
        self._repo = git.Repo(repo_dir)
        self._file_path = file_path
        super().__init__(hint, depends)

    def _validate(self) -> None:
        """Validation method. See Validator for more details"""
        self._valid = True
        try:
            _ = self._repo.tree() / self._file_path
            unstaged = [d.a_path for d in self._repo.index.diff(None)]
            if self._file_path in unstaged:
                self._valid = False
                self._error_msg = f"{self._file_path} exists but has unstaged changes"
        except KeyError:
            self._valid = False
            self._error_msg = f"No such file in Git repository: {self._file_path}"


class GitRepoRemoteValidator(Validator):
    """
    Validator for checking whether a Git repository
    has a given remote, and that it is (or isn't)
    associated with a given URL.
    """

    _repo: git.Repo
    _remote_name: str
    _remote_url: Optional[str]
    _check_url_equality: bool

    def __init__(
        self,
        repo_dir: Path,
        remote_name: str,
        remote_url: Optional[str] = None,
        check_url_equality: bool = True,
        hint: Optional[str] = None,
        depends: Optional[Collection["Validator"]] = None,
    ):
        """
        Constructor

        Args:
            repo_dir: Directory containing Git repository
            remote_name: Remote name to check
            remote_url: (optional) URL of remote
            check_url_equality: If True, check whether the remote is
                associated with `remote_url`. If False, check
                that the remote is NOT associated with `remote_url`
            hint: See Validator
            depends: See Validator
        """
        self._repo = git.Repo(repo_dir)
        self._remote_name = remote_name
        self._remote_url = remote_url
        self._check_url_equality = check_url_equality
        super().__init__(hint, depends)

    def _validate(self) -> None:
        """Validation method. See Validator for more details"""
        self._valid = True
        try:
            remote = self._repo.remote(self._remote_name)
            if self._remote_url is not None:
                if self._check_url_equality and remote.url != self._remote_url:
                    self._valid = False
                    self._error_msg = (
                        f"Expected remote '{self._remote_name}' to be "
                        f"{self._remote_url} but instead got {remote.url}"
                    )
                elif not self._check_url_equality and remote.url == self._remote_url:
                    self._valid = False
                    self._error_msg = f"Remote '{self._remote_name}' has an invalid value: {remote.url}"
        except ValueError:
            self._valid = False
            self._error_msg = f"Git is missing a(n) '{self._remote_name}' remote."
