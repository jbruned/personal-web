import glob
import os
from shutil import rmtree
from sys import argv

from common import log, INDEX_URL, BLOG_URL, SITEMAP_URL, STRINGS_URL, ASSETS_DIR_NAME

if __name__ == "__main__":
    BASE_PATH = argv[1] if len(argv) > 1 else ".."
    log("Removing generated files...", header=True)
    for file in [
        os.path.join(BASE_PATH, INDEX_URL),
        os.path.join(BASE_PATH, f"{BLOG_URL}.html"),
        os.path.join(BASE_PATH, SITEMAP_URL),
        os.path.join(BASE_PATH, STRINGS_URL),
        os.path.join(BASE_PATH, BLOG_URL),
        os.path.join(BASE_PATH, ASSETS_DIR_NAME, "fonts", "*.woff2"),
        os.path.join(BASE_PATH, ASSETS_DIR_NAME, "fonts", "*.woff"),
        os.path.join(BASE_PATH, ASSETS_DIR_NAME, "fonts", "*.ttf"),
        os.path.join(BASE_PATH, ASSETS_DIR_NAME, "fonts", "*.eot"),
        os.path.join(BASE_PATH, ASSETS_DIR_NAME, "fonts", "*.svg"),
        os.path.join(BASE_PATH, "CV_*.pdf")
    ]:
        for file in glob.glob(file):
            if os.path.exists(file):
                log(f"Removing {file}...")
                if os.path.isfile(file):
                    os.remove(file)
                else:
                    rmtree(file)
    log("Done!", header=True)
