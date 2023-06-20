import os
import re
from typing import Tuple
from jinja2 import Template
from markdown import markdown

def build_blog_post(template: str, content: str):
    """
    Build a blog post from a template and content
    - template: post template (in HTML with Jinja2)
    - content: content of the blog post (in Markdown)
    """
    # Get the metadata from the markdown comment
    metadata, content = extract_metadata(content)
    metadata = process_metadata(metadata)
    # Return the rendered template
    return Template(template).render(
        post_url=metadata["url"],
        post_title=metadata["title"],
        post_date=metadata.get("date", ""),
        post_content=markdown(content)
    ), metadata

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

    # Get the thumbnail from the first image, if any
    if "thumbnail" not in metadata:
        images = find_image_urls(content)
        if len(images) > 0:
            metadata["image"] = images[0]
        
    # Filter empty lines at the beginning or the end
    while content.startswith("\n") or content.startswith(" "):
        content = content[1:]
    while content.endswith("\n") or content.endswith(" "):
        content = content[:-1]
    return metadata, content

def find_image_urls(content: str) -> list:
    """
    Find all image URLs in the content
    """
    return [
        url[0] if url[0] else url[1] for url in
        re.findall(r'<img[^>]*src="([^"]+)"[^>]*>|!\[[^\]]*\]\(([^"\s]+)[^)]*\)', content)
    ]

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

def build_blog_posts(template_path: str, content_path: str, output_path: str):
    """
    Build all blog posts from a template and content
    - template: path to the template (HTML with Jinja2)
    - content: path to the Markdown files
    - output_path: route to the build folder
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
            print(f"Skipping {filename} (not a Markdown file)")
            continue
        with open(os.path.join(content_path, filename), "r") as f:
            content = f.read()
        rendered, metadata = build_blog_post(template, content)
        posts.append(metadata)
        with open(os.path.join(output_path, f"{metadata['url']}.html"), "w") as f:
            f.write(rendered)
        print(f"> Built {metadata['url']}")
    return posts

def build_blog_index(template_path: str, posts: list, index_file: str, sitemap_file: str):
    """
    Build the blog index from a template and content
    - template: path to the template (HTML with Jinja2)
    - posts: list of posts (as returned by build_blog_posts)
    - index_file: path to the output index file
    - sitemap_file: path to the output sitemap file
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
        f.write(Template(template).render(posts=posts, tags=list(tags.values())))
    print(f"> Built index")
    # Build the sitemap
    pass

INPUT_FOLDER = "../posts"
OUTPUT_FOLDER = ".."
BLOG_FOLDER = "blog"
BLOG_INDEX = "blog.html"
SITEMAP_FILE = "sitemap.xml"
POST_TEMPLATE = "post_template.html"
INDEX_TEMPLATE = "blog_template.html"

if __name__ == "__main__":
    print("Building blog posts...")
    posts = build_blog_posts(POST_TEMPLATE, INPUT_FOLDER, OUTPUT_FOLDER + "/" + BLOG_FOLDER)
    print("Building blog index...")
    build_blog_index(INDEX_TEMPLATE, posts, OUTPUT_FOLDER + "/" + BLOG_INDEX, OUTPUT_FOLDER + "/" + SITEMAP_FILE)
    print("Done!")
