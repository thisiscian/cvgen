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

## JSON Keys

* **["program"]** required to be "cvgen"
* **["css_files"]** a list of css template files to be rendered and added to the cv
* **["general"]** See the [general](#general) section
* **["pages"]** See the [pages](#pages) section

### ["general"]
* **["general"]["header"]** Defines the template to be used for the page header
* **["general"]["footer"]** Defines the template to be used for the page footer
* **["general"]["css_files"]** Defines (in list form) the css files that should be rendered into the cv.
* **["general"]["paper_size"]** See the [paper_size](#paper_size) section

#### ["general"]["paper_size"]
* **["general"]["paper_size"]["unit"]** Defines the units to be used in the css file
* **["general"]["paper_size"]["width"]** Defines the width of the page (currently needs to be 210, otherwise wkhtmltopdf will have a mismatch)
* **["general"]["paper_size"]["height"]** Defines the hight of the page (needs to be 297)
* **["general"]["paper_size"]["margin_left"]** Defines the left page margin
* **["general"]["paper_size"]["margin_right"]** Defines the right page margin
* **["general"]["paper_size"]["margin_top"]** Defines the top margin

{
    "program":"cvgen",
    "version":"0.01",
    "general": {
        "name":"John Doe",
        "address":["01 Example Lane", "City", "Country"],
        "phoneNumber": "+123 (0)45 678 9012",
        "email": "example@email.com",
        "website": "google.com",
        "paper_size": {
            "width": 210,
            "height": 297,
            "unit": "mm",
            "margin_left": 45,
            "margin_right": 45,
            "margin_top": 30,
            "margin_bottom": 30
         },
        "style": "default",
        "title": "John Doe Curriculum Vitae",
        "header": "header.html",
        "footer": "footer.html"
    },
    "css_files": [ "css/cv.css" ],
    "pages": {
        "1": {
            "blocks": {
                "Contact": {
                    "type": "list",
                    "data": {
                        "name": false,
                        "items": "{{[general][address]}}"
                    }
                },
                "About": {
                    "type": "text",
                    "data": {
                        "name": false,
                        "content": "About me; i am good at the stuff that i do including making cvs."
                    }
                },
                "Education": {
                    "type": "education",
                    "data": {
                        "degrees": [
                            { "award": "1.1", "level": "BA", "course": "CV Automation", "school": "Python School" },
                            { "award": "II.2", "level": "MA", "course": "CV Design", "school": "Design School" }
                        ]
                    }
                },

                "Technical Skills": {
                    "type": "named_item_list",
                    "data": {
                        "items": [
                            ["Languages","C, V, Python, CSS, HTML5, Jinja2"],
                            ["Aaahhh","BBB, CCC"],
                            ["Example","This is an example by the way"]
                        ]
                    }
                },

                "Strengths": {
                    "type":"list",
                    "data": {
                        "items": [
                            "Communicates to your employer",
                            "What you are strong at",
                            "In a flexible manner"
                        ]
                    }
                },
                "Hobbies": {
                    "type":"list",
                    "data": {
                        "items": [
                            "Writing code to generate CVs",
                            "Staying DRY"
                        ]
                    }
                }
            }
        },
        "2": {
            "blocks": {
                "Work History": {
                    "type":"work_history",
                    "data": {
                        "jobs": [
                            {
                                "title":"Associate Curriculum Vitae",
                                "company": "CV Ltd.",
                                "duration": "Then - Now",
                                "description":"That's it."
                            } 
                        ]
                    }
                },
                "References": {
                    "type":"text",
                    "data": {
                        "content": "Available upon request"
                    }
                }
            }
        }
    }
}
    


