import argparse
import os
import sys
from io import StringIO

from . import __version__
from .utils import confirm_and_update_file, show_diff
from .versions import (
    MAX_MINOR_FOR_MAJOR,
    important,
    update_version_list,
)
from .parsers.python import (
    get_supported_python_versions,
    get_python_requires,
    update_python_requires,
    update_supported_python_versions,
)
from .parsers.tox import (
    TOX_INI,
    get_tox_ini_python_versions,
    update_tox_ini_python_versions,
)
from .parsers.travis import (
    TRAVIS_YML,
    get_travis_yml_python_versions,
    update_travis_yml_python_versions,
)
from .parsers.appveyor import (
    APPVEYOR_YML,
    get_appveyor_yml_python_versions,
    update_appveyor_yml_python_versions,
)
from .parsers.manylinux import (
    MANYLINUX_INSTALL_SH,
    get_manylinux_python_versions,
    update_manylinux_python_versions,
)

try:
    import yaml
except ImportError:  # pragma: nocover
    # Shouldn't happen, we install_requires=['PyYAML'], but maybe someone is
    # running ./check-python-versions directly from a git checkout.
    yaml = None
    print("PyYAML is needed for Travis CI/Appveyor support"
          " (apt install python3-yaml)")


def parse_version(v):
    try:
        major, minor = map(int, v.split('.', 1))
    except ValueError:
        raise argparse.ArgumentTypeError(f'bad version: {v}')
    return (major, minor)


def parse_version_list(v):
    versions = set()

    for part in v.split(','):
        if '-' in part:
            lo, hi = part.split('-', 1)
        else:
            lo = hi = part

        if lo and hi:
            lo_major, lo_minor = parse_version(lo)
            hi_major, hi_minor = parse_version(hi)
        elif hi and not lo:
            hi_major, hi_minor = parse_version(hi)
            lo_major, lo_minor = hi_major, 0
        elif lo and not hi:
            lo_major, lo_minor = parse_version(lo)
            try:
                hi_major, hi_minor = lo_major, MAX_MINOR_FOR_MAJOR[lo_major]
            except KeyError:
                raise argparse.ArgumentTypeError(
                    f'bad range: {part}')
        else:
            raise argparse.ArgumentTypeError(
                f'bad range: {part}')

        if lo_major != hi_major:
            raise argparse.ArgumentTypeError(
                f'bad range: {part} ({lo_major} != {hi_major})')

        for v in range(lo_minor, hi_minor + 1):
            versions.add(f'{lo_major}.{v}')

    return sorted(versions)


def is_package(where='.'):
    setup_py = os.path.join(where, 'setup.py')
    return os.path.exists(setup_py)


def check_package(where='.', *, print=print):

    if not os.path.isdir(where):
        print("not a directory")
        return False

    setup_py = os.path.join(where, 'setup.py')
    if not os.path.exists(setup_py):
        print("no setup.py -- not a Python package?")
        return False

    return True


def filename_or_replacement(pathname, replacements):
    if replacements and pathname in replacements:
        new_lines = replacements[pathname]
        buf = StringIO("".join(new_lines))
        buf.name = pathname
        return buf
    else:
        return pathname


def check_versions(where='.', *, print=print, expect=None, replacements=None,
                   only=None):

    sources = [
        ('setup.py', get_supported_python_versions, 'setup.py'),
        ('- python_requires', get_python_requires, 'setup.py'),
        (TOX_INI, get_tox_ini_python_versions, TOX_INI),
        (TRAVIS_YML, get_travis_yml_python_versions, TRAVIS_YML),
        (APPVEYOR_YML, get_appveyor_yml_python_versions, APPVEYOR_YML),
        (MANYLINUX_INSTALL_SH, get_manylinux_python_versions,
         MANYLINUX_INSTALL_SH),
    ]

    width = max(len(title) for title, *etc in sources) + len(" says:")

    version_sets = []

    for (title, extractor, filename) in sources:
        if only and filename not in only:
            continue
        pathname = os.path.join(where, filename)
        if not os.path.exists(pathname):
            continue
        versions = extractor(filename_or_replacement(pathname, replacements))
        if versions is None:
            continue
        print(f"{title} says:".ljust(width), ", ".join(versions) or "(empty)")
        version_sets.append(important(versions))

    if not expect:
        expect = version_sets[0]
    else:
        print("expected:".ljust(width), ', '.join(expect))

    expect = important(expect)
    return all(
        expect == v for v in version_sets
    )


