# Gigabloat File Manager

Note: this project is in it's baby stage, do not use it, like at all. Come back later to see how it goes.

## Development

For now Gigabloat was developed mostly on MacOS (Catalina), therefore I can only provide clear instructions for development related to MacOS, although I suppose it would be very similar on Linux and on Windows.

### MacOS

This project relies on the follwoing packages during development.  

- [PyEnv](https://github.com/pyenv/pyenv) - used to switch to the specific python version this package requires
- [Poetry](https://python-poetry.org/) - used as a dependency management solution.
- [Black](https://github.com/psf/black) - code formatter.

0. Clone/Fork this repo
1. Install PyEnv and Poetry (see their repos on instructions, Gigabloat needs just basic installation)
2. You need to add this line to zhrc, otherwise you'll see some errors while using Poetry   
`eval "$(pyenv init -)"`
3. In the root folder of this repo specify python version to use with PyEnv (this will update .python-version file)  
```shell
pyenv install 3.8.2
pyenv local 3.8.2
```
4. Run `poetry install`
5. Configure VScode workspace settings to use black and pylint  
    5.1. Get poetry virtual env path `poetry env info --path`  
    5.2. Create `.vscode` folder with `settings.json` file in it (in root of this project) and add the following lines  
    ```json
    {
        "python.formatting.blackPath": "<poetry_env_path>/bin/black",
        "python.formatting.provider": "black",
        "python.linting.pylintPath": "<poetry_env_path>/bin/pylint"
    }
    ```

## General algorithm
_This section is just for me to keep track of stuff, experimental/unfinished/uncertain_

`scanDirectory` is called with directory to scan.
for it we:
- create dummy `Directory` with just path name for now (and parent if provided)
1. get list of files (in dir, no subdirs)
    - create `File` objects for each
    - increment total files in scan with number of these files
2. get list of subdirs
    - recursively apply `scanDirectory` again
3. update dummy `Directory` with `File`s and sub`Directories`
4. add directory to `self.directories` list
5. if we end up at this point and figure out that we're in root
    - assing `self.root_directory` for easy access
6. return the `Directory` to be used in step 2

## Proposed CLI interface

Command `gigabloat scan`  
Get general stats  
Options:  
`--dir <directory>` @required  
directory to scan  
`--json`  
_Not implemented yet_  
provide json output  
`--table`  
_Not implemented yet_  
provide tabulat output  
`--pyobj`  
_Not implemented yet_  
provide pyobj output  
`--nofile`  
_Not implemented yet_  
do not save report file after scan is finished  

Command `gigabloat filter`  
_Not implemented yet_  
Filter some specific stat  
`--f <file>` @required  
specify report file  
`--ext <ext>`  
give stats for files with .<ext> extension  
`--bd`  
show biggest directory (by size)  
`--bf`  
show biggest file (by size)  
`--photos`  
show amount and size of photos  
`--videos`  
show amount and size of videos  
`--audio`  
show amount and size of audio  
`--media`  
show amount and size of media files (phtos, images, audio)  
