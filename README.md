# Python script for results from "Elecciones Regionales y Municipales 2022"

## Installation

To install this package you must build and install following the procedure
suggested for setuptools https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html.

```
pip install --upgrade setuptools
python -m build .
python install .
```

You can also use the scrip from the current source by:
```
pip install -r requirements.txt
```

## How to use

The script could be used installed in your local environment, or directly from the
location of the package source.

If you have installed it, the command name is `dlresultserm` and admits the next
options:

```
dlresultserm [options]
```

**Options:**

* `-h, --help`

  Show this help message and exit

* `-l LOGLEVEL, --log-level=LOGLEVEL`

  Set log level. Available options: critical, error, warning, info, debug

* `-d FOLDER, --output-folder=FOLDER`

  Save to output folder


The default filename for the output json file is 
`results.json`, while for the sqlite3 file is `results.db`.
When the output folder is not defined via
`--output-folder`, the default folder name is `output` under the current
directory where the script is launched.


In case you are using the script from the source folder, you can call it via:
```
python -m dlresultserm [options] 
```

Where `[options]` are the options described above.

In case you have installed, it automatically installs a script to the system
path, so you can call as:
```
dlresultserm [options] 
```

## License

Copyright 2022 Open Política

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
