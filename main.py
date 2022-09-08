import os
from pathlib import Path
from watchdog.observers import Observer

from resources.user_prompts import (
    start_watching_path,
    start_watching_what_path,
    check_vt_for_sha256_hash
)
from resources.hash_generator import Hash
from resources.utils import (
    create_logger,
    temp_file,
    my_event_handler,
    start_observer,
    stop_observer,
    get_envs
)
from resources.vt_check import VirusTotal

logger = create_logger()


def main(path_to_watch: str) -> None:
    observer = Observer()
    observer.schedule(event_handler=my_event_handler, path=path_to_watch, recursive=True)
    text_file = Path(temp_file)
    start_observer(observer)
    while True:
        # TODO: INTRODUCE A TIMEOUT FOR WAITING ON THE THREAD
        while observer.is_alive():
            if text_file.is_file() and not os.stat(temp_file).st_size == 0:
                logger.info("[+] File downloaded, stopping observer and progressing")
                stop_observer(observer)
                break
        logger.info("[!] Generating hashes for the downloaded file")
        hashes = Hash(text_file=temp_file)
        print(f' >> SHA256 -- {hashes.hash_sha256}')
        print(f' >> SHA1 -- {hashes.hash_sha1}')
        print(f' >> MD5 -- {hashes.hash_md5}')
        # see if user has set up API file in directory
        if get_envs():
            if check_vt_for_sha256_hash():
                logger.info("[!] Attempting to call Virus Total")
                vt = VirusTotal(
                    hash_sha256=hashes.hash_sha256,
                    api_endpoint=os.getenv('API_ENDPOINT'),
                    api_key=os.getenv('API_key'),
                    api_key_val=os.getenv('API_KEY_VAL')
                )
                if not vt.out_dict.get('error_code'):
                    print(f">> Virus Total Results:")
                    print(f" >>> Last Analysis Date:")
                    print(f"      {vt.out_dict.get('LastAnalysisDate')}")
                    print(f" >>> Last Analysis Stats:")
                    for k, v in vt.out_dict.get('LastAnalysisStats').items():
                        print(f"      {k} - {v}")
                else:
                    print(f">> Virus Total Scan Failed with error code:\n {vt.out_dict.get('error_code')}")
        break


if __name__ == '__main__':
    try:
        if start_watching_path():
            user_path = start_watching_what_path()
            logger.info("[!] Starting the watcher, to interrupt press 'CTRL+C'")
            main(path_to_watch=user_path)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
