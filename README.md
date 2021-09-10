<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->


# RA Flatfile importer

OS2mo flatfile importer.

## Build
```
docker build . -t ra-flatfile-importer
```
Which yields:
```
...
Successfully built ...
Successfully tagged ra-flatfile-importer:latest
```
After which you can run:
```
docker run --rm ra-flatfile-importer
```
Which yields:
```
Usage: flatfile_importer.py [OPTIONS] COMMAND [ARGS]...

  Flatfile importer.

  Used to validate and load flatfile data (JSON) into OS2mo.

Options:
  --help  Show this message and exit.

Commands:
  mo  OS2mo Flatfile importer.
```

## Usage
The primary usage of the tool is to upload flat-files to OS2mo.
```
docker run --rm ra-flatfile-importer mo upload < mo.json
```

The tool can generate dummy files to test out this functionality:
```
docker run --rm ra-flatfile-importer mo generate --name "Aarhus Kommune" > mo.json
```
These test files should be uploadable to MO and produce a valid instance.


The tool has various other commands too, such as producing the validation schema for the flat file format:
```
docker run --rm ra-flatfile-importer mo schema --indent 4
```
Which yields:
```
{
    "title": "MOFlatFileFormatImport",
    "description": "Flatfile format for OS2mo.\n\nEach chunk in the list is send as bulk / in parallel, and as such 
                    entries\nwithin a single chunk should not depend on other entries within the same chunk.\n\nMinimal 
                    valid example is [].",
    "type": "object",
    "properties": {
        "chunks": {
            ...
        },
        ...
    }
}
```
Or for validating whether a file is invalid:
```
docker run --rm ra-flatfile-importer mo validate < mo.json
```

## Versioning
This project uses [Semantic Versioning](https://semver.org/) with the following strategy:
- MAJOR: Incompatible changes to existing commandline interface
- MINOR: Backwards compatible updates to commandline interface
- PATCH: Backwards compatible bug fixes

The fileformat is versioned directly, and the version is exported in the file itself.

<!--
## Getting Started

TODO: README section missing!

### Prerequisites


TODO: README section missing!

### Installing

TODO: README section missing!

## Running the tests

TODO: README section missing!

## Deployment

TODO: README section missing!

## Built With

TODO: README section missing!

## Authors

Magenta ApS <https://magenta.dk>

TODO: README section missing!
-->
## License
- This project: [MPL-2.0](LICENSES/MPL-2.0.txt)
- Dependencies:
  - pydantic: [MIT](LICENSES/MIT.txt)

This project uses [REUSE](https://reuse.software) for licensing. All licenses can be found in the [LICENSES folder](LICENSES/) of the project.
