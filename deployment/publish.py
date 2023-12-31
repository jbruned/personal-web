from base64 import decodebytes, encodebytes
import io
import os
import stat
import sys
from hashlib import md5
import pysftp
import dotenv

from common import VERBOSE_ALL, VERBOSE_INFO, VERBOSE_NONE, VERBOSE_WARNING, \
    POSTS_DIR_NAME, TEMPLATES_DIR_NAME, PROJECTS_FILE_NAME, SKILLS_FILE_NAME, \
    file_hash, log, set_log_level

DEFAULT_DEPLOYMENT_STATUS_FILE = "deployment_status.txt"

def publish(
    username: str,
    password: str,
    host: str,
    port: int = 22,
    public_key: str = None,
    remote_path: str = "/",
    local_path: str = ".",
    status_file: str = "status.txt",
    ignore: list = [],
    remove_unmatched: bool = False,
    dry_run: bool = True
):
    """
    Publish the files to the remote directory. Flags.
    - remove_unmatched: delete all files in the remote directory that are not in the local directory
    """
    assert username is not None, "No username provided"
    assert password is not None, "No password provided"
    assert host is not None, "No host provided"
    public_key = public_key.strip() if public_key is not None else ""
    cnopts = pysftp.CnOpts()
    for should_be_ignored in [
        POSTS_DIR_NAME, TEMPLATES_DIR_NAME, PROJECTS_FILE_NAME, SKILLS_FILE_NAME,
        'deployment', '.gitignore', '.git', 'README.md', '.github', status_file,
        'assets/fonts/jbruned-icons.json', 'LICENSE', 'makefile'
    ]:
        if should_be_ignored not in ignore:
            ignore.append(should_be_ignored)
    if public_key != "":
        # key_type, public_key = public_key.split(" ", maxsplit=1)
        # Temporary file to store the public key
        with open("temp.pub", "w") as f:
            f.write(f"{host} {public_key}")
        cnopts.hostkeys.load(f.name)
        os.remove("temp.pub")
    else:
        cnopts.hostkeys = None
        log("WARNING: No public key provided. This transfer is not secure against MITM attacks.",
            level=VERBOSE_WARNING)

    with pysftp.Connection(
        host,
        username=username,
        password=password,
        port=port,
        cnopts=cnopts
    ) as sftp:
        # Initialize
        init(sftp, remote_path, local_path, status_file)
        curr_status = get_status(status_file)
        new_status = {}

        # Fetch all file paths
        remote_files = get_all_remote_files(sftp, ignore=ignore)
        for file in list(curr_status.keys()):
            if file not in remote_files:
                curr_status.pop(file)            
        local_files = get_all_local_files(ignore=ignore)

        # Publish the files
        log(f"Publishing files...", dry_run=dry_run, header=True, level=VERBOSE_INFO)
        for file in remote_files.union(local_files):
            if is_ignored(file, ignore):
                log(f"Ignored {file} (it's in the ignore list).", dry_run=dry_run)
                continue
            if file in remote_files and file not in local_files:
                if remove_unmatched:
                    remove_file(sftp, file, dry_run=dry_run)
                elif file in curr_status:
                    raise Exception(f"File {file} is in the remote status but not in the local directory. "
                                    "Use the --remove_unmatched flag if you wish to continue.")
                # else:
                #     log(f"Skipped {file} (it's in the remote directory but not in the status file).",
                #         dry_run=dry_run)
                continue
            published_hash = curr_status.get(file) if file in curr_status else None
            local_hash = file_hash(file)
            new_status[file] = local_hash
            if published_hash != local_hash:
                upload_file(sftp, file, dry_run=dry_run)
            else:
                log(f"Already up to date: {file}", dry_run=dry_run)

        # Warn if the status file is not forbidden
        if '.htaccess' not in local_files or not file_contains('.htaccess', status_file):
            log("WARNING: The status file is not forbidden from being accessed. This is a security risk.",
                level=VERBOSE_WARNING)

        # Update the status file
        with open(status_file, "w") as f:
            f.write("\n".join([
                f"{filename} {hash}"
                for filename, hash in new_status.items()
            ]))
        upload_file(sftp, status_file, dry_run=dry_run)
        os.remove(status_file)
    log("Done publishing!", dry_run=dry_run, header=True)

def init(sftp, remote_path, local_path, status_file):
    """
    Go to the root directories and initialize the status file if it doesn't exist
    """
    sftp.chdir(remote_path)
    os.chdir(local_path)
    if status_file in sftp.listdir():
        sftp.get(status_file)
    else:
        with open(status_file, "w") as f:
            f.write("")

