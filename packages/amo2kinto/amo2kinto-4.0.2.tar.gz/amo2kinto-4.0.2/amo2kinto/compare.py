# This file is taken as is from Olympia addons-server source code.
#
# https://github.com/mozilla/addons-server/
# - src/olympia/versions/compare.py
import re

MAXVERSION = 2 ** 63 - 1

version_re = re.compile(r"""(?P<major>\d+|\*)      # major (x in x.y)
                            \.?(?P<minor1>\d+|\*)? # minor1 (y in x.y)
                            \.?(?P<minor2>\d+|\*)? # minor2 (z in x.y.z)
                            \.?(?P<minor3>\d+|\*)? # minor3 (w in x.y.z.w)
                            (?P<alpha>[a|b]?)      # alpha/beta
                            (?P<alpha_ver>\d*)     # alpha/beta version
                            (?P<pre>pre)?          # pre release
                            (?P<pre_ver>\d)?       # pre release version
                        """,
                        re.VERBOSE)


def version_dict(version):
    """Turn a version string into a dict with major/minor/... info."""
    match = version_re.match(str(version) or '')
    letters = 'alpha pre'.split()
    numbers = 'major minor1 minor2 minor3 alpha_ver pre_ver'.split()
    if match:
        d = match.groupdict()
        for letter in letters:
            d[letter] = d[letter] if d[letter] else None
        for num in numbers:
            if d[num] == '*':
                d[num] = 99
            else:
                d[num] = int(d[num]) if d[num] else None
    else:
        d = dict((k, None) for k in numbers)
        d.update((k, None) for k in letters)
    return d


def version_int(version):
    if isinstance(version, bytes):  # pragma: no cover
        version = version.decode('utf-8')

    d = version_dict(version)
    for key in ['alpha_ver', 'major', 'minor1', 'minor2', 'minor3',
                'pre_ver']:
        if not d[key]:
            d[key] = 0
    atrans = {'a': 0, 'b': 1}
    d['alpha'] = atrans.get(d['alpha'], 2)
    d['pre'] = 0 if d['pre'] else 1

    v = "%d%02d%02d%02d%d%02d%d%02d" % (
        d['major'], d['minor1'], d['minor2'], d['minor3'], d['alpha'],
        d['alpha_ver'], d['pre'], d['pre_ver'])
    return min(int(v), MAXVERSION)
