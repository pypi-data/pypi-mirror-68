# Scidra Module Utils

[![PyPI version](https://badge.fury.io/py/scidra-module-utils.svg)](https://badge.fury.io/py/scidra-module-utils)

## Version: 0.2.1

## Description

A base class and a set of helper functions to reduce the amount of new code required to create new modules as
well as help enforce expeted variables and functionality of a moodule

## Example Module

This library will take care of most

```python
from scidra.module_utils import BaseModule, Output, FileRef
from typing import Dict
import json

class TestModule(BaseModule):
    def run_job_logic(self, parameters: dict, files: Dict[str, FileRef]) -> Output:
        # Use this function to 'munge' the generic module inputs and run your existing python code or even
        # a command line app that you have made available in a docker environment.
        assert "message" in parameters

        print(parameters["message"])

        return Output(
            output_json=json.dumps(
                {"out_message": f"{parameters['message']} was printed"}
            )
        )

# Good to have this variable available for the test cli runner (See tests)
module = TestModule()

def cli():
    """Used as the command line entry point in setup.py"""
    module.run()

# Optional but include this here if you want to run this file like 'python module/main.py run-job --help'
if __name__ == "__main__":
    cli()
```

```python
# Add this to setup.py
entry_points="""
    [console_scripts]
    test-module=module.main:cli
"""
```
