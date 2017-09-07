# CVGen
This is a set of scripts that generates a Curriculum Vitae, based on data stored in a .json file.

## Requirements
* Python 3.6
* A \*nix distribution that supports the [wkhtmltopdf](https://wkhtmltopdf.org/) binary I have included (probably linux).

## Usage

    ./cvgen.py examples.json/sample_cv.json

writes to `output/John\\ Doe\\ Curriculum\\ Vitae.html`
and `output/John\\ Doe\\ Curriculum\\ Vitae.pdf`
as dictated by the the general[title] section of the json file.

## Description

## Pre-defined JSON Keys

* **["program"]** required to be "cvgen"
* **["css_files"]** a list of css template files to be rendered and added to the cv
* **["general"]** See the [["general"]](#["general"]) section
* **["pages"]** See the [["pages"]](#["pages"]) section

e.g.

    {
        "program": "cvgen",
        "css_files": ["sample.css", ...],
        "general": {
            "header": "header.html",
            "footer": "footer.html",
            "paper_size": { ... },
            ...
        },
        "pages": { ... },
        ...
    }

### ["general"]
* **["general"]["header"]** Defines the template to be used for the page header
* **["general"]["footer"]** Defines the template to be used for the page footer
* **["general"]["paper_size"]** See the [["general"]["paper_size"]](#["general"]["paper_size"]) section
* **["general"]["style"]** Defines the template set to be used (directly matches to immediate contents of the `layout/` directory.

e.g.

    {
        "general": {
            "header": "header.html",
            "footer": "footer.html",
            "paper_size": { ... },
            "style": "default"
            ...
        },
        ...
    }

#### ["general"]["paper_size"]
* **["general"]["paper_size"]["unit"]** Defines the units to be used in the css file
* **["general"]["paper_size"]["width"]** Defines the width of the page (currently needs to be 210, otherwise wkhtmltopdf will have a mismatch)
* **["general"]["paper_size"]["height"]** Defines the hight of the page (needs to be 297)
* **["general"]["paper_size"]["margin_left"]** Defines the left page margin
* **["general"]["paper_size"]["margin_right"]** Defines the right page margin
* **["general"]["paper_size"]["margin_top"]** Defines the top margin

e.g.

    {
        "general": {
            ...
            "paper_size": {
                "width": 210,
                "height": 297,
                "unit": "mm",
                "margin_left": 45,
                "margin_right": 45,
                "margin_top": 30,
                "margin_bottom": 30
             },
             ...
        },
        ...
    }


### ["pages"]
* **["pages"][PAGE_NAME]** See the [["PAGES"][PAGE_NAME]](#["pages"][PAGE_NAME]) section. `PAGE_NAME` can be defined by the user.

e.g.

    {
        ...
        "pages": {
            "page one": { ... },
            ...
        }
    }
  

#### ["pages"][PAGE_NAME]
* **["pages"][PAGE_NAME]["blocks"]** A dictionary of Blocks, where the key is used for the title (See the [Blocks]](#Blocks) section)

e.g.

    {
        ...
        "pages": {
            "page one": { 
                "blocks": { ... }
            },
            ...
        }
    }

### Blocks
A block is a section of a CV, which is rendered using json data and a template.
A typical block has the following form:

    {
        ...
        "pages": {
            "1": {
                "blocks": {
                    "BLOCK_TITLE": {
                        "name": true,
                        "type": "BLOCK_TYPE",
                        "data": { ... },
                    }, 
                    ...
                }
            },
            ...
        },
        ...
    }

* `BLOCK_TITLE` is the title of the block, and a CSS class name for that block.
* `name` defines whether the heading containing `BLOCK_TITLE` is shown or not.
* `type` is a pointer to the template to be used (e.g. "list" -> "templates/list.html")
* `data` are the variables passed to the template when being rendererd. These are dependant on the block being used.
