 # Inline TODOs


# BUG

## [`myproject/other.py`](/myproject/other.py)

- make todo should see this too  
  local link: [`/myproject/other.py#4`](/myproject/other.py#4) 
  | view on GitHub: [myproject/other.py#L4](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/other.py#L4)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=make%20todo%20should%20see%20this%20too&body=%23%20source%0A%0A%5B%60myproject%2Fother.py%23L4%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fother.py%23L4%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20BUG%3A%20make%20todo%20should%20see%20this%20too%0Adef%20another_function%28%29%20-%3E%20None%3A%0A%09%22dummy%20docstring%22%0A%60%60%60&labels=bug)

  ```python
  # BUG: make todo should see this too
  def another_function() -> None:
  	"dummy docstring"
  ```





# DOC

## [`scripts/docs_clean.py`](/scripts/docs_clean.py)

- S_DIR: str = "docs"  
  local link: [`/scripts/docs_clean.py#17`](/scripts/docs_clean.py#17) 
  | view on GitHub: [scripts/docs_clean.py#L17](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/docs_clean.py#L17)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=S_DIR%3A%20str%20%3D%20%22docs%22&body=%23%20source%0A%0A%5B%60scripts%2Fdocs_clean.py%23L17%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fdocs_clean.py%23L17%29%0A%0A%23%20context%0A%60%60%60python%0ATOOL_PATH%3A%20str%20%3D%20%22tool.makefile.docs%22%0ADEFAULT_DOCS_DIR%3A%20str%20%3D%20%22docs%22%0A%60%60%60&labels=documentation)

  ```python
  TOOL_PATH: str = "tool.makefile.docs"
  DEFAULT_DOCS_DIR: str = "docs"
  ```


- S_DIR), set()  
  local link: [`/scripts/docs_clean.py#32`](/scripts/docs_clean.py#32) 
  | view on GitHub: [scripts/docs_clean.py#L32](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/docs_clean.py#L32)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=S_DIR%29%2C%20set%28%29&body=%23%20source%0A%0A%5B%60scripts%2Fdocs_clean.py%23L32%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fdocs_clean.py%23L32%29%0A%0A%23%20context%0A%60%60%60python%0A%09%22read%20configuration%20from%20pyproject.toml%22%0A%09if%20not%20pyproject_path.is_file%28%29%3A%0A%09%09return%20Path%28DEFAULT_DOCS_DIR%29%2C%20set%28%29%0A%0A%09with%20pyproject_path.open%28%22rb%22%29%20as%20f%3A%0A%60%60%60&labels=documentation)

  ```python
  	"read configuration from pyproject.toml"
  	if not pyproject_path.is_file():
  		return Path(DEFAULT_DOCS_DIR), set()
  
  	with pyproject_path.open("rb") as f:
  ```


- S_DIR))  
  local link: [`/scripts/docs_clean.py#38`](/scripts/docs_clean.py#38) 
  | view on GitHub: [scripts/docs_clean.py#L38](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/docs_clean.py#L38)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=S_DIR%29%29&body=%23%20source%0A%0A%5B%60scripts%2Fdocs_clean.py%23L38%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fdocs_clean.py%23L38%29%0A%0A%23%20context%0A%60%60%60python%0A%09preserved%3A%20List%5Bstr%5D%20%3D%20deep_get%28config%2C%20f%22%7BTOOL_PATH%7D.no_clean%22%2C%20%5B%5D%29%0A%09docs_dir%3A%20Path%20%3D%20Path%28deep_get%28config%2C%20f%22%7BTOOL_PATH%7D.output_dir%22%2C%20DEFAULT_DOCS_DIR%29%29%0A%0A%09%23%20Convert%20to%20absolute%20paths%20and%20validate%0A%60%60%60&labels=documentation)

  ```python
  	preserved: List[str] = deep_get(config, f"{TOOL_PATH}.no_clean", [])
  	docs_dir: Path = Path(deep_get(config, f"{TOOL_PATH}.output_dir", DEFAULT_DOCS_DIR))
  
  	# Convert to absolute paths and validate
  ```


- S_DIR` (the latter) without updating the other."  
  local link: [`/scripts/docs_clean.py#78`](/scripts/docs_clean.py#78) 
  | view on GitHub: [scripts/docs_clean.py#L78](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/docs_clean.py#L78)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=S_DIR%60%20%28the%20latter%29%20without%20updating%20the%20other.%22&body=%23%20source%0A%0A%5B%60scripts%2Fdocs_clean.py%23L78%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fdocs_clean.py%23L78%29%0A%0A%23%20context%0A%60%60%60python%0A%09assert%20docs_dir.is_dir%28%29%2C%20f%22Docs%20directory%20%27%7Bdocs_dir%7D%27%20not%20found%22%0A%09assert%20docs_dir%20%3D%3D%20Path%28docs_dir_cli%29%2C%20%28%0A%09%09f%22Docs%20directory%20mismatch%3A%20%7Bdocs_dir%20%3D%20%7D%20%21%3D%20%7Bdocs_dir_cli%20%3D%20%7D.%20this%20is%20probably%20because%20you%20changed%20one%20of%20%60pyproject.toml%3A%7BTOOL_PATH%7D.output_dir%60%20%28the%20former%29%20or%20%60makefile%3ADOCS_DIR%60%20%28the%20latter%29%20without%20updating%20the%20other.%22%0A%09%29%0A%60%60%60&labels=documentation)

  ```python
  	assert docs_dir.is_dir(), f"Docs directory '{docs_dir}' not found"
  	assert docs_dir == Path(docs_dir_cli), (
  		f"Docs directory mismatch: {docs_dir = } != {docs_dir_cli = }. this is probably because you changed one of `pyproject.toml:{TOOL_PATH}.output_dir` (the former) or `makefile:DOCS_DIR` (the latter) without updating the other."
  	)
  ```





# FIXME

## [`myproject/helloworld.py`](/myproject/helloworld.py)

- an example that `make todo` should find  
  local link: [`/myproject/helloworld.py#13`](/myproject/helloworld.py#13) 
  | view on GitHub: [myproject/helloworld.py#L13](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/helloworld.py#L13)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=an%20example%20that%20%60make%20todo%60%20should%20find&body=%23%20source%0A%0A%5B%60myproject%2Fhelloworld.py%23L13%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fhelloworld.py%23L13%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20FIXME%3A%20an%20example%20that%20%60make%20todo%60%20should%20find%0Adef%20critical_function%28%29%20-%3E%20None%3A%0A%09%22dummy%20docstring%22%0A%60%60%60&labels=FIXME)

  ```python
  # FIXME: an example that `make todo` should find
  def critical_function() -> None:
  	"dummy docstring"
  ```





# TODO

## [`myproject/helloworld.py`](/myproject/helloworld.py)

- an example todo that `make todo` should find  
  local link: [`/myproject/helloworld.py#7`](/myproject/helloworld.py#7) 
  | view on GitHub: [myproject/helloworld.py#L7](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/helloworld.py#L7)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=an%20example%20todo%20that%20%60make%20todo%60%20should%20find&body=%23%20source%0A%0A%5B%60myproject%2Fhelloworld.py%23L7%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fhelloworld.py%23L7%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20another%20line%20which%20should%20be%20included%20in%20the%20body%0A%23%20TODO%3A%20an%20example%20todo%20that%20%60make%20todo%60%20should%20find%0Adef%20some_function%28%29%20-%3E%20None%3A%0A%09%22dummy%20docstring%22%0A%60%60%60&labels=enhancement)

  ```python
  # another line which should be included in the body
  # TODO: an example todo that `make todo` should find
  def some_function() -> None:
  	"dummy docstring"
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




## [`scripts/docs_clean.py`](/scripts/docs_clean.py)

- this is not recursive  
  local link: [`/scripts/docs_clean.py#57`](/scripts/docs_clean.py#57) 
  | view on GitHub: [scripts/docs_clean.py#L57](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/docs_clean.py#L57)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20not%20recursive&body=%23%20source%0A%0A%5B%60scripts%2Fdocs_clean.py%23L57%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fdocs_clean.py%23L57%29%0A%0A%23%20context%0A%60%60%60python%0A%09%22%22%22delete%20files%20not%20in%20preserved%20set%0A%0A%09TODO%3A%20this%20is%20not%20recursive%0A%09%22%22%22%0A%09for%20path%20in%20docs_dir.iterdir%28%29%3A%0A%60%60%60&labels=enhancement)

  ```python
  	"""delete files not in preserved set
  
  	TODO: this is not recursive
  	"""
  	for path in docs_dir.iterdir():
  ```




