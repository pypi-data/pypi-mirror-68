"""Contains classes and functions designed to improve the ease of using the file system for experiments.
"""

import os
from os import path
from pickle import Pickler, Unpickler


class FilePipeline():
    """An object to help saving and loading multiple stages of a data pipeline automatically.
    """

    def __init__(self, directory, file_type='pkl', files=()):
        """Create a file pipeline instance that saves a particular type of file to a specified base directory.

        Args:
            directory (str): The base directory to save and load files from.
            to (str, optional): The file type to save. Defaults to ``'pkl'``.
            files (tuple, optional): An iterable containing the names of required values at every stage. Defaults to
                ``()``.
        """

        # Store the parameters.
        self.directory = directory
        self.file_type = file_type
        self.files = files

        # Store a reference to the current stage.
        self.__stage_name = None
        self.__stage_files = ()

        # Create an object to store values from files.
        self.values = {}

    def __getitem__(self, index):
        """Get an item from the pipeline values by index.

        Args:
            index (int): The index of the value.

        Returns:
            object: The value at the specified index.
        """

        return self.values[index]

    def __setitem__(self, index, value):
        """Set an item in the pipeline values by index.

        Args:
            index (int): The index of the value.
            value (object): The value to set at the specified index.
        """

        self.values[index] = value

    def __save_file(self, value, file_path):
        """Save a file for the pipeline.

        Args:
            value (object): The value to save to file.
            file_path (str): The path to the file to save.

        Raises:
            NotImplementedError: If the data type specified by the user is not supported.
        """

        # We need to make sure parent directories are created.
        os.makedirs(path.dirname(file_path), exist_ok=True)

        # Handle pickle type files.
        if self.file_type == 'pkl':
            with open(file_path, 'wb') as file:
                pkler = Pickler(file)
                pkler.dump(value)
            return

        # Raise error if unknown file type.
        raise NotImplementedError(
            f"Support for file type {self.file_type} is not implemented.")

    def __load_file(self, file_path):
        """Load a file for the pipeline.

        Args:
            file_path (str): The path to the file to load.

        Raises:
            NotImplementedError: If the data type specified by the user is not supported.

        Returns:
            object: The value loaded from the file.
        """

        # Handle pickle type files.
        if self.file_type == 'pkl':
            with open(file_path, 'rb') as file:
                unpkler = Unpickler(file)
                return unpkler.load()

        # Raise error if unknown file type.
        raise NotImplementedError(
            f"Support for file type {self.file_type} is not implemented.")

    def stage(self, name, overwrite=False, files=(), ignore_missing=False):
        """
        Start a stage for data processing loading in already existing data and specifying whether data needs to be
        computed. Automatically close previous pipeline stage if possible.

        Args:
            name (str): The name of the stage/subdirectory to store values in.
            overwrite (bool, optional): Whether values in the stage should be overwritten. Defaults to ``False``.
            files (tuple, optional): An iterable containing the names of additional files required at this stage.
                Defaults to ``()``.
            ignore_missing (bool, optional): Whether the the pipeline should ignore when required values are not set by
                the user. Otherwise, will raise an error. Defaults to ``False``.

        Returns:
            bool: Whether the stage needs to be recomputed.
        """

        # If a previous stage was in progress,
        # save its contents and then continue.
        self.end(ignore_missing=ignore_missing)

        # Store current stage.
        self.__stage_name = name
        self.__stage_files = files

        # If no files are specified, then, just check
        # if the directory exists.
        if not self.files and not files:
            already_staged = path.isdir(path.join(self.directory, name))
        # If files are specified, then, check if each
        # file in the directory exists.
        else:
            already_staged = True
            required_files = tuple(self.files) + tuple(files)
            for required_file in required_files:
                if not path.isfile(path.join(self.directory, name, f"{required_file}.{self.file_type}")):
                    already_staged = False
                    break

        # If the directory exists and all files are present,
        # then, load the directory and its values into the instance.
        if already_staged and not overwrite:
            for required_file in required_files:
                self.values[required_file] = self.__load_file(
                    path.join(self.directory, name, f"{required_file}.{self.file_type}"))

                # Otherwise, let the user create the proper values.
        return not already_staged or overwrite

    def end(self, ignore_missing=False):
        """End a stage for data processing by saving all required files for the stage.

        Args:
            ignore_missing (bool, optional): Whether the the pipeline should ignore when required values are not set by
                the user. Otherwise, will raise an error. Defaults to ``False``.

        Raises:
            KeyError: When a required value is missing and `ignore_missing` is set to False.
        """

        # If there was an in progress stage,
        # save all of its files.
        if self.__stage_name:
            required_files = tuple(self.files) + tuple(self.__stage_files)
            for required_file in required_files:
                try:
                    value = self.values[required_file]
                    self.__save_file(value, path.join(
                        self.directory, self.__stage_name, f"{required_file}.{self.file_type}"))
                except KeyError:
                    if not ignore_missing:
                        raise KeyError(
                            f"Value {required_file} expected but missing.")

        # Reset stored stage.
        self.__stage_name = None
        self.__stage_files = ()
