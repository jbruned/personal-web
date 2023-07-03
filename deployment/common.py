from hashlib import md5

VERBOSE_NONE = 0
VERBOSE_ERROR = 1
VERBOSE_WARNING = 2
VERBOSE_INFO = 3
VERBOSE_ALL = 4

def file_hash(file: str):
    """
    Get the hash of a file
    """
    with open(file, "rb") as f:
        return md5(f.read()).hexdigest()

def log(message: str, level: int = VERBOSE_INFO, verbose: int = VERBOSE_INFO, dry_run: bool = False, header: bool = False):
    """
    Log a message
    """
    if verbose >= level:
        prefix = f"{'dry' if dry_run else ''}> " if not header else ''
        print(f"{prefix}{message}")

def abort(message: str = None):
    """
    Abort the script
    """
    log(message, VERBOSE_ERROR, header=True)
    exit(1)
