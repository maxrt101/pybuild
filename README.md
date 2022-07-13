# pybuild

Build tool for C++ written in python

## How to run
To build included example C++ project run `./example.py`  
To run test run `./example.py test`  
To run cppcheck run `./example.py cppcheck`  

## Example pybuild file
Simplest pybuild file could look like this:  
```python
#!/usr/bin/env python3

from pybuild.config import format as cf
import pybuild

@build.task()
def app(ctx):
    pybuild.cpp.compile(cf('{topdir}/example/src/app.cc'))
    pybuild.cpp.link_exe(
       files=[cf('{build_dir}/{profile}/obj/app.o')],
       output='app'
    )

pybuild.cli.run('app') # 'app' is default task name
```

Main executable units of pybuild are called tasks.  
To create a task define a function and annotate it with `@pybuild.task()`:  
```python
@pybuild.task()
def app(ctx):
    ...
```

Tasks can have substasks. Subtasks are annotated with `@pybuild.subtask('parent task name')`.

```python

@pybuild.task()
def lib(ctx):
    ctx.run_subtasks()
    pybuild.cpp.create_static_lib(
        files=pybuild.cpp.get_objs([
            cf('{build_dir}/{profile}/obj/utils'),
            cf('{build_dir}/{profile}/obj/core')
        ]),
        output='libexample.a'
    )

@pybuild.subtask('libff')
def core(ctx):
    pybuild.cpp.compile_batch(pybuild.utils.get_files(cf('{topdir}/src/core'), r'.+\.cc'), 'core')

@pybuild.subtask('libff')
def utils(ctx):
    pybuild.cpp.compile_batch(pybuild.utils.get_files(cf('{topdir}/src/utils'), r'.+\.cc'), 'utils')

```

Also tasks can depend on each other. Dependencies are passed as a list of task names to `build.task` annotation:  
```python

@pybuild.task()
def install_headers(ctx):
    ...

@pybuild.task()
def dependencies(ctx):
    ctx.run_subtasks()

@pybuild.task(['install_headers', 'dependencies'])
def lib(ctx):
    ...

```
