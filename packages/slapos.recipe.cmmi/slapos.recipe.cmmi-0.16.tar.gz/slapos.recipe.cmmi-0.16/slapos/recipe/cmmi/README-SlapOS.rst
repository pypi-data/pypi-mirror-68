This document describe the usages of ``slapos.recipe.cmmi`` in SlapOS.

SlapOS ``${:_profile_base_location_}`` support
==============================================

To describe this scenario, we need some packages to install.

We will install ``haproxy``, which depends on ``package`` and apply a patch
to both of them, using the typical pattern of referencing the patch by an
absolute URL that will be calculated using the ``${:_profile_base_location_}``
substitution so that it is relative to the current profile, which is what we
use to be able to install profiles directly as http URLs.

    >>> import os
    >>> src = join(os.path.dirname(__file__), 'testdata')
    >>> ls(src)
    - Foo-Bar-0.0.0.tar.gz
    - haproxy-1.4.8-dummy.tar.gz
    - package-0.0.0.tar.gz

    >>> testdata = tmpdir('testdata')
    >>> package_path = join(testdata, 'package-0.0.0.tar.gz')
    >>> os.symlink(join(src, 'package-0.0.0.tar.gz'), package_path)
    >>> haproxy_package_path = join(testdata, 'haproxy-1.4.8-dummy.tar.gz')
    >>> os.symlink(join(src, 'haproxy-1.4.8-dummy.tar.gz'), haproxy_package_path)
    >>> write('dummy.patch',
    ... '''
    ...  --- /dev/null
    ... +++ dummy.txt
    ... @@ -0,0 +1 @@
    ... +a dummy file added by a patch
    ... ''')

    >>> import subprocess
    >>> shared_dir = tmpdir('shared')
    >>> __tear_downs.insert(0, lambda: subprocess.call(
    ...     ('chmod', '-R', 'u+w', shared_dir)))

    >>> def read_installed():
    ...     import zc.buildout.configparser
    ...     with open('.installed.cfg') as f:
    ...         return zc.buildout.configparser.parse(f, '.installed.cfg')

    >>> _reset_md5sums()

We have profiles for this, they are located at URL ``URL1``.

    >>> mkdir('URL1')
    >>> write('URL1/package.cfg',
    ... """
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... patches = ${:_profile_base_location_}/../dummy.patch
    ... shared = True
    ... """ % package_path)

    >>> write('URL1/haproxy.cfg',
    ... """
    ... [buildout]
    ... extends =
    ...    ./package.cfg
    ...
    ... [haproxy]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... patches = ${:_profile_base_location_}/../dummy.patch
    ... shared = True
    ... environment=
    ...    CFLAGS=-I${package:location}/include/
    ... """ % package_path)


We have a buildout using these profiles from ``URL1``:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... extends =
    ...    URL1/haproxy.cfg
    ... parts = haproxy
    ... shared-part-list = %s
    ...
    ... """ % shared_dir)

    >>> print(system(buildout))
    package: shared at /shared/package/<MD5SUM:0>
    haproxy: shared at /shared/haproxy/<MD5SUM:1>
    Installing package.
    package: Checking whether package is installed at shared path: /shared/package/<MD5SUM:0>
    package: Applying patches
    patching file dummy.txt
    configure --prefix=/shared/package/<MD5SUM:0>
    building package
    installing package
    Installing haproxy.
    haproxy: Checking whether package is installed at shared path: /shared/haproxy/<MD5SUM:1>
    haproxy: [ENV] CFLAGS = /shared/package/<MD5SUM:0>/include/
    haproxy: Applying patches
    patching file dummy.txt
    configure --prefix=/shared/haproxy/<MD5SUM:1>
    building package
    installing package

When we ran this buildout, it installed a first version of the packages, in directories named
after the hash calculated from their options and from their buildout signature.

    >>> first_haproxy_location = read_installed()['haproxy']['location']
    >>> first_haproxy_location
    '/shared/haproxy/<MD5SUM:1>'


We create another version of the profiles for components at ``URL2``. There are
no differences with the previous version, only the URL is different.

    >>> mkdir('URL2')
    >>> import shutil
    >>> _ = shutil.copy('URL1/package.cfg', 'URL2/package.cfg')
    >>> _ = shutil.copy('URL1/haproxy.cfg', 'URL2/haproxy.cfg')

We update our buildout to use the new URL:

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... extends =
    ...    URL2/haproxy.cfg
    ... parts = haproxy
    ... shared-part-list = %s
    ...
    ... """ % shared_dir)