def update_versions(where='.', *, add=None, drop=None, update=None,
                    diff=False, dry_run=False, only=None):

    sources = [
        ('setup.py', get_supported_python_versions,
         update_supported_python_versions),
        ('setup.py', get_python_requires,
         update_python_requires),
        (TOX_INI, get_tox_ini_python_versions,
         update_tox_ini_python_versions),
        (TRAVIS_YML, get_travis_yml_python_versions,
         update_travis_yml_python_versions),
        (APPVEYOR_YML, get_appveyor_yml_python_versions,
         update_appveyor_yml_python_versions),
        (MANYLINUX_INSTALL_SH, get_manylinux_python_versions,
         update_manylinux_python_versions),
        # TODO: CHANGES.rst
    ]
    replacements = {}

    for (filename, extractor, updater) in sources:
        if only and filename not in only:
            continue
        pathname = os.path.join(where, filename)
        if not os.path.exists(pathname):
            continue
        versions = extractor(filename_or_replacement(pathname, replacements))
        if versions is None:
            continue

        versions = sorted(important(versions))
        new_versions = update_version_list(
            versions, add=add, drop=drop, update=update)
        if versions != new_versions:
            fp = filename_or_replacement(pathname, replacements)
            new_lines = updater(fp, new_versions)
            if new_lines is not None:
                if diff:
                    fp = filename_or_replacement(pathname, replacements)
                    show_diff(fp, new_lines)
                if dry_run:
                    replacements[pathname] = new_lines
                if not diff and not dry_run:
                    confirm_and_update_file(pathname, new_lines)

    return replacements


def _main():
    parser = argparse.ArgumentParser(
        description="verify that supported Python versions are the same"
                    " in setup.py, tox.ini, .travis.yml and appveyor.yml")
    parser.add_argument('--version', action='version',
                        version="%(prog)s version " + __version__)
    parser.add_argument('--expect', metavar='VERSIONS',
                        type=parse_version_list,
                        help='expect these versions to be supported, e.g.'
                             ' --expect 2.7,3.5-3.7')
    parser.add_argument('--skip-non-packages', action='store_true',
                        help='skip arguments that are not Python packages'
                             ' without warning about them')
    parser.add_argument('--only', metavar='FILES',
                        help='check only the specified files'
                             ' (comma-separated list, e.g.'
                             ' --only tox.ini,appveyor.yml)')
    parser.add_argument('where', nargs='*',
                        help='directory where a Python package with a setup.py'
                             ' and other files is located')
    group = parser.add_argument_group(
        "updating supported version lists (EXPERIMENTAL)")
    group.add_argument('--add', metavar='VERSIONS', type=parse_version_list,
                       help='add these versions to supported ones, e.g'
                            ' --add 3.8')
    group.add_argument('--drop', metavar='VERSIONS', type=parse_version_list,
                       help='drop these versions from supported ones, e.g'
                            ' --drop 2.6,3.4')
    group.add_argument('--update', metavar='VERSIONS', type=parse_version_list,
                       help='update the set of supported versions, e.g.'
                            ' --update 2.7,3.5-3.7')
    group.add_argument('--diff', action='store_true',
                       help='show a diff of proposed changes')
    group.add_argument('--dry-run', action='store_true',
                       help='verify proposed changes without'
                            ' writing them to disk')
    args = parser.parse_args()

    if args.update and args.add:
        parser.error("argument --add: not allowed with argument --update")
    if args.update and args.drop:
        parser.error("argument --drop: not allowed with argument --update")
    if args.diff and not (args.update or args.add or args.drop):
        parser.error(
            "argument --diff: not allowed without --update/--add/--drop")
    if args.dry_run and not (args.update or args.add or args.drop):
        parser.error(
            "argument --dry-run: not allowed without --update/--add/--drop")
    if args.expect and args.diff and not args.dry_run:
        parser.error(
            "argument --expect: not allowed with --diff,"
            " unless you also add --dry-run")

    where = args.where or ['.']
    if args.skip_non_packages:
        where = [path for path in where if is_package(path)]

    only = [a.strip() for a in args.only.split(',')] if args.only else None

    multiple = len(where) > 1
    mismatches = []
    for n, path in enumerate(where):
        if multiple and (not args.diff or args.dry_run):
            if n:
                print("\n")
            print(f"{path}:\n")
        if not check_package(path):
            mismatches.append(path)
            continue
        replacements = {}
        if args.add or args.drop or args.update:
            replacements = update_versions(
                path, add=args.add, drop=args.drop,
                update=args.update, diff=args.diff,
                dry_run=args.dry_run, only=only)
        if not args.diff or args.dry_run:
            if not check_versions(path, expect=args.expect,
                                  replacements=replacements,
                                  only=only):
                mismatches.append(path)
                continue

    if not args.diff or args.dry_run:
        if mismatches:
            if multiple:
                sys.exit(f"\n\nmismatch in {' '.join(mismatches)}!")
            else:
                sys.exit("\nmismatch!")
        elif multiple:
            print("\n\nall ok!")


def main():
    try:
        _main()
    except KeyboardInterrupt:
        sys.exit(2)
