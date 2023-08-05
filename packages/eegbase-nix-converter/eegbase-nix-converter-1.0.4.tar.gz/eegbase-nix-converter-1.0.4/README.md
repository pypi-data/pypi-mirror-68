[![coverage report](https://gitlab.com/honza.seda/eegbase-nix-converter/badges/master/coverage.svg)](https://gitlab.com/honza.seda/eegbase-nix-converter/commits/master)
[![pipeline status](https://gitlab.com/honza.seda/eegbase-nix-converter/badges/master/pipeline.svg)](https://gitlab.com/honza.seda/eegbase-nix-converter/-/commits/master)

# EEGbase NIX converter

EEGbase NIX converter is a python script that converts BranVision/odML dataset to a NIX container file

Its design and primary use is to convert data from neurophysiology experiments taken at the Faculty of applied sciences, 
university of West Bohemia, stored in the EEGbase portal.

## Requirements

Developed and tested with `Python 3.8` 

The required third party libraries are in the [requirements.txt](requirements.txt) file.

You can install the dependencies using the command:
```
pip install -r requirements.txt
```
## Install using pip

The package is available from pip at:
```
pip install eegbase-nix-converter
```

## Usage

Run the script with the following command: 
```
python -m nixconverter DATASET [--output=<path>] [-m] [-t|--mapping=<path>] [-v] [-y]
```
    
The help can be printed out using the following command:
```
python -m nixconverter -h | --help
```

Alternatively, the script can be run with the proper requirements from the nixconverter module directory: 
```
python eegbase_nix_converter DATASET [--output=<path>] [-m] [-t|--mapping=<path>] [-v] [-y]
```

Arguments:
- `DATASET`
    - Path to the directory with the dataset. Path is expected to be relative from the script execution directory.

    - By default, the script expects the directory to contain a single dataset and will create a single NIX file.
      If you want to change this behaviour and convert multiple datasets at a time,
      you can do so by passing the `--multiple (-m)` option, which will interpret the `DATASET` as
      parent directory and expect every immediate subfolder to be a dataset folder (will run
      the conversion on every subfolder in the passed directory).

    - The tool will attempt by default to convert the odML (.xml) metadata to use the odML terminology.
      The mapping to the odML terminologies uses a predefined mapping JSON file.
      To use custom mapping, pass the path to a JSON file with the `--mapping=<path>` option.
      
      To create your own mapping file, see the [Mapping generator](#odml-mapping-generator) section.
      
      - To prevent this and use the original terminologies or not add any terminologies at all,
      pass the `--keep-terminologies (-t)` option with the script

Options:
- `-v --verbose` - Output detailed logging information to console
- `-m --multiple` - Will handle the passed path as a folder containing multiple datasets in separate directories
- `--output=<path>` - Specify the output directory for the converted files. If the path does not exist, 
                      it will be created
- `-t --keep-terminologies` - Keep the terminologies from the original odML metadata
- `-mapping=<path>` - Path to a JSON mapping file
- `-y` - Always replaces already existing files
- `-h --help` - Show help in console.

# odML Mapping generator

Part of this package is the script `odml_mapping_generator.py` for generating the mapping file from 
the odML .xml metadata. Mapping is used for the conversion of the odML files to the NIX sections and properties.

## Usage

Usage:
```
    odml_mapping_generator ODML OUTPUT
```
```
    odml_mapping_generator -h | --help
```

Arguments:
- `ODML` - Folder (and all the nested folders) that will be searched for .xml files. If multiple .xml files are found, 
           the mapping will merge all the sections and properties together into a single mapping file.
- `OUTPUT` - Name of the file to output the mapping into.

Options:
- `-h --help`                   Shows help.

## Mapping file
The mapping is a `.JSON` file containing all the sections and its properties of the odML .xml files in a folder.
Sections are represented with a key in a format of `type__name`. The properties of the section are stored in the
`props` field of the section.

> **_NOTE:_** Every section must be in the root level of the JSON.

## Section/Property mapping options
The mapping of a section or a property is defined in the `corresponding_term` field. By default, the generator fills
the corresponding term values by the original odML.

The "corresponding_term" field must consist of the "name" (Section/property name), "type" and "parent_sections" fields.

> **_NOTE:_** If the "name" or "type" field is empty, the section/property will be skipped during the conversion to 
> the NIX file.

Parent sections is a string sequence of sections.
- Each section is represented by a type_Name combination (separated by a double underscore `__` character).
- Nested sections are separated by a triple underscore `___`. Empty "parent_sections" means the root section of
the odML document.

For `parent_sections` of a property, the last section is the section where the property will be appended.
If the mapped property type is of type `date`/`datetime`, a format field is required that specifies the format used
to parse the values, e.g.: `"format": "%d.%m.%Y, %H:%M:%S"`. 

The `corresponding_term` can also contain the `definition` element that sets the `definition` of a section/property 
in the NIX file.

Example of the odML section and property with the "corresponding_term":
```json
{
  "person__person": {
      "corresponding_term": {
          "type": "person",
          "name": "Experimenter",
          "parent_sections": "collection__Experimenters"
      },
      "props": {
          "surname": {
              "type": "string",
              "example_value": "['Doe']",
              "corresponding_term": {
                "name": "LastName",
                "type": "string",
                "parent_sections": "collection__Experimenters___person__Experimenter"
              }
          }
      }
  }
}
```
> The example shows the Person section being remapped to a section "Experimenters" of type "collection".
 
> The prop surname of the original Person section will be remapped as "LastName" to a section "Experimenter" that is a 
> child section of the previously mapped "Experimenters" section.

Apart from the "corresponding_term", Props in the mapping contain the fields "type" (type in the original odML)
and "example_value" (an example of a value stored in the property). These fields have solely an  informational purpose

### Additional options

The JSON mapping file allows for some optional options:

---

`add_props` - Can be set for either for a section or a corresponding term of a property. 
    It can contain an array of properties (defined by `name`, `type` and `value`) that will be added
    at the place of the remapped section/property.

```json
"add_props": [
  {
    "name": "Role",
    "value": "Experimenter",
    "type": "string"
  }
]
```

---

`section_reference` - This field can be specified for a section. It will put an id reference of the newly remapped 
section to the specified array of properties. 

```json
"person__person": {
  "corresponding_term": {
    "type": "person",
    "name": "Experimenter",
    "parent_sections": "collection__Experimenters"
  },
  "section_reference": [
    {
      "section": "recording__Recording",
      "prop": "Experimenter",
      "ref_type": "string",
      "definition": "Contains id references to Experimenters 'person' sections"
    }
  ]
}
```

---

`use_as_reference` - An option for a property in the mapping file. If specified, the property value will be set 
as a reference in the specified NIX section instead of a new property. 
This will be used instead of the `corresponding_term` field.

```json
"props": {
  "source-link": {
    "type": "string",
    "use_as_reference": "collection/hardware_properties__HardwareProperties___hardware__EEG cap"
  }
}
```

---