When buildout runs again, since the packages are same they are reused from their shared parts
and not installed again.

    >>> print(system(buildout))
    package: shared at /shared/package/<MD5SUM:0>
    haproxy: shared at /shared/haproxy/<MD5SUM:1>
    Uninstalling haproxy.
    Uninstalling package.
    Installing package.
    package: Checking whether package is installed at shared path: /shared/package/<MD5SUM:0>
    package: This shared package has been installed by other package
    Installing haproxy.
    haproxy: Checking whether package is installed at shared path: /shared/haproxy/<MD5SUM:1>
    haproxy: This shared package has been installed by other package


On the other hand, if the ``package`` becomes different, then it will be re-installed at another
shared location and ``haproxy``, which depend on ``package`` will also be re-installed.

    >>> write('URL2/package.cfg',
    ... """
    ... [package]
    ... recipe = slapos.recipe.cmmi
    ... url = file://%s
    ... # no patch this time
    ... shared = True
    ... """ % package_path)

    >>> print(system(buildout))
    package: shared at /shared/package/<MD5SUM:2>
    haproxy: shared at /shared/haproxy/<MD5SUM:3>
    Uninstalling haproxy.
    Uninstalling package.
    Installing package.
    package: Checking whether package is installed at shared path: /shared/package/<MD5SUM:2>
    configure --prefix=/shared/package/<MD5SUM:2>
    building package
    installing package
    Installing haproxy.
    haproxy: Checking whether package is installed at shared path: /shared/haproxy/<MD5SUM:3>
    haproxy: [ENV] CFLAGS = /shared/package/<MD5SUM:2>/include/
    haproxy: Applying patches
    patching file dummy.txt
    configure --prefix=/shared/haproxy/<MD5SUM:3>
    building package
    installing package


Shared parts signatures for tooling
===================================

Because shared parts are never uninstalled by buildout, the more we build different
parts, the more we have directories in share parts folder, each representing a package
that was built with different build options:

    >>> ls(join(shared_dir, 'haproxy')) # doctest: +ELLIPSIS
    d ...<MD5SUM:1>...
    >>> ls(join(shared_dir, 'haproxy')) # doctest: +ELLIPSIS
    d ...<MD5SUM:3>...

We have a tool to delete unused shared parts, ``slapos node prune``, which rely on the
MD5SUM signatures of shared parts.

By examining buildout's installed database, we can see it's a simple text file containing
the hashes of both ``haproxy`` and ``package`` and this is what the tool uses to know
that the shared parts are used by this buildout:

    >>> cat('.installed.cfg') # doctest: +ELLIPSIS
    [buildout]
    ...<MD5SUM:2>...
    >>> cat('.installed.cfg') # doctest: +ELLIPSIS
    [buildout]
    ...<MD5SUM:3>...

Of course, the first version of ``haproxy`` that is not longer used is not referred here, so our
tool will be able to delete this previous version of ``haproxy``.

    >>> with open('.installed.cfg') as f:
    ...   installed_cfg = f.read()
    >>> first_haproxy_location in installed_cfg
    False

We also needed something to know the dependences between shared parts. For this, we are using
``.slapos.recipe.cmmi.signature`` files in folders where shared parts are installed. Because
``haproxy`` depends on ``package`` version ``<MD5SUM:2>``, we can see ``<MD5SUM:2>`` in its
signature file.

    >>> haproxy_location = read_installed()['haproxy']['location']
    >>> haproxy_location
    '/shared/haproxy/<MD5SUM:3>'
    >>> cat(join(haproxy_location, '.slapos.recipe.cmmi.signature')) # doctest: +ELLIPSIS
    '__buildout_signature__': ...
    ...<MD5SUM:2>...

This is also useful during testing, we check that signatures do not have references to non-shared parts.
