from io import StringIO
import ast

try:
    import yaml
except ImportError:  # pragma: nocover
    yaml = None

from .tox import parse_envlist, tox_env_to_py_version
from .travis import update_yaml_list
from ..utils import open_file, warn


APPVEYOR_YML = 'appveyor.yml'


def get_appveyor_yml_python_versions(filename=APPVEYOR_YML):
    with open_file(filename) as fp:
        conf = yaml.safe_load(fp)
    # There's more than one way of doing this, I'm setting %PYTHON% to
    # the directory that has a Python interpreter (C:\PythonXY)
    versions = []
    for env in conf['environment']['matrix']:
        for var, value in env.items():
            if var.lower() == 'python':
                versions.append(appveyor_normalize_py_version(value))
            elif var == 'TOXENV':
                toxenvs = parse_envlist(value)
                versions.extend(
                    tox_env_to_py_version(e)
                    for e in toxenvs if e.startswith('py'))
    return sorted(set(versions) - {None})


def appveyor_normalize_py_version(ver):
    ver = str(ver).lower()
    if ver.startswith('c:\\python'):
        ver = ver[len('c:\\python'):]
    elif ver.startswith('c:/python'):
        ver = ver[len('c:/python'):]
    if ver.endswith('\\'):
        ver = ver[:-1]
    if ver.endswith('-x64'):
        ver = ver[:-len('-x64')]
    if len(ver) >= 2 and ver[:2].isdigit():
        return f'{ver[0]}.{ver[1:]}'
    else:
        return None


def appveyor_detect_py_version_pattern(ver):
    ver = str(ver)
    pattern = '{}'
    for prefix in 'c:\\python', 'c:/python':
        if ver.lower().startswith(prefix):
            pos = len(prefix)
            prefix, ver = ver[:pos], ver[pos:]
            pattern = pattern.format(f'{prefix}{{}}')
            break
    if ver.endswith('\\'):
        ver = ver[:-1]
        pattern = pattern.format('{}\\')
    if ver.lower().endswith('-x64'):
        pos = -len('-x64')
        ver, suffix = ver[:pos], ver[pos:]
        pattern = pattern.format(f'{{}}{suffix}')
    if len(ver) >= 2 and ver[:2].isdigit():
        return pattern.format('{}{}')
    else:
        return None


def escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def update_appveyor_yml_python_versions(filename, new_versions):
    with open_file(filename) as fp:
        orig_lines = fp.readlines()
        fp.seek(0)
        conf = yaml.safe_load(fp)

    varname = 'PYTHON'
    patterns = set()
    for env in conf['environment']['matrix']:
        for var, value in env.items():
            if var.lower() == 'python':
                varname = var
                patterns.add(appveyor_detect_py_version_pattern(value))
                break
    patterns.discard(None)

    if not patterns:
        warn(f"Did not recognize any PYTHON environments in {fp.name}")
        return orig_lines

    quote = any(f'{varname}: "' in line for line in orig_lines)

    patterns = sorted(patterns)

    new_pythons = [
        pattern.format(*ver.split(".", 1))
        for ver in new_versions
        for pattern in patterns
    ]

    if quote:
        new_environments = [
            f'{varname}: "{escape(python)}"'
            for python in new_pythons
        ]
    else:
        new_environments = [
            f'{varname}: {python}'
            for python in new_pythons
        ]

    def keep_complicated(value):
        if value.lower().startswith('python:'):
            ver = value.partition(':')[-1].strip()
            if ver.startswith('"'):
                ver = ast.literal_eval(ver)
            ver = appveyor_normalize_py_version(ver)
            if ver is not None:
                return False
        elif value.startswith('{') and value.endswith('}'):
            env = yaml.safe_load(StringIO(value))
            for var, value in env.items():
                if var.lower() == 'python':
                    ver = appveyor_normalize_py_version(value)
                    if ver is not None and ver not in new_versions:
                        return False
        return True

    new_lines = update_yaml_list(
        orig_lines, ('environment', 'matrix'), new_environments,
        keep=keep_complicated,
    )
    return new_lines
