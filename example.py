#!/usr/bin/env python3

from pybuild.config import format as cf
import pybuild, os, shutil

@pybuild.config.feature_handler
def features(profile, feature_list):
    if 'DEBUG' in feature_list: pybuild.config.get('cpp', 'cxxflags').append('-D_DEBUG')
 
@pybuild.task()
def install_headers(ctx):
    src, dst = cf('{topdir}/example/include'), cf('{build_dir}/{profile}/include')
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    pybuild.utils.copytree(src, dst)

@pybuild.task(['lib'])
def app(ctx):
    pybuild.cpp.compile(cf('{topdir}/example/src/app.cc'))
    pybuild.cpp.link_exe(
       files=[cf('{build_dir}/{profile}/obj/app.o')],
       output='app',
       libs=['example']
    )

@pybuild.task(['install_headers'])
def lib(ctx):
    pybuild.cpp.compile(cf('{topdir}/example/src/lib.cc'))
    pybuild.cpp.create_static_lib(
        files=[cf('{build_dir}/{profile}/obj/lib.o')],
        output='libexample.a'
    )

@pybuild.task()
def clean(ctx):
    shutil.rmtree(cf('{build_dir}/{profile}'))

@pybuild.task()
def cppcheck(ctx):
    pybuild.run_cmd([
        'cppcheck',
        '--enable=all',
        '--error-exitcode=1',
        cf('-I{build_dir}/{profile}/include'),
        cf('{topdir}/example/src')
    ], print_stdout=True, print_stderr=True)

@pybuild.task()
def test(ctx):
    pybuild.run_cmd(
        [cf('{build_dir}/{profile}/bin/app'), 'pybuild'],
        exit_on_fail=True,
        print_stderr=True,
        print_stdout=True
    )

pybuild.cli.run('app')
