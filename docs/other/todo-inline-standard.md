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
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=an%20example%20that%20%60make%20todo%60%20should%20find&body=%23%20source%0A%0A%5B%60myproject%2Fhelloworld.py%23L13%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fmyproject%2Fhelloworld.py%23L13%29%0A%0A%23%20context%0A%60%60%60python%0A%23%20FIXME%3A%20an%20example%20that%20%60make%20todo%60%20should%20find%0Adef%20critical_function%28%29%20-%3E%20None%3A%0A%09%22dummy%20docstring%22%0A%60%60%60&labels=bug)

  ```python
  # FIXME: an example that `make todo` should find
  def critical_function() -> None:
  	"dummy docstring"
  ```





# HACK

## [`.meta/scripts/make_docs.py`](/.meta/scripts/make_docs.py)

- this is kind of fragile  
  local link: [`/.meta/scripts/make_docs.py:152`](/.meta/scripts/make_docs.py#L152) 
  | view on GitHub: [.meta/scripts/make_docs.py#L152](https://github.com/mivanit/python-project-makefile-template/blob/main/.meta/scripts/make_docs.py#L152)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20kind%20of%20fragile&body=%23%20source%0A%0A%5B%60.meta%2Fscripts%2Fmake_docs.py%23L152%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2F.meta%2Fscripts%2Fmake_docs.py%23L152%29%0A%0A%23%20context%0A%60%60%60python%0A%09%09%22%22%22name%20of%20the%20module%2C%20which%20is%20the%20package%20name%20with%20%27-%27%20replaced%20by%20%27_%27%0A%0A%09%09HACK%3A%20this%20is%20kind%20of%20fragile%0A%09%09%22%22%22%0A%09%09return%20self.package_name.replace%28%22-%22%2C%20%22_%22%29%0A%60%60%60&labels=enhancement)

  ```python
  """name of the module, which is the package name with '-' replaced by '_'

  HACK: this is kind of fragile
  """
  return self.package_name.replace("-", "_")
  ```




## [`scripts/make/make_docs.py`](/scripts/make/make_docs.py)

- this is kind of fragile  
  local link: [`/scripts/make/make_docs.py:152`](/scripts/make/make_docs.py#L152) 
  | view on GitHub: [scripts/make/make_docs.py#L152](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/make/make_docs.py#L152)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20kind%20of%20fragile&body=%23%20source%0A%0A%5B%60scripts%2Fmake%2Fmake_docs.py%23L152%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fmake%2Fmake_docs.py%23L152%29%0A%0A%23%20context%0A%60%60%60python%0A%09%09%22%22%22name%20of%20the%20module%2C%20which%20is%20the%20package%20name%20with%20%27-%27%20replaced%20by%20%27_%27%0A%0A%09%09HACK%3A%20this%20is%20kind%20of%20fragile%0A%09%09%22%22%22%0A%09%09return%20self.package_name.replace%28%22-%22%2C%20%22_%22%29%0A%60%60%60&labels=enhancement)

  ```python
  """name of the module, which is the package name with '-' replaced by '_'

  HACK: this is kind of fragile
  """
  return self.package_name.replace("-", "_")
  ```




## [`scripts/out/make_docs.py`](/scripts/out/make_docs.py)

- this is kind of fragile  
  local link: [`/scripts/out/make_docs.py:152`](/scripts/out/make_docs.py#L152) 
  | view on GitHub: [scripts/out/make_docs.py#L152](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/out/make_docs.py#L152)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20kind%20of%20fragile&body=%23%20source%0A%0A%5B%60scripts%2Fout%2Fmake_docs.py%23L152%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fout%2Fmake_docs.py%23L152%29%0A%0A%23%20context%0A%60%60%60python%0A%09%09%22%22%22name%20of%20the%20module%2C%20which%20is%20the%20package%20name%20with%20%27-%27%20replaced%20by%20%27_%27%0A%0A%09%09HACK%3A%20this%20is%20kind%20of%20fragile%0A%09%09%22%22%22%0A%09%09return%20self.package_name.replace%28%22-%22%2C%20%22_%22%29%0A%60%60%60&labels=enhancement)

  ```python
  """name of the module, which is the package name with '-' replaced by '_'

  HACK: this is kind of fragile
  """
  return self.package_name.replace("-", "_")
  ```





# TODO

## [`.meta/scripts/docs_clean.py`](/.meta/scripts/docs_clean.py)

- this is not recursive  
  local link: [`/.meta/scripts/docs_clean.py:71`](/.meta/scripts/docs_clean.py#L71) 
  | view on GitHub: [.meta/scripts/docs_clean.py#L71](https://github.com/mivanit/python-project-makefile-template/blob/main/.meta/scripts/docs_clean.py#L71)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20not%20recursive&body=%23%20source%0A%0A%5B%60.meta%2Fscripts%2Fdocs_clean.py%23L71%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2F.meta%2Fscripts%2Fdocs_clean.py%23L71%29%0A%0A%23%20context%0A%60%60%60python%0A%09%22%22%22delete%20files%20not%20in%20preserved%20set%0A%0A%09TODO%3A%20this%20is%20not%20recursive%0A%09%22%22%22%0A%09for%20path%20in%20docs_dir.iterdir%28%29%3A%0A%60%60%60&labels=enhancement)

  ```python
  """delete files not in preserved set

  TODO: this is not recursive
  """
  for path in docs_dir.iterdir():
  ```




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

- Extraction  
  local link: [`/README.md:257`](/README.md#L257) 
  | view on GitHub: [README.md#L257](https://github.com/mivanit/python-project-makefile-template/blob/main/README.md#L257)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=Extraction&body=%23%20source%0A%0A%5B%60README.md%23L257%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2FREADME.md%23L257%29%0A%0A%23%20context%0A%60%60%60markdown%0A%60%60%60%0A%0A%23%23%20%60%5Btool.makefile.inline-todo%5D%60%20-%20TODO%20Extraction%0A%0ASettings%20for%20%60make%20todo%60%20which%20finds%20TODO%2FFIXME%2FBUG%20comments%20and%20generates%20reports%3A%0A%60%60%60&labels=enhancement)

  ```markdown
  ```

  ## `[tool.makefile.inline-todo]` - TODO Extraction

  Settings for `make todo` which finds TODO/FIXME/BUG comments and generates reports:
  ```




## [`scripts/make/docs_clean.py`](/scripts/make/docs_clean.py)

- this is not recursive  
  local link: [`/scripts/make/docs_clean.py:71`](/scripts/make/docs_clean.py#L71) 
  | view on GitHub: [scripts/make/docs_clean.py#L71](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/make/docs_clean.py#L71)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20not%20recursive&body=%23%20source%0A%0A%5B%60scripts%2Fmake%2Fdocs_clean.py%23L71%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fmake%2Fdocs_clean.py%23L71%29%0A%0A%23%20context%0A%60%60%60python%0A%09%22%22%22delete%20files%20not%20in%20preserved%20set%0A%0A%09TODO%3A%20this%20is%20not%20recursive%0A%09%22%22%22%0A%09for%20path%20in%20docs_dir.iterdir%28%29%3A%0A%60%60%60&labels=enhancement)

  ```python
  """delete files not in preserved set

  TODO: this is not recursive
  """
  for path in docs_dir.iterdir():
  ```




## [`scripts/out/docs_clean.py`](/scripts/out/docs_clean.py)

- this is not recursive  
  local link: [`/scripts/out/docs_clean.py:71`](/scripts/out/docs_clean.py#L71) 
  | view on GitHub: [scripts/out/docs_clean.py#L71](https://github.com/mivanit/python-project-makefile-template/blob/main/scripts/out/docs_clean.py#L71)
  | [Make Issue](https://github.com/mivanit/python-project-makefile-template/issues/new?title=this%20is%20not%20recursive&body=%23%20source%0A%0A%5B%60scripts%2Fout%2Fdocs_clean.py%23L71%60%5D%28https%3A%2F%2Fgithub.com%2Fmivanit%2Fpython-project-makefile-template%2Fblob%2Fmain%2Fscripts%2Fout%2Fdocs_clean.py%23L71%29%0A%0A%23%20context%0A%60%60%60python%0A%09%22%22%22delete%20files%20not%20in%20preserved%20set%0A%0A%09TODO%3A%20this%20is%20not%20recursive%0A%09%22%22%22%0A%09for%20path%20in%20docs_dir.iterdir%28%29%3A%0A%60%60%60&labels=enhancement)

  ```python
  """delete files not in preserved set

  TODO: this is not recursive
  """
  for path in docs_dir.iterdir():
  ```




