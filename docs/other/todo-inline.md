 # Inline TODOs


# BUG

## [`myproject/other.py`](/myproject/other.py)

- make todo should see this too  
  local link: [`/myproject/other.py#1`](/myproject/other.py#1) 
  | view on GitHub: [myproject/other.py#L1](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/other.py#L1)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=make%20todo%20should%20see%20this%20too&body=%23%20source%0A%0A%5B%60myproject%2Fother.py%23L1%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fother.py%23L1%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20BUG%3A%20make%20todo%20should%20see%20this%20too%0Adef%20another_function%28%29%3A%0A%09raise%20NotImplementedError%28%22This%20function%20is%20not%20implemented%20yet%22%29%0A%60%60%60&labels=bug)

  ```python
# BUG: make todo should see this too
def another_function():
	raise NotImplementedError("This function is not implemented yet")
  ```





# DOC

## [`scripts/docs_clean.py`](/scripts/docs_clean.py)

- S_DIR` (the latter) without updating the other."  
  local link: [`/scripts/docs_clean.py#64`](/scripts/docs_clean.py#64) 
  | view on GitHub: [scripts/docs_clean.py#L64](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/docs_clean.py#L64)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=S_DIR%60%20%28the%20latter%29%20without%20updating%20the%20other.%22&body=%23%20source%0A%0A%5B%60scripts%2Fdocs_clean.py%23L64%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fdocs_clean.py%23L64%29%0A%0A%23%20context%0A%60%60%60python%0A%09assert%20docs_dir.is_dir%28%29%2C%20f%22Docs%20directory%20%27%7Bdocs_dir%7D%27%20not%20found%22%0A%09assert%20docs_dir%20%3D%3D%20Path%28docs_dir_cli%29%2C%20%28%0A%09%09f%22Docs%20directory%20mismatch%3A%20%7Bdocs_dir%20%3D%20%7D%20%21%3D%20%7Bdocs_dir_cli%20%3D%20%7D.%20this%20is%20probably%20because%20you%20changed%20one%20of%20%60pyproject.toml%3A%7BTOOL_PATH%7D.output_dir%60%20%28the%20former%29%20or%20%60makefile%3ADOCS_DIR%60%20%28the%20latter%29%20without%20updating%20the%20other.%22%0A%09%29%0A%60%60%60&labels=documentation)

  ```python
assert docs_dir.is_dir(), f"Docs directory '{docs_dir}' not found"
	assert docs_dir == Path(docs_dir_cli), (
		f"Docs directory mismatch: {docs_dir = } != {docs_dir_cli = }. this is probably because you changed one of `pyproject.toml:{TOOL_PATH}.output_dir` (the former) or `makefile:DOCS_DIR` (the latter) without updating the other."
	)
  ```





# FIXME

## [`myproject/helloworld.py`](/myproject/helloworld.py)

- an example that `make todo` should find  
  local link: [`/myproject/helloworld.py#10`](/myproject/helloworld.py#10) 
  | view on GitHub: [myproject/helloworld.py#L10](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/helloworld.py#L10)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=an%20example%20that%20%60make%20todo%60%20should%20find&body=%23%20source%0A%0A%5B%60myproject%2Fhelloworld.py%23L10%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fhelloworld.py%23L10%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20FIXME%3A%20an%20example%20that%20%60make%20todo%60%20should%20find%0Adef%20critical_function%28%29%3A%0A%09raise%20NotImplementedError%28%22This%20function%20is%20not%20implemented%20yet%22%29%0A%60%60%60&labels=FIXME)

  ```python
# FIXME: an example that `make todo` should find
def critical_function():
	raise NotImplementedError("This function is not implemented yet")
  ```





# TODO

## [`myproject/helloworld.py`](/myproject/helloworld.py)

- an example todo that `make todo` should find  
  local link: [`/myproject/helloworld.py#5`](/myproject/helloworld.py#5) 
  | view on GitHub: [myproject/helloworld.py#L5](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/helloworld.py#L5)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=an%20example%20todo%20that%20%60make%20todo%60%20should%20find&body=%23%20source%0A%0A%5B%60myproject%2Fhelloworld.py%23L5%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fhelloworld.py%23L5%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20another%20line%20which%20should%20be%20included%20in%20the%20body%0A%23%20TODO%3A%20an%20example%20todo%20that%20%60make%20todo%60%20should%20find%0Adef%20some_function%28%29%3A%0A%09raise%20NotImplementedError%28%22This%20function%20is%20not%20implemented%20yet%22%29%0A%60%60%60&labels=enhancement)

  ```python
# another line which should be included in the body
# TODO: an example todo that `make todo` should find
def some_function():
	raise NotImplementedError("This function is not implemented yet")
  ```




## [`README.md`](/README.md)

- 's from the code  
  local link: [`/README.md#70`](/README.md#70) 
  | view on GitHub: [README.md#L70](https://github.com/mivanit/python-project-makefile-template/blob/main/README.md#L70)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=%27s%20from%20the%20code&body=%23%20source%0A%0A%5B%60README.md%23L70%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2FREADME.md%23L70%29%0A%0A%23%20context%0A%60%60%60markdown%0A%20%20%20%20make%20setup%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20install%20and%20update%20via%20uv%0A%20%20%20%20make%20test%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20running%20tests%0A%20%20%20%20make%20todo%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20get%20all%20TODO%27s%20from%20the%20code%0A%20%20%20%20make%20typing%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20running%20type%20checks%0A%20%20%20%20make%20verify-git%20%20%20%20%20%20%20%20%20%20%20checking%20git%20status%0A%60%60%60&labels=enhancement)

  ```markdown
make setup                install and update via uv
    make test                 running tests
    make todo                 get all TODO's from the code
    make typing               running type checks
    make verify-git           checking git status
  ```




