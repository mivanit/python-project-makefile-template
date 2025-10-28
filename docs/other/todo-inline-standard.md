 # Inline TODOs


# BUG

## [`myproject/other.py`](/myproject/other.py)

- make todo should see this too  
  local link: [`/myproject/other.py:4`](/myproject/other.py#L4) 
  | view on GitHub: [myproject/other.py#L4](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/other.py#L4)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=make%20todo%20should%20see%20this%20too&body=%23%20source%0A%0A%5B%60myproject%2Fother.py%23L4%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fother.py%23L4%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20BUG%3A%20make%20todo%20should%20see%20this%20too%0Adef%20another_function%28%29%20-%3E%20None%3A%0A%09%22dummy%20docstring%22%0A%60%60%60&labels=bug)

  ```python
  # BUG: make todo should see this too
  def another_function() -> None:
  	"dummy docstring"
  ```





# FIXME

## [`myproject/helloworld.py`](/myproject/helloworld.py)

- an example that `make todo` should find  
  local link: [`/myproject/helloworld.py:13`](/myproject/helloworld.py#L13) 
  | view on GitHub: [myproject/helloworld.py#L13](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/helloworld.py#L13)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=an%20example%20that%20%60make%20todo%60%20should%20find&body=%23%20source%0A%0A%5B%60myproject%2Fhelloworld.py%23L13%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fhelloworld.py%23L13%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20FIXME%3A%20an%20example%20that%20%60make%20todo%60%20should%20find%0Adef%20critical_function%28%29%20-%3E%20None%3A%0A%09%22dummy%20docstring%22%0A%60%60%60&labels=FIXME)

  ```python
  # FIXME: an example that `make todo` should find
  def critical_function() -> None:
  	"dummy docstring"
  ```





# HACK

## [`scripts/make_docs.py`](/scripts/make_docs.py)

- this is kid of fragile  
  local link: [`/scripts/make_docs.py:149`](/scripts/make_docs.py#L149) 
  | view on GitHub: [scripts/make_docs.py#L149](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/make_docs.py#L149)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20kid%20of%20fragile&body=%23%20source%0A%0A%5B%60scripts%2Fmake_docs.py%23L149%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fmake_docs.py%23L149%29%0A%0A%23%20context%0A%60%60%60python%0A%09%09%22%22%22name%20of%20the%20module%2C%20which%20is%20the%20package%20name%20with%20%27-%27%20replaced%20by%20%27_%27%0A%0A%09%09HACK%3A%20this%20is%20kid%20of%20fragile%0A%09%09%22%22%22%0A%09%09return%20self.package_name.replace%28%22-%22%2C%20%22_%22%29%0A%60%60%60&labels=HACK)

  ```python
  """name of the module, which is the package name with '-' replaced by '_'

  HACK: this is kid of fragile
  """
  return self.package_name.replace("-", "_")
  ```





# TODO

## [`myproject/helloworld.py`](/myproject/helloworld.py)

- an example todo that `make todo` should find  
  local link: [`/myproject/helloworld.py:7`](/myproject/helloworld.py#L7) 
  | view on GitHub: [myproject/helloworld.py#L7](https://github.com/mivanit/python-project-makefile-template/blob/main/myproject/helloworld.py#L7)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=an%20example%20todo%20that%20%60make%20todo%60%20should%20find&body=%23%20source%0A%0A%5B%60myproject%2Fhelloworld.py%23L7%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fhelloworld.py%23L7%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20another%20line%20which%20should%20be%20included%20in%20the%20body%0A%23%20TODO%3A%20an%20example%20todo%20that%20%60make%20todo%60%20should%20find%0Adef%20some_function%28%29%20-%3E%20None%3A%0A%09%22dummy%20docstring%22%0A%60%60%60&labels=enhancement)

  ```python
  # another line which should be included in the body
  # TODO: an example todo that `make todo` should find
  def some_function() -> None:
  	"dummy docstring"
  ```




## [`README.md`](/README.md)

- switch to [`ty`](https://github.com/astral-sh/ty) once it's more mature  
  local link: [`/README.md:11`](/README.md#L11) 
  | view on GitHub: [README.md#L11](https://github.com/mivanit/python-project-makefile-template/blob/main/README.md#L11)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=switch%20to%20%5B%60ty%60%5D%28https%3A%2F%2Fgithub.com%2Fastral-sh%2Fty%29%20once%20it%27s%20more%20mature&body=%23%20source%0A%0A%5B%60README.md%23L11%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2FREADME.md%23L11%29%0A%0A%23%20context%0A%60%60%60markdown%0A-%20%5B%60pytest%60%5D%28https%3A%2F%2Fdocs.pytest.org%29%20for%20testing%0A-%20%5B%60mypy%60%5D%28https%3A%2F%2Fgithub.com%2Fpython%2Fmypy%29%20for%20static%20type%20checking%0A%20%20-%20TODO%3A%20switch%20to%20%5B%60ty%60%5D%28https%3A%2F%2Fgithub.com%2Fastral-sh%2Fty%29%20once%20it%27s%20more%20mature%0A-%20%5B%60ruff%60%5D%28https%3A%2F%2Fdocs.astral.sh%2Fruff%2F%29%20for%20formatting%0A-%20%5B%60pdoc%60%5D%28https%3A%2F%2Fpdoc.dev%29%20for%20documentation%20generation%0A%60%60%60&labels=enhancement)

  ```markdown
  - [`pytest`](https://docs.pytest.org) for testing
  - [`mypy`](https://github.com/python/mypy) for static type checking
    - TODO: switch to [`ty`](https://github.com/astral-sh/ty) once it's more mature
  - [`ruff`](https://docs.astral.sh/ruff/) for formatting
  - [`pdoc`](https://pdoc.dev) for documentation generation
  ```




## [`scripts/make/docs_clean.py`](/scripts/make/docs_clean.py)

- this is not recursive  
  local link: [`/scripts/make/docs_clean.py:55`](/scripts/make/docs_clean.py#L55) 
  | view on GitHub: [scripts/make/docs_clean.py#L55](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/make/docs_clean.py#L55)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20not%20recursive&body=%23%20source%0A%0A%5B%60scripts%2Fmake%2Fdocs_clean.py%23L55%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fmake%2Fdocs_clean.py%23L55%29%0A%0A%23%20context%0A%60%60%60python%0A%09%22%22%22delete%20files%20not%20in%20preserved%20set%0A%0A%09TODO%3A%20this%20is%20not%20recursive%0A%09%22%22%22%0A%09for%20path%20in%20docs_dir.iterdir%28%29%3A%0A%60%60%60&labels=enhancement)

  ```python
  """delete files not in preserved set

  TODO: this is not recursive
  """
  for path in docs_dir.iterdir():
  ```




## [`scripts/make/get_todos.py`](/scripts/make/get_todos.py)

- type comments and write them to markdown, jsonl, html. configurable in pyproject.toml"  
  local link: [`/scripts/make/get_todos.py:1`](/scripts/make/get_todos.py#L1) 
  | view on GitHub: [scripts/make/get_todos.py#L1](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/make/get_todos.py#L1)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=type%20comments%20and%20write%20them%20to%20markdown%2C%20jsonl%2C%20html.%20configurable%20in%20pyproject.toml%22&body=%23%20source%0A%0A%5B%60scripts%2Fmake%2Fget_todos.py%23L1%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fmake%2Fget_todos.py%23L1%29%0A%0A%23%20context%0A%60%60%60python%0A%22read%20all%20TODO%20type%20comments%20and%20write%20them%20to%20markdown%2C%20jsonl%2C%20html.%20configurable%20in%20pyproject.toml%22%0A%0Afrom%20__future__%20import%20annotations%0A%60%60%60&labels=enhancement)

  ```python
  "read all TODO type comments and write them to markdown, jsonl, html. configurable in pyproject.toml"

  from __future__ import annotations
  ```




