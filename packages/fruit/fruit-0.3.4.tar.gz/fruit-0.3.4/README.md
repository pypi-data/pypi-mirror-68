# Fruit

Fruit is an automation framework written in python.

## Configuration

Fruit, when installed via pip, can be called via the command `fruit` from the 
terminal. 

### Targets

Targets are entry points of the **fruit make** process. They may be executed with the command `fruit make <target>` from the command line.

Each target may consist of multiple steps or even multiple sub targets. Each of these elemts will be automatically detected during the execution of a target. All sub targets and steps will be automatically listed and added to the result tracking of the called target.

To create a new target, use the decorator `@fruit.target()`.

The following example will create a target with the name `build` and an empty
help text.

```python
@fruit.target()
def build():
  pass
```

The name and the help text of the target can be overwritten by using the argumetns `name` and `help` of `@fruit.target()`.

```python
# Create a target with the name 'build-new'
@fruit.target(name='build-new', help='Build a new castle')
def build():
  pass
```

The target results will be generated during the target execution process and the results will be shown after target is finished. May the target process be aborted, the results will show the unsuccessful execution with the proper error message.

### Steps

Steps are the parts of targets and they serve diagnostic purposes and ease the
generation of detailed reports. They are not mandatory to define, but the provide nice diagnostics and cli output for longer processes.

Steps can be created by using the decorator `@fruit.step()`. The step name will be the name of the decorated function by default but it can be overwritten
by the argument `name`.

```python
# Create a step called step1 without help text
@fruit.step()
def step1():
  pass

# Create a step called 'GIT version' with help text
@fruit.step(name='GIT version', help='Get the current version of the GIT repo')
def step2():
  pass
```

