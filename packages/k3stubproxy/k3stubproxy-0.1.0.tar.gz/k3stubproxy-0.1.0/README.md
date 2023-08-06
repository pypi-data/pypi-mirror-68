# k3stubproxy

An proxy implementation to be used by embedded c stub implementations

## Stub generation
Use the cli tool k3stubproxy-generate-stub included in this package.

Requirements:
 - Stub functions begin with extern
 - In the code documnetation a parameter is labled in/out in the following style
   - param [in] variableName
   - param [out] variableName



__V0.1.0 Help:__

```
usage: k3stubproxy-generate-stub [-h] [--func_prefix FUNC_PREFIX]
                                 [--filename_suffix FILENAME_SUFFIX]
                                 [--file_header FILE_HEADER]
                                 [--stub_function_definition_out STUB_FUNCTION_DEFINITION_OUT]
                                 [-o OUTPUT] [-v] [-vv]
                                 files [files ...]

Tool for generating stub.c files that work with k3stubproxy from implemented stub.c files

Author: Joachim Kestner <joachim.kestner@khoch3.de>
Version: 0.1.0

positional arguments:
  files                 One or more files to be parsed for stub creation

optional arguments:
  -h, --help            show this help message and exit
  --func_prefix FUNC_PREFIX
                        A function prefix that will, if set, only stub
                        functions that match this prefix
  --filename_suffix FILENAME_SUFFIX
                        A suffix that is added before the extension for
                        created files
  --file_header FILE_HEADER
                        Path to a file whose contents will become the initial
                        part of each file. Use for generic includes.
  --stub_function_definition_out STUB_FUNCTION_DEFINITION_OUT
                        File path to which the stub function definition will
                        be written to as json. Default:
                        stub_function_definition.json
  -o OUTPUT, --output OUTPUT
                        Output directory. Default is .
  -v, --verbose         Enable info logging
  -vv, --extra_verbose  Enable debug logging
```

__Example CLI Usage__
```
k3stubproxy-generate-stub -v ../Code/HAL/HAL_*.c --func_prefix HAL_ -o ../Code/HAL/high_level_stub/ --filename_suffix _teststub --file_header defheader.txt --stub_function_definition_out stub_function_definition.json
```

## Example usage within C

### C API usage

### General Information About Embedding Python Within C


```c
char* phDir = "/some/path/to/a/venv";
printf("INFO: Using virutalenv: %s", phDir);
// This should not be some hard code palth like /home/annoying_user/temp/project123
// For example in some usages of the k3stubproxy this is set dynamically to look
// beside the exe vor the venv

// Note: Need to check return of Py_DecodeLocale is != NULL
Py_SetPythonHome(Py_DecodeLocale(phDir, NULL));

//optional but recommended
wchar_t *program = Py_DecodeLocale("stub_program", NULL);
Py_SetProgramName(program);

Py_Initialize();

// Then any lib within the venv can be used via cpython
PyRun_SimpleString("import k3stubproxy;");
```