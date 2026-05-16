<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple and easy-to-use static site generator. It parses Markdown content to HTML format and builds a static site.

Created as part of the referenced [Boot.dev course](https://www.boot.dev/courses/build-static-site-generator-python).

<br>

<!-- GETTING STARTED -->
## Prerequisites

The only requisite is Python 3+
  ```sh
  sudo apt update
  sudo apt install python3
```

<br>

<!-- USAGE EXAMPLES -->
## Usage

The app has two folders for site content.
<ul>
  <li><b>content: </b>Main content of the site in Markdown files.</li>
  <li><b>static: </b>Static content such as css files, images, etc.</li>
</ul>

Both folders have some preloaded content. They have to be removed in order to generate a new site.

Once the new content has been added, just run the script.

```sh
./main.sh
```
<br>

## Test

The app has several test modules that use the standard Python [unittest](https://docs.python.org/3/library/unittest.html) library.