def get_status(status_file):
    """
    Get the hashes of the files from the remote directory
    Returns a dictionary of filename: hash
    """
    with open(status_file, "r") as f:
        status = f.read()
        lines = status.split("\n")
        return {
            filename: hash
            for filename, hash in map(
                lambda line: tuple(line.split(" ", maxsplit=1)),
                filter(lambda line: line != "", lines)
            )
        }

def get_all_remote_files(sftp, relative_path: str = None, first_call: bool = True, ignore: list = []):
    """
    Get all files from the remote directory, recursively
    """
    if first_call:
        log(f"Indexing remote files...", header=True)
    all_files = set()
    for file in sftp.listdir_attr():
        path = (f"{relative_path}/" if relative_path is not None else '') + file.filename
        if is_ignored(path, ignore):
            log(f"Ignored {path} (it's in the ignore list).", level=VERBOSE_WARNING)
            continue
        if stat.S_ISDIR(file.st_mode):
            sftp.chdir(file.filename)
            if first_call:
                log(f"Listing {file.filename}", level=VERBOSE_INFO)
            all_files.update(
                get_all_remote_files(sftp, relative_path=path, first_call=False)
            )
            sftp.chdir("..")
        else:
            all_files.add(path)
    return all_files

def get_all_local_files(local_path: str = None, first_call: bool = True, ignore: list = []):
    """
    Get all files from the local directory, recursively
    """
    if first_call:
        log(f"Indexing local files...", header=True)
    all_files = set()
    for file in os.listdir(local_path if local_path is not None else '.'):
        path = (f"{local_path}/" if local_path is not None else '') + file
        if is_ignored(path, ignore):
            log(f"Ignored {path} (it's in the ignore list).", level=VERBOSE_WARNING)
            continue
        if os.path.isdir(path):
            if first_call:
                log(f"Listing {file}", level=VERBOSE_INFO)
            all_files.update(
                get_all_local_files(path, first_call=False)
            )
        else:
            all_files.add(path)
    return all_files

def upload_file(sftp, file: str, dry_run: bool = False):
    """
    Upload a file to the remote directory
    """
    # Create the directories if they don't exist
    if not sftp.exists(os.path.dirname(file)):
        sftp.makedirs(os.path.dirname(file))
    # Upload the file
    already_existed = sftp.exists(file)
    if not dry_run:
        sftp.put(file, file)
    log(f"{'Updated' if already_existed else 'Created'} {file}", dry_run=dry_run)

def remove_file(sftp, file: str, dry_run: bool = False):
    """
    Remove a file from the remote directory
    """
    if not dry_run:
        sftp.remove(file)
    log(f"Deleted {file}", dry_run=dry_run)

def is_ignored(file: str, ignore: list):
    """
    Check if a file is in the ignore list
    """
    for ignored in ignore:
        if file.startswith(ignored):
            return True
    return False

def file_contains(file: str, string: str):
    """
    Check if a file contains a string
    """
    with open(file, "r") as f:
        return string in f.read()

if __name__ == '__main__':
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python publish.py [-f | --remove_unmatched] [-d | --dry_run] "
              "[-v | --verbose] [-vv | --verbose_all] [-h | --help]")
        exit(0)
    if ".env" in os.listdir():
        dotenv.load_dotenv()
    dry_run = "--dry_run" in sys.argv or "-d" in sys.argv
    verbose_level = VERBOSE_NONE
    if "--verbose" in sys.argv or "-v" in sys.argv:
        verbose_level = VERBOSE_INFO
    if "--verbose_all" in sys.argv or "-vv" in sys.argv:
        verbose_level = VERBOSE_ALL
    set_log_level(verbose_level)
    log(f"Publishing...{' (dry run)' if dry_run else ''}", header=True)
    publish(
        username=os.getenv("FTP_USER"),
        password=os.getenv("FTP_PASS"),
        host=os.getenv("FTP_HOST"),
        port=int(os.getenv("FTP_PORT", 22)),
        public_key=os.getenv("FTP_PUBKEY"),
        remote_path=os.getenv("FTP_PATH", "/"),
        local_path=os.getenv("LOCAL_PATH", ".."),
        status_file=os.getenv("STATUS_FILE", DEFAULT_DEPLOYMENT_STATUS_FILE),
        ignore=os.getenv("IGNORED_PATHS", "").split(","),
        remove_unmatched="--remove_unmatched" in sys.argv or "-f" in sys.argv,
        dry_run=dry_run
    )
