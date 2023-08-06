# General testing and feedback

Unified tester for any language, for any exam

## Currently supported languages

 - Python
 - C++

# How to run

run the feedback module with the name of the tested file, and the appropriate configuration

The runner assumes that all required modules are in the same directory as the tested file. The all files in the directory containing the tested file will be copied, and used for evaluation

## Examples

Python:
```
python -m feedback "tests/fixtures/integration/py/tested.py" "tests/fixtures/integration/py/py_config.json"
```

C++:
```
python -m feedback "tests/fixtures/integration/cpp/tested.cpp" "tests/fixtures/integration/cpp/cpp_config.json"
```

## Config file arhitecture

The config file uses JSON to serialise data.

### Tests

Specify a list of tests that should be ran, under the `"tests"` key, with each test name as a key and with a set of key-value pairs under that.

Every test requires the `"max_score"` key, and some tests may require other parameters

#### Currently supported tests and parameters
 - All
    - (optional) number
    - (optional) tags
    - (optional) visibility

 - C++
    - compile
        - max_score
        - (optional) warning_penalty: [0.0, 1.0]
    - functionality
        - max_score
        - tester_file
    - functionality_executable
        - max_score
        - tester_file
    - comments
        - max_score
    - static
        - max_score
        - (optional) error_penalty: [0.0, 1.0]
    - style
        - style
        - max_score
 - Python
    - syntax
        - max_score
    - functionality
        - max_score
        - tester_file
    - comments
        - max_score

### Example config

```
{
    "tests": [
        {
            "type": "compile",
            "max_score": 10.0,
            "number": "1",
            "tags": [],
            "visibility": "visible"
        },
        {
            "type": "functionality",
            "max_score": 60.0,
            "number": "2",
            "tags": [],
            "visibility": "visible",
            "tester_file": "run_code.cpp"
        },
        {
            "type": "static",
            "max_score": 10.0,
            "number": "4",
            "tags": [],
            "visibility": "visible"
        },
        {
            "type": "comments",
            "max_score": 10.0,
            "number": "3",
            "tags": [],
            "visibility": "visible"
        },
        {
            "type": "style",
            "max_score": 10.0,
            "number": "5",
            "tags": [],
            "visibility": "visible",
            "style": "google"
        }
    ]
}
```