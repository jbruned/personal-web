import os
from shutil import rmtree
from sys import argv

from common import log, INDEX_URL, BLOG_URL, SITEMAP_URL, STRINGS_URL

if __name__ == "__main__":
    # Local directories
    BASE_PATH = argv[1] if len(argv) > 1 else ".."
    OUTPUT_FOLDER = os.path.join(BASE_PATH)
    # Build
    log("Removing generated files...", header=True)
    for file in [
        os.path.join(BASE_PATH, INDEX_URL),
        os.path.join(OUTPUT_FOLDER, f"{BLOG_URL}.html"),
        os.path.join(OUTPUT_FOLDER, SITEMAP_URL),
        os.path.join(OUTPUT_FOLDER, STRINGS_URL),
        os.path.join(OUTPUT_FOLDER, BLOG_URL)
    ]:
        if os.path.exists(file):
            log(f"Removing {file}...")
            if os.path.isfile(file):
                os.remove(file)
            else:
                rmtree(file)
    log("Done!", header=True)
