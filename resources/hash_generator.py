"""Module containing the class and methods for creating the hashes"""

# Standard Library imports
from dataclasses import dataclass, field
import hashlib

# Local App imports
from resources.utils import error_handler


@dataclass
class Hash:
    """Data-oriented class that generates and stores the
    SHA256, SHA1, and MD5 hash for the downloaded file.
    :param text_file: (required) this is the name of the auto-generated file in the script dir that containing the
    path info for the downloaded file. (e.g. 'C:/example_folder/downloaded_file.txt')
    """
    text_file: str
    text_data: str = field(default_factory=str, init=False, repr=False)
    hash_sha256: str = field(default_factory=str, init=False, repr=False)
    hash_sha1: str = field(default_factory=str, init=False, repr=False)
    hash_md5: str = field(default_factory=str, init=False, repr=False)

    @error_handler
    def __post_init__(self) -> None:
        """
        This post init does two things:
        1. It will open the passed param file and retrieve the file path. (e.g. 'C:/example_folder/downloaded_file.txt')
        2. It will call the _generate_hashes method to open the downloaded file at the param path and gen hashes
        :return: None
        """
        try:
            with open(self.text_file) as f:
                self.text_data = f.read()
        except FileNotFoundError:
            raise

        self._generate_hashes()

    @error_handler
    def _generate_hashes(self) -> None:
        """
        This method will set the buffer size to read from the downloaded file, open the file
        and read in the content while the length remaining of the file is not zero. This
        data is used to generate the hashes and updates the instance attrs.
        :return: None
        """
        BLOCK_SIZE = 65536  # The size of each read from the file
        sha_256 = hashlib.sha256()
        sha_1 = hashlib.sha1()
        md_5 = hashlib.md5()
        try:
            with open(self.text_data, 'rb') as f:  # Open the file to read its bytes
                fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
                while len(fb) > 0:  # While there is still data being read from the file
                    sha_256.update(fb)  # Update the hash
                    sha_1.update(fb)
                    md_5.update(fb)
                    fb = f.read(BLOCK_SIZE)  # Read the next block from the file
        except FileNotFoundError:
            raise
        else:
            self.hash_sha256 = str(sha_256.hexdigest())
            self.hash_sha1 = str(sha_1.hexdigest())
            self.hash_md5 = str(md_5.hexdigest())
