from hashlib import md5
import json
import os
import re
from sys import argv
from typing import Tuple
from jinja2 import Template
from markdown import markdown

def build_blog_post(template: str, content: str, asset_hashes: callable):
    """
    Build a blog post from a template and content
    - template: post template (in HTML with Jinja2)
    - content: content of the blog post (in Markdown)
    - asset_hashes: callable to compute the function to compute the dictionary of hashes for the assets
    """
    # Get the metadata from the markdown comment
    metadata, content = extract_metadata(content)
    metadata = process_metadata(metadata)
    metadata["content"] = parse_content(content)
    # Return the rendered template
    return Template(template).render(post=metadata, hashes=asset_hashes()), metadata

def extract_metadata(content: str) -> Tuple[dict, str]:
    """
    Get the metadata from the markdown comment
    """
    metadata = {}
    if not content.startswith("<!--"):
        return metadata, content
    comment = content.split("-->", maxsplit=1)[0][4:].strip()
    for line in comment.split("\n"):
        if ":" not in line:
            continue
        key, value = line.split(":", maxsplit=1)
        metadata[key.strip().lower()] = value.strip()
    content = content.split("-->", maxsplit=1)[1].strip()

    public = metadata["public"] if "public" in metadata else "true"
    metadata["public"] = public.lower() in ["true", "yes", "1"]

    # Get the thumbnail from the first image, if any
    if "thumbnail" not in metadata:
        images = find_image_urls(content)
        if len(images) > 0:
            metadata["thumbnail"] = images[0]
        
    # Filter empty lines at the beginning or the end
    while content.startswith("\n") or content.startswith(" "):
        content = content[1:]
    while content.endswith("\n") or content.endswith(" "):
        content = content[:-1]
    return metadata, content

def parse_content(content: str) -> str:
    """
    Parse the Markdown content to HTML
    """
    # Convert the content from Markdown to HTML
    content = markdown(content)
    # Add target blank to all links so that they open in a new tab
    # TODO: only do this for external links
    content = re.sub(r"<a([^>]+)>", r"<a\1 target=\"_blank\">", content)
    # If there is any h1, increase all the heading levels by one
    if "<h1>" in content:
        for i in range(6, 0, -1):
            content = content.replace(f"<h{i}>", f"<h{i+1}>")
            content = content.replace(f"</h{i}>", f"</h{i+1}>")
    # Replace all iframes tags' src with data-lazy-src
    content = re.sub(r'<iframe([^>]+)src=\\?"([^\\]+)\\?"([^>]+)>', r'<iframe\1data-lazy-src="\2"\3>', content)
    # Replace all img tags' src with data-lazy-src
    content = re.sub(r'<img([^>]+)src=\\?"([^\\]+)\\?"([^>]+)>', r'<img\1data-lazy-src="\2"\3>', content)
    return content

def find_image_urls(content: str) -> list:
    """
    Find all image URLs in the content
    """
    youtube_urls = find_youtube_urls(content)
    youtube_thumbnails = [get_youtube_thumbnail(url) for url in youtube_urls]
    return [
        url[0] if url[0] else url[1].replace(")", "") for url in
        re.findall(r'<img[^>]*src="([^"]+)"[^>]*>|!\[[^\]]*\]\(([^"\s]+)[^)]*\)', content)
    ] + youtube_thumbnails

def find_youtube_urls(content: str) -> list:
    """
    Find all iframe URLs in the content that are YouTube videos
    """
    return [
        url for url in
        re.findall(r'<iframe[^>]*src="([^"]+)"[^>]*>', content)
        if "youtube" in url
    ]

def get_youtube_thumbnail(youtube_url: str) -> str:
    """
    Get the thumbnail of a YouTube video
    """
    youtube_id = youtube_url.split("/")
    if len(youtube_id) < 2:
        youtube_id = youtube_id[0].split("=")
    if len(youtube_id) < 2:
        return None
    youtube_id = youtube_id[-1]
    return f"https://img.youtube.com/vi/{youtube_id}/maxresdefault.jpg"


def urlify(title: str) -> str:
    """
    Convert a title to a URL
    Replaces any spaces and non-alphanumeric characters with a dash
    """
    return re.sub(r"\s+", "-",
        re.sub(r"[^a-z0-9]", " ", title.lower()).strip()
    )

def idify(title_or_url: str) -> str:
    """
    Convert a title or URL to an ID
    Replaces any spaces and non-alphanumeric characters with an underscore
    """
    return urlify(title_or_url).replace("-", "_")

