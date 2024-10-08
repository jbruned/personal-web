# Jorge's personal site [![CI/CD](https://github.com/jbruned/personal-web/actions/workflows/cicd.yml/badge.svg)](https://github.com/jbruned/personal-web/actions/workflows/cicd.yml)

In this repo, you can find the source code for my personal webpage. All of the code is public and the build & publish process is automated using pipelines.

> This project is available online at [jorgebruned.com](https://jorgebruned.com)

## Table of contents

1. [Tech stack](#tech-stack)
1. [CI/CD](#continuous-integration--deployment)
1. [Relevant features](#relevant-features)
1. [License](#license)

## Tech stack

I have developed this project from scratch using HTML, CSS and JavaScript for the frontend, as well as some libraries such as <em>Bootstrap</em> or <em>Isotope.JS</em>. It is built every time a commit is pushed to the repository by means of a custom *python* script, and then published to my server using an automated pipeline.

### Why not use a *CMS* or a *frontend framework*?

I have decided to build this project from scratch for several reasons:
- One of my main goals was to put into practice and expand my knowledge.
- I wanted to have full control over the code and the architecture of the project.
- Having an *ad hoc* solution means I'm not locked to any specific technology or framework, and I can easily change or add new features.
- Most *frameworks* require client-side rendering and/or hydration by default, which is not the best option for SEO. Although this behaviour can be changed, I wanted to avoid the extra complexity since the amount of *JavaScript* code is not that big.
- Although implementing custom *build* and *publish* scripts could well be considered *overkill*/*reinventing the wheel*, using a powerful *CMS*/*framework* would be even more so, since I would only be using a small fraction of its features. I did find some disadvantages, like the lack of a component-based architecture, with reusable components and props, like the ones provided by *React*. 

## Continuous integration & deployment

The pipeline is implemented by means of GitHub Actions. There is a single stage, in which the code is built and published to my server using FTP. Such stage is triggered on every push to the `main` branch and does the following:
1. Ofc, install all the dependencies and prepare the environment.
1. Build the custom icon font using `fontello-cli`. Some advantages include the ability to use any icon I want, from different sources, and that only the icons I use are included in the font, which reduces the size of the font file.
1. Build the project using a custom *python* script (see "Why not use a CMS or a frontend framework?"):
    - `jinja2` is used as a template engine, and all necessary data is stored in *JSON* and *Markdown* files. This allows me to easily add new projects and blog posts while avoiding redundant and repetitive code.
    - Hashes are calculated for any files which are prone to be cached by the browser, such as stylesheets or scripts. This prevents the client from using outdated versions of the code, while easing cache management.
1. Render the website as a static PDF. This is done by means of a headless browser using `puppeteer`. The main reason for this is that the print behaviour and styles are highly inconsistent across browsers, and this way I can ensure that the PDF will look as expected. Apart from the PDF being rendered only once in the server, this also provides me with an always up-to-date version of my CV in PDF format (so I don't have to create it manually every time I need it). 
1. Publish the build to the server using FTP. Only the files that have changed are uploaded; this is also done by means of a custom *python* script based in the MD5 hashes of the files.

## Relevant features

Some random features that I think are worth mentioning:

- Most media is lazy-loaded using a custom *JavaScript* implementation. For example, images or videos for the projects are only loaded when the user opens the corresponding modal.
- Thumbnails are automatically fetched from YouTube or the first image of a post.
- The website is fully responsive, which makes it suitable for any device, and also for printing.
- Most data is stored in *JSON* and *Markdown* files, which makes changes easier and quicker, and avoids redundant and repetitive code. The site is built automatically from these files, along with HTML templates.
- A PDF version optimized for printing is automatically generated in the *pipeline*, so that I always have the last version available for sharing when necessary.
- The website is available in both English and Spanish. The language can be dynamically changed without reloading the page by means of a switch in the navbar.
- All of the generated files are built automatically, including the icon font, the rendered PDF, and all of the HTML files. There is also a custom *python* script to automatically build the project when changes are detected.
- The entire build & deployment process is automated by means of pipelines.
- Email is hidden from bots and only revealed when the user clicks on it.
- Built from scratch using HTML, CSS and JavaScript. I didn't use a CMS like Wordpress or a UI framework like Angular because I wanted full control over the architecture, while developing my own ad-hoc solution. Furthermore, my objective was to practice and learn, which I definitely did!

## License

The author of this piece of software is Jorge Bruned. As per the [license](/LICENSE), you are allowed to fork, use and modify the source code, as long as you make the modifications public (open source) and keep all of the attributions to the original author unaltered (including those in the GUI; i.e., the webpage).

