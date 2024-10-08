- `PACKAGE_NAME`: !!! MODIFY AT LEAST THIS PART TO SUIT YOUR PROJECT !!!  
  it assumes that the source is in a directory named the same as the package name  
  this also gets passed to some other places      `PACKAGE_NAME := myproject`  

- `RUN_GLOBAL`: for formatting or something, we might want to run python without uv  
  RUN_GLOBAL=1 to use global `PYTHON_BASE` instead of `uv run $(PYTHON_BASE)`      `RUN_GLOBAL ?= 0`  

- `default`: No description available  
  

- `gen-version-info`: No description available  
  

- `setup`: install and update via uv  
  

- `format`: format the source code  
  

- `docs-html`: generate html docs  
  

- `verify-git`: checking git status  
  

- `clean`: clean up temporary files  
  

- `help-targets`: -n "# make targets  
    https://stackoverflow.com/questions/4219255/how-do-you-get-the-list-of-targets-in-a-makefile  
  no .PHONY because this will only be run before `make help`  
  it's a separate command because getting the versions takes a bit of time    


