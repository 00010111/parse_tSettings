# parse_tSettings
## Extracts information from Settings.xml of Siemens TIA Portal
Settings.xml file is maintained by the Siemens TIA Portal holding various interesting data if the user activity on an engineering workstation, running the TIA Portal has to be analyzed. 
parse_tSettings is small python 3 script to extract this data, provided with the -v option it will also print some information on the different data fields and observations made on their behavior.
### Tested TIA Portal versions:
Version 15.1

## Usage
Option | Explanation
--- | ---
-f \<FILE\>, --file \<FILE\> | Path (relative or absolute) to the file to parse. Example: C:\Data\Settings.xml
-d \<DIRECTORY\>, --directory \<DIRECTORY\> | Path (relative or absolute) to directory that should be search recursively for a file named settings.xml. First found file will be processed.
-b, --bulk | When -d (--directory) is specified and more than one Settings.xml files should be parsed 
-v, --verbose | Increase output verbosity and include explanations about the different data fields and observations on their behavior
-h, --help | sprints usage information and exit



## Examples
```
# Analyse one Settings.xml file and print verbose output 
python3 ./parse_tSettings.py -v -f ./sampledata2/Settings.xml

# search the given directory for a settings.xml file and parse it. (First occurance will be used) User verbose output
python3 ./parse_tSettings.py -vd ~/tool/sampledata2

# search the given directory for settings.xml files and parse all of them
python3 ./parse_tSettings.py -b -d ~/tool/sampledata2
```

## Limitations
* Tested with TIA Portal Version 15.1, other Versions of the TIA Portal might behave different.
* For other information on how the data fields within the Settings.xml file have, see verbose output of the tool.

## Author
* Mastodon: [@b00010111](https://ioc.exchange/@b00010111)
* Blog: https://00010111.at/
* Twitter: [@b00010111](https://twitter.com/b00010111)

## License
* Free to use, reuse and redistribute for everyone.
* No Limitations.
* Of course attribution is always welcome but not mandatory.

## Bugs, Discussions, Feature requests, contact
* open an issue
* contact me via Mastodon: https://ioc.exchange/@b00010111
* (reaching out via Twitter doesn't really work well anymore...sorry)

## further reading
* Part 2 of the blog post series I wrote on investigationg an engineering workstation: https://blog.nviso.eu/series/investigating-an-engineering-workstation/

## Change History
 * Version 0.1000:
    * initial release
