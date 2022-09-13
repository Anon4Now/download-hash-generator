"""Module containing tests for the Hash generator class"""

# Standard Library imports
import os

# Local App imports
from resources import hash_generator


def test_hash_class() -> None:
    """
    Function to test the Hash class and make sure the hashes generated are accurate.
    Will test SHA256, SHA1, and MD5 hash accuracy
    :return: None
    """
    # Create/Write to a file to emulate the temp_file being created by the script
    with open("test_file_path.txt", 'w+') as f:  # create "event" file
        f.write("test_file_read.txt")  # write the path to another "downloaded file" in it
        f.seek(0)  # seek back to index 0 to read what was written in the file
        data = f.read()  # put the written file name "test_file_read.txt" in a var

    # Write data to the "downloaded file" for the class to hash
    with open(data, "w") as f1:  # open the file in write mode
        f1.write("Hello World")  # write the string to the file to be hashed

    # Instantiate the object
    hashing = hash_generator.Hash(text_file="test_file_path.txt")
    # Test that the file "test_file_read.txt" with "Hello World" will hash correctly
    assert hashing.hash_sha256 == 'A591A6D40BF420404A011733CFB7B190D62C65BF0BCDA32B57B277D9AD9F146E'.lower()
    assert hashing.hash_sha1 == '0A4D55A8D778E5022FAB701977C5D840BBC486D0'.lower()
    assert hashing.hash_md5 == 'B10A8DB164E0754105B7A99BE72E3FE5'.lower()

    # Remove the test files from dir
    if os.path.exists("test_file_path.txt"):
        os.remove("test_file_path.txt")
    if os.path.exists("test_file_read.txt"):
        os.remove("test_file_read.txt")