def process_metadata(metadata: dict) -> dict:
    """
    Process the metadata
    """
    assert "title" in metadata, "The title is required"
    if "url" not in metadata:
        metadata["url"] = urlify(metadata["title"])
    if "tag" in metadata:
        metadata["tag"] = process_tag(metadata["tag"])
    return metadata

def process_tag(tag: str) -> dict:
    """
    Process a tag
    """
    return {
        "name": tag,
        "id": idify(tag),
        "url": urlify(tag)
    }

def build_blog_posts(template_path: str, content_path: str, output_path: str, asset_hashes: callable):
    """
    Build all blog posts from a template and content
    - template: path to the template (HTML with Jinja2)
    - content: path to the Markdown files
    - output_path: route to the build folder
    - asset_hashes: callable to compute the dictionary of hashes for the assets
    """
    if not os.path.exists(content_path) or not os.path.isdir(content_path):
        print("The content path doesn't exist or isn't a directory")
        return
    if not os.path.exists(template_path) or not os.path.isfile(template_path):
        print("The template path doesn't exist or isn't a file")
        return
    if not os.path.exists(output_path) or not os.path.isdir(output_path):
        os.mkdir(output_path)
    template = open(template_path, "r").read()
    posts = []
    for filename in os.listdir(content_path):
        if not filename.endswith(".md"):
            print(f"> Skipping {filename} (not a Markdown file)")
            continue
        with open(os.path.join(content_path, filename), "r") as f:
            content = f.read()
        rendered, metadata = build_blog_post(template, content, asset_hashes)
        if "public" not in metadata or metadata["public"]:
            posts.append(metadata)
            with open(os.path.join(output_path, f"{metadata['url']}.html"), "w") as f:
                f.write(rendered)
            print(f"> Built {metadata['url']}")
        else:
            print(f"> Skipped {metadata['url']} (set as not public)")
    return posts

def parse_date(date: str) -> str:
    """
    Parse a date in DD_MM_YYYY format to an integer YYYYMMDD
    """
    for i in ["-", "/", " ", "_", "."]:
        date = date.replace(i, "")
    return sum([int(x) * 10 ** i for i, x in enumerate(reversed(date))])

def build_blog_index(template_path: str, posts: list, index_file: str, sitemap_file: str, asset_hashes: callable):
    """
    Build the blog index from a template and content
    - template: path to the template (HTML with Jinja2)
    - posts: list of posts (as returned by build_blog_posts)
    - index_file: path to the output index file
    - sitemap_file: path to the output sitemap file
    - asset_hashes: callable to compute the dictionary of hashes for the assets
    """
    if not os.path.exists(template_path) or not os.path.isfile(template_path):
        print("The template path doesn't exist or isn't a file")
        return
    if len(posts) == 0:
        print("[Warning] No posts found")
    # Aggregate the tags
    tags = {}
    for post in posts:
        if "tag" not in post:
            continue
        tag = post["tag"]
        if tag["id"] not in tags:
            tags[tag["id"]] = tag
    if len(tags) == 0:
        print("[Warning] No tags found")
    # Build the index
    template = open(template_path, "r").read()
    with open(index_file, "w") as f:
        f.write(Template(template).render(
            posts=sorted(posts, key=lambda p: parse_date(p["date"]), reverse=True),
            tags=list(tags.values()),
            hashes=asset_hashes()
        ))
    print(f"> Built index")
    # Build the sitemap
    pass

DEFAULT_LANG = "es" # Lowercase!

def process_project(project: dict) -> dict:
    """
    Process a project's metadata
    """
    if "id" not in project:
        print("> Skipping project (no ID)")
        return None
    for required_attr in ["cat_id", "media", "strings"]:
        if required_attr not in project or project[required_attr] is None:
            print(f"> Skipping project {project['id']} (no {required_attr})")
            return None
    if "thumbnail" not in project:
        if "youtube" in project["media"]:
            project["thumbnail"] = get_youtube_thumbnail(project["media"])
        else:
            project["thumbnail"] = project["media"] # TODO: compress image
    project["is_media_iframe"] = "youtube" in project["media"]
    project["media"] = project["media"].replace("youtube.com/embed", "youtube-nocookie.com/embed")
    langs = project["strings"].keys()
    # Move the default language to the first position
    if DEFAULT_LANG in langs:
        langs = [DEFAULT_LANG] + [lang.lower() for lang in langs if lang != DEFAULT_LANG]
    strings = {
        key: {} for key in project["strings"]
    }
    for lang in langs:
        for attr in ["title", "html", "category", "btn_text"]:
            if attr in project["strings"][lang]:
                string_id = project["id"] + "_" + attr
                strings[lang][string_id] = project["strings"][lang][attr]
                if lang == DEFAULT_LANG or attr not in project:
                    project[attr] = {
                        "string_id": string_id,
                        "static_value": project["strings"][lang][attr]
                    }
    for required_attr in ["title", "html"]:
        if required_attr not in project:
            print(f"> Skipping project {project['id']} (no {required_attr} string in any language)")
            return None
    project["strings"] = strings
    return project

