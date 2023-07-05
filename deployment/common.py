from hashlib import md5
import os

# Verbose levels
VERBOSE_NONE = 0
VERBOSE_ERROR = 1
VERBOSE_WARNING = 2
VERBOSE_INFO = 3
VERBOSE_ALL = 4
LOG_LEVEL = VERBOSE_INFO

# Remote URLs
BLOG_URL = "blog"
SITEMAP_URL = "sitemap.xml"
INDEX_URL = "index.html"
STRINGS_URL = os.path.join("assets", "strings.js")
SCRIPT_URL = os.path.join("assets", "script.js")
STYLE_URL = os.path.join("assets", "style.css")

# Local directories
DEFAULT_BASE_PATH = ".."
POSTS_DIR_NAME = "posts"
TEMPLATES_DIR_NAME = "templates"
ASSETS_DIR_NAME = "assets"
PROJECTS_FILE_NAME = "projects.json"
SKILLS_FILE_NAME = "skills.json"

def file_hash(file: str):
    """
    Get the hash of a file
    """
    with open(file, "rb") as f:
        return md5(f.read()).hexdigest()

def log(message: str, level: int = VERBOSE_INFO, verbose: int = None, dry_run: bool = False, header: bool = False):
    """
    Log a message
    """
    if verbose if verbose is not None else LOG_LEVEL >= level:
        prefix = f"{'dry' if dry_run else ''}> " if not header else ''
        print(f"{prefix}{message}")

def get_log_level():
    """
    Get the log level
    """
    return LOG_LEVEL

def set_log_level(level: int):
    """
    Set the log level
    """
    global LOG_LEVEL
    LOG_LEVEL = level

def abort(message: str = None):
    """
    Abort the script
    """
    log(message, VERBOSE_ERROR, header=True)
    exit(1)
