#!/usr/bin/env python3

from build.config import format as cf
import build, os, shutil

@build.config.feature_handler
def features(profile, feature_list):
    if 'DEBUG' in feature_list: build.config.get('cpp', 'cxxflags').append('-D_DEBUG')
 
@build.task()
def install_headers(ctx):
    src, dst = cf('{topdir}/example/include'), cf('{build_dir}/{profile}/include')
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    build.utils.copytree(src, dst)

@build.task(['lib'])
def app(ctx):
    build.cpp.compile(cf('{topdir}/example/src/app.cc'))
    build.cpp.link_exe(
       files=[cf('{build_dir}/{profile}/obj/app.o')],
       output='app',
       libs=['example']
    )

@build.task(['install_headers'])
def lib(ctx):
    build.cpp.compile(cf('{topdir}/example/src/lib.cc'))
    build.cpp.create_static_lib(
        files=[cf('{build_dir}/{profile}/obj/lib.o')],
        output='libexample.a'
    )

@build.task()
def clean(ctx):
    shutil.rmtree(cf('{build_dir}/{profile}'))

@build.task()
def cppcheck(ctx):
    build.run_cmd([
        'cppcheck',
        '--enable=all',
        '--error-exitcode=1',
        cf('-I{build_dir}/{profile}/include'),
        cf('{topdir}/example/src')
    ], print_stdout=True, print_stderr=True)

@build.task()
def test(ctx):
    build.run_cmd(
        [cf('{build_dir}/{profile}/bin/app'), 'pybuild'],
        exit_on_fail=True,
        print_stderr=True,
        print_stdout=True
    )

build.cli.run('app')