def build_index(template: str, index_file: str, asset_hashes: callable, projects_json: str, strings_template: str, strings_file: str):
    """
    Build the home page from a template
    - template: path to the template (HTML with Jinja2)
    - index_file: path to the output index file
    - asset_hashes: callable to compute the dictionary of hashes
    - projects_json: path to the projects JSON file
    - strings_template: path to the strings template (JS with Jinja2)
    - strings_file: path to the output strings file
    """
    if not os.path.exists(template) or not os.path.isfile(template):
        print("The template path doesn't exist or isn't a file")
        return
    if not os.path.exists(projects_json) or not os.path.isfile(projects_json):
        print("The projects JSON path doesn't exist or isn't a file")
        return
    with open(projects_json, "r") as f:
        projects = json.loads(f.read())
    projects = [process_project(project) for project in projects]
    # Remove empty projects
    projects = [project for project in projects if project is not None]
    string_translations = {}
    for project in projects:
        for lang in project["strings"]:
            # Add the string translations to the global dictionary
            if lang not in string_translations:
                string_translations[lang] = {}
            string_translations[lang].update(project["strings"][lang])
        del project["strings"]
    strings_template = open(strings_template, "r").read()
    with open(strings_file, "w") as f:
        f.write(Template(strings_template).render(strings=string_translations))
    template = open(template, "r").read()
    with open(index_file, "w") as f:
        f.write(Template(template).render(projects=projects, hashes=asset_hashes()))
    print(f"> Built index")

def file_hash(file: str):
    """
    Get the hash of a file
    """
    with open(file, "rb") as f:
        return md5(f.read()).hexdigest()

if __name__ == "__main__":
    # Local directories
    BASE_PATH = argv[1] if len(argv) > 1 else ".."
    POSTS_FOLDER = os.path.join(BASE_PATH, "posts")
    TEMPLATES_FOLDER = os.path.join(BASE_PATH, "templates")
    OUTPUT_FOLDER = os.path.join(BASE_PATH)
    ASSETS_PATH = os.path.join(BASE_PATH, "assets")
    # Local template filenames
    POST_TEMPLATE = "post.html"
    BLOG_TEMPLATE = "blog.html"
    INDEX_TEMPLATE = "index.html"
    STRINGS_TEMPLATE = "strings.js"
    PROJECTS_JSON = "projects.json"
    # Local assets filenames and hashes
    asset_paths = {
        'icon': os.path.join(ASSETS_PATH, 'img', 'favicon.ico'),
        'style': os.path.join(ASSETS_PATH, 'style.css'),
        'script': os.path.join(ASSETS_PATH, 'script.js'),
        'script': os.path.join(ASSETS_PATH, 'strings.js')
    }
    def asset_hashes():
        return {
            name: file_hash(path)
            for name, path in asset_paths.items()
        }
    # Remote URLs
    BLOG_URL = "blog"
    SITEMAP_URL = "sitemap.xml"
    INDEX_URL = "index.html"
    STRINGS_URL = os.path.join("assets", "strings.js")
    # Build
    print("Building index...")
    build_index(
        os.path.join(TEMPLATES_FOLDER, INDEX_TEMPLATE),
        os.path.join(OUTPUT_FOLDER, INDEX_URL),
        asset_hashes,
        os.path.join(BASE_PATH, PROJECTS_JSON),
        os.path.join(TEMPLATES_FOLDER, STRINGS_TEMPLATE),
        os.path.join(OUTPUT_FOLDER, STRINGS_URL)
    )
    print("Building blog posts...")
    posts = build_blog_posts(
        os.path.join(TEMPLATES_FOLDER, POST_TEMPLATE),
        POSTS_FOLDER,
        os.path.join(OUTPUT_FOLDER, BLOG_URL),
        asset_hashes
    )
    print("Building blog index...")
    build_blog_index(
        os.path.join(TEMPLATES_FOLDER, BLOG_TEMPLATE),
        posts,
        os.path.join(OUTPUT_FOLDER, f"{BLOG_URL}.html"),
        os.path.join(OUTPUT_FOLDER, SITEMAP_URL),
        asset_hashes
    )
    print("Done!")
