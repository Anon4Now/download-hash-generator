"""Module containing tests for the Hash generator class"""

# Standard Library imports
import os

# Local App imports
from resources import hash_generator


def test_hash_class() -> None:
    #  Create/Write to a file to emulate the temp_file being created by the script
    with open("test_file_path.txt", 'w+') as f:
        f.write("test_file_read.txt")
        f.seek(0)
        data = f.read()

    with open(data, "w") as f1:
        f1.write("Hello World")

    hashing = hash_generator.Hash(text_file="test_file_path.txt")
    assert hashing.hash_sha256 == 'A591A6D40BF420404A011733CFB7B190D62C65BF0BCDA32B57B277D9AD9F146E'.lower()

    if os.path.exists("test_file_path.txt"):
        os.remove("test_file_path.txt")
    if os.path.exists("test_file_read.txt"):
        os.remove("test_file_read.txt")
