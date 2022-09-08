from dataclasses import dataclass, field
import hashlib


@dataclass
class Hash:
    """Data-oriented class"""
    text_file: str
    text_data: str = field(default_factory=str, init=False, repr=False)
    hash_sha256: str = field(default_factory=str, init=False, repr=False)
    hash_sha1: str = field(default_factory=str, init=False, repr=False)
    hash_md5: str = field(default_factory=str, init=False, repr=False)

    def __post_init__(self):
        with open(self.text_file) as f:
            self.text_data = f.read()
        self._generate_hashes()

    def _generate_hashes(self) -> None:
        BLOCK_SIZE = 65536  # The size of each read from the file
        sha_256 = hashlib.sha256()
        sha_1 = hashlib.sha1()
        md_5 = hashlib.md5()

        with open(self.text_data, 'rb') as f:  # Open the file to read its bytes
            fb = f.read(BLOCK_SIZE)  # Read from the file. Take in the amount declared above
            while len(fb) > 0:  # While there is still data being read from the file
                sha_256.update(fb)  # Update the hash
                sha_1.update(fb)
                md_5.update(fb)
                fb = f.read(BLOCK_SIZE)  # Read the next block from the file
        self.hash_sha256 = str(sha_256.hexdigest())
        self.hash_sha1 = str(sha_1.hexdigest())
        self.hash_md5 = str(md_5.hexdigest())
