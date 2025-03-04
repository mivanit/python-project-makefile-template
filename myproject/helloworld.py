"dummy module"

print("hello world")


# another line which should be included in the body
# TODO: an example todo that `make todo` should find
def some_function() -> None:
	"dummy docstring"
	raise NotImplementedError("This function is not implemented yet")


# FIXME: an example that `make todo` should find
def critical_function() -> None:
	"dummy docstring"
	raise NotImplementedError("This function is not implemented yet")
