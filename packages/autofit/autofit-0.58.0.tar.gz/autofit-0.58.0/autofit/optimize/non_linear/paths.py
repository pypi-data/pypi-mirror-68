import glob
import logging
import os
import shutil
import zipfile
from functools import wraps

from autofit import conf
from autofit.mapper import link

logger = logging.getLogger(__name__)


def make_path(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        full_path = func(*args, **kwargs)
        if not os.path.exists(full_path):
            try:
                os.makedirs(full_path)
            except FileExistsError:
                pass
        return full_path

    return wrapper


def convert_paths(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if len(args) > 1:
            raise AssertionError(
                "Only phase name is allowed to be a positional argument in a phase constructor"
            )

        first_arg = kwargs.pop("paths", None)
        if first_arg is None and len(args) == 1:
            first_arg = args[0]

        if isinstance(first_arg, Paths):
            return func(self, paths=first_arg, **kwargs)

        if first_arg is None:
            first_arg = kwargs.pop("phase_name", None)

        remove_files = conf.instance.general.get("output", "remove_files", bool)

        # TODO : Using the class nam avoids us needing to mak an sintance - still cant get the kwargs.get() to work
        # TODO : nicely though.

        non_linear_name = kwargs["non_linear_class"].__name__.lower() if "non_linear_class" in kwargs else ""

        func(
            self,
            paths=Paths(
                phase_name=first_arg,
                phase_tag=kwargs.pop("phase_tag", None),
                phase_folders=kwargs.pop("phase_folders", tuple()),
                phase_path=kwargs.pop("phase_path", None),
                non_linear_name=non_linear_name,
                remove_files=remove_files,
            ),
            **kwargs,
        )

    return wrapper


class Paths:
    def __init__(
            self,
            phase_name="",
            phase_tag=None,
            phase_folders=tuple(),
            phase_path=None,
            non_linear_name=None,
            remove_files=True,
    ):

        if not isinstance(phase_name, str):
            raise ValueError("Phase name must be a string")
        self.phase_path = phase_path or "/".join(phase_folders)
        self.phase_name = phase_name
        self.phase_tag = phase_tag or ""
        self.non_linear_name = non_linear_name or ""
        self.remove_files = remove_files

    @property
    def path(self):
        return link.make_linked_folder(self.sym_path)

    def __eq__(self, other):
        return isinstance(other, Paths) and all(
            [
                self.phase_path == other.phase_path,
                self.phase_name == other.phase_name,
                self.phase_tag == other.phase_tag,
                self.non_linear_name == other.non_linear_name,
            ]
        )

    @property
    def phase_folders(self):
        return self.phase_path.split("/")

    @property
    def samples_path(self) -> str:
        """
        The path to the samples folder.
        """
        return f"{self.phase_output_path}/samples"

    @property
    def backup_path(self) -> str:
        """
        The path to the backed up samples folder.
        """
        return f"{self.phase_output_path}/samples_backup"

    @property
    def zip_path(self) -> str:
        return f"{self.phase_output_path}.zip"

    @property
    @make_path
    def phase_output_path(self) -> str:
        """
        The path to the output information for a phase.
        """
        return "/".join(
            filter(
                len,
                [
                    conf.instance.output_path,
                    self.phase_path,
                    self.phase_name,
                    self.phase_tag,
                    self.non_linear_name,
                ],
            )
        )

    @property
    def has_completed_path(self) -> str:
        """
        A file indicating that a multinest search has been completed previously
        """
        return f"{self.phase_output_path}/.completed"

    @property
    def execution_time_path(self) -> str:
        """
        The path to the output information for a phase.
        """
        return "{}/execution_time".format(self.phase_name_folder)

    @property
    @make_path
    def phase_name_folder(self):
        return "/".join((conf.instance.output_path, self.phase_path, self.phase_name))

    @property
    def sym_path(self) -> str:
        return "{}/{}/{}/{}/{}/samples".format(
            conf.instance.output_path, self.phase_path, self.phase_name, self.phase_tag, self.non_linear_name
        )

    @property
    def file_param_names(self) -> str:
        return "{}/{}".format(self.path, self.non_linear_name + ".paramnames")

    @property
    def file_model_promises(self) -> str:
        return "{}/{}".format(self.phase_output_path, "model.promises")

    @property
    def file_model_info(self) -> str:
        return "{}/{}".format(self.phase_output_path, "model.info")

    @property
    @make_path
    def image_path(self) -> str:
        """
        The path to the directory in which images are stored.
        """
        return "{}/image/".format(self.phase_output_path)

    @property
    @make_path
    def pdf_path(self) -> str:
        """
        The path to the directory in which images are stored.
        """
        return "{}pdf/".format(self.image_path)

    @property
    @make_path
    def pickle_path(self) -> str:
        return f"{self.make_path()}/pickles"

    def make_non_linear_pickle_path(self) -> str:
        """
        Create the path at which the optimizer pickle should be saved
        """
        return f"{self.pickle_path}/non_linear.pickle"

    def make_model_pickle_path(self):
        """
        Create the path at which the model pickle should be saved
        """
        return f"{self.pickle_path}/model.pickle"

    @make_path
    def make_path(self) -> str:
        """
        Create the path to the folder at which the metadata should be saved
        """
        return "{}/{}/{}/{}/{}/".format(
            conf.instance.output_path, self.phase_path, self.phase_name, self.phase_tag, self.non_linear_name
        )

    # TODO : These should all be moved to the mult_nest.py ,module in a MultiNestPaths class. I dont know how t do this.

    @property
    def file_summary(self) -> str:
        return "{}/{}".format(self.backup_path, "multinestsummary.txt")

    @property
    def file_weighted_samples(self):
        return "{}/{}".format(self.backup_path, "multinest.txt")

    @property
    def file_phys_live(self) -> str:
        return "{}/{}".format(self.backup_path, "multinestphys_live.points")

    @property
    def file_resume(self) -> str:
        return "{}/{}".format(self.backup_path, "multinestresume.dat")

    @property
    def file_results(self):
        return "{}/{}".format(self.phase_output_path, "model.results")

    def backup(self):
        """
        Copy files from the sym-linked optimizer folder to the backup folder in the workspace.
        """
        try:
            shutil.rmtree(self.backup_path)
        except FileNotFoundError:
            pass

        try:
            shutil.copytree(self.sym_path, self.backup_path)
        except shutil.Error as e:
            logger.exception(e)

    def backup_zip_remove(self):
        """
        Copy files from the sym linked optimizer folder then remove the sym linked folder.
        """
        self.backup()
        self.zip()

        if self.remove_files:
            try:
                shutil.rmtree(self.path)
            except FileNotFoundError:
                pass

    def restore(self):
        """
        Copy files from the backup folder to the sym-linked optimizer folder.
        """

        self.restore_old_to_new()

        if os.path.exists(self.zip_path):
            with zipfile.ZipFile(self.zip_path, "r") as f:
                f.extractall(self.phase_output_path)

            os.remove(self.zip_path)

        if os.path.exists(self.backup_path):
            for file in glob.glob(self.backup_path + "/*"):
                shutil.copy(file, self.path)

    # TODO : DElete at some point in the future...

    def restore_old_to_new(self):
        """
        Copy files from the backup folder to the sym-linked optimizer folder.
        """

        old_path = "/".join(
            filter(
                len,
                [
                    conf.instance.output_path,
                    self.phase_path,
                    self.phase_name,
                    self.phase_tag,
                ],
            )
        )

        old_zip_path = old_path + ".zip"

        if os.path.exists(old_zip_path):
            with zipfile.ZipFile(old_zip_path, "r") as f:
                f.extractall(self.phase_output_path)

            if os.path.exists(self.phase_output_path + "/optimizer_backup"):
                os.rename(self.phase_output_path + "/optimizer_backup", self.phase_output_path + "/samples_backup")

            if os.path.exists(old_path + "/image"):
                shutil.rmtree(old_path + "/image")

            if os.path.exists(old_path + "/optimizer_backup"):
                shutil.rmtree(old_path + "/optimizer_backup")

            file_list = glob.glob(old_path + "/*.pickle")
            [os.remove(file) for file in file_list]

            file_list = glob.glob(old_path + "/*.results")
            [os.remove(file) for file in file_list]

            file_list = glob.glob(old_path + "/*.info")
            [os.remove(file) for file in file_list]

            if os.path.exists(old_path + "/metadata"):
                os.remove(old_path + "/metadata")

            if os.path.exists(old_path + "/output.log"):
                os.remove(old_path + "/output.log")

            os.remove(old_zip_path)

        else:
            return

        if os.path.exists(self.backup_path):
            for file in glob.glob(self.backup_path + "/*"):
                shutil.copy(file, self.path)

        file_list = glob.glob(self.phase_output_path + "/*.pickle")
        if len(file_list) > 0:
            [os.remove(file) for file in file_list]

    def zip(self):
        try:
            with zipfile.ZipFile(self.zip_path, "w", zipfile.ZIP_DEFLATED) as f:
                for root, dirs, files in os.walk(self.phase_output_path):
                    for file in files:
                        f.write(
                            os.path.join(root, file),
                            os.path.join(
                                root[len(self.phase_output_path):].lstrip("/"), file
                            ),
                        )

            if self.remove_files:
                shutil.rmtree(self.phase_output_path)

        except FileNotFoundError:
            pass
