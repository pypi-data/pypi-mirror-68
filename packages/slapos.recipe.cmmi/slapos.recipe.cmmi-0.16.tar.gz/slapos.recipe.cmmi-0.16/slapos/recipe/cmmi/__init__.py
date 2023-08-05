import errno
from hashlib import md5
import slapos.recipe.downloadunpacked
import imp
import logging
import os
import pkg_resources
from platform import machine as platform_machine
import re
import shutil
import stat
import subprocess
import sys
import zc.buildout
try:
  # import from zc.buildout>2
  from zc.buildout.buildout import bool_option
except:
  def bool_option(options, name, defaults=None):
    if getattr(options, "query_bool", None) is None:
      from zc.buildout.buildout import Options
      options = Options({}, "options", options)
    return options.query_bool(name, defaults)

startup_environ = os.environ.copy()

# backport of shlex.quote from Python 3.3
_find_unsafe = re.compile(r'[^\w@%+=:,./-]', 256).search

def quote(s):
    """Return a shell-escaped version of the string *s*."""
    if not s:
        return "''"
    if _find_unsafe(s) is None:
        return s

    # use single quotes, and put single quotes into double quotes
    # the string $'b is then quoted as '$'"'"'b'
    return "'" + s.replace("'", "'\"'\"'") + "'"
###

class Recipe(object):
    """zc.buildout recipe for compiling and installing software"""

    def __init__(self, buildout, name, options):
        self.options = options
        self.buildout = buildout
        self.name = name
        log = logging.getLogger(self.name)
        # Merge options if there is a matched platform section
        platform_options = buildout.get(
            "%s:%s:%s" % (name, sys.platform, self.get_machine()),
            buildout.get("%s:%s" % (name, sys.platform)))
        if platform_options is None:
            self.original_options = options
        else:
            self.original_options = options.copy()
            options.update(platform_options)

        environment_section = options.get('environment-section')
        self.environ = (
            buildout[environment_section].copy()
            if environment_section else {})

        # Trigger computation of part signature for shared signature.
        # From now on, we should not pull new dependencies.
        # Ignore if buildout is too old.
        options.get('__buildout_signature__')

        shared = ((options.get('shared', '').lower() == 'true') and
                  buildout['buildout'].get('shared-part-list', None))
        if shared:
            self._signature = slapos.recipe.downloadunpacked.Signature(
                '.slapos.recipe.cmmi.signature')
            buildout_directory = buildout['buildout']['directory']
            profile_base_location = options.get('_profile_base_location_', '')
            for k, v in sorted(options.items()):
                if k != '_profile_base_location_':
                    # Key not vary on profile base location
                    if profile_base_location:
                        v = v.replace(profile_base_location,
                                      '${:_profile_base_location_}')
                    self._signature.update(k, v)

            signature_digest = self._signature.hexdigest()
            for x in shared.splitlines():
                x = x.strip().rstrip('/')
                if x:
                    shared = os.path.join(os.path.join(x, self.name),
                                          signature_digest)
                    if os.path.exists(shared):
                        break
            log.info('shared at %s', shared)
        else:
            shared = ''

        options['shared'] = shared
        location = options['location'] = shared or os.path.join(
            buildout['buildout']['parts-directory'],
            self.name)

        prefix = options.get('prefix', '').strip()
        if prefix == '':
            prefix = self.buildout_prefix = buildout['buildout'].get('prefix', '').strip()
            if 'cygwin' != sys.platform:
                self.buildout_prefix = ''
        else:
            self.buildout_prefix = ''
        options['prefix'] = prefix or location
        options['url'] = options.get('url', '').strip()
        options['path'] = options.get('path', '').strip()
        options['promises'] = options.get('promises', '')
        options['strip-top-level-dir'] = options.get('strip-top-level-dir', 'false').strip()

        if options['url'] and options['path']:
            raise zc.buildout.UserError('You must use either "url" or "path", not both!')
        if not (options['url'] or options['path']):
            raise zc.buildout.UserError('You must provide either "url" or "path".')

        if options['url']:
            options['compile-directory'] = location + '__compile__'
        else:
            options['compile-directory'] = options['path']

        for k, v in list(options.items()):
            if '@@LOCATION@@' in v:
                options[k] = v.replace('@@LOCATION@@', location)

        self.original_environment = os.environ.copy()
        for variable in options.get('environment', '').splitlines():
            if variable.strip():
                try:
                    key, value = variable.split('=', 1)
                    self.environ[key.strip()] = value
                except ValueError:
                    raise zc.buildout.UserError('Invalid environment variable definition: %s' % variable)
        # Add prefix to PATH, CPPFLAGS, CFLAGS, CXXFLAGS, LDFLAGS
        if self.buildout_prefix != '':
            self.environ['PATH'] = '%s/bin:%s' % (self.buildout_prefix, self.environ.get('PATH', '/usr/bin'))
            self.environ['CPPFLAGS'] = '-I%s/include %s' % (self.buildout_prefix, self.environ.get('CPPFLAGS', ''))
            self.environ['CFLAGS'] = '-I%s/include %s' % (self.buildout_prefix, self.environ.get('CFLAGS', ''))
            self.environ['CXXFLAGS'] = '-I%s/include %s' % (self.buildout_prefix, self.environ.get('CXXFLAGS', ''))
            self.environ['LDFLAGS'] = '-L%s/lib %s' % (self.buildout_prefix, self.environ.get('LDFLAGS', ''))

        if options.get('configure-command') == 'cygport':
            self.environ.setdefault('CYGCONF_PREFIX', options['prefix'])

    def augmented_environment(self):
        """Returns a dictionary containing the current environment variables
        augmented with the part specific overrides.

        The dictionary is an independent copy of ``os.environ`` and
        modifications will not be reflected in back in ``os.environ``.
        """
        # Note that we don't set TMPDIR or TMP here as we use to do, because
        # this path might be too deep and this will cause problem with some
        # software (for example golang) who runs a test suite after build and
        # use this TMPDIR to create unix sockets.
        env = os.environ.copy()
        env.update(self.environ)
        return env

    def update(self):
        pass

    def _compute_part_signatures(self, options):
        # Copy from zc.buildout.Buildout, compute recipe signature
        recipe, entry = zc.buildout.buildout._recipe(options)
        req = pkg_resources.Requirement.parse(recipe)
        sig = zc.buildout.buildout._dists_sig(pkg_resources.working_set.resolve([req]))
        return ' '.join(sig)

    def get_platform(self):
        # Get value of sys.platform
        for platform in ['linux', 'cygwin', 'beos', 'darwin', 'atheos', 'osf1',
            'netbsd', 'openbsd',  'freebsd', 'unixware', 'sunos']:
            if sys.platform.startswith(platform):
                return platform
        return sys.platform

    def get_machine(self):
        arch = platform_machine()
        # i?86-*-* : x86
        if arch in ('i386', 'i586', 'i686'):
            return 'x86'
        # x86_64-*-* : amd64
        elif arch == 'x86_64':
            return 'amd64'
        # ia64-*-* : ia64
        # and others
        return arch

    def get_platform_options(self):
        platform_part = self.get_platform() + '-' + self.name
        part_list = [part for part in self.buildout if part.endswith(platform_part)]
        if part_list[:1]:
            arch_prefix = self.get_machine() + '-'
            for part in part_list:
                if part.startswith(arch_prefix):
                    return self.buildout[part]
            else:
                return self.buildout.get(platform_part)

    def download_file(self, url):
        download = zc.buildout.download.Download(
          self.buildout['buildout'], hash_name=True)
        url, _s_, md5sum = url.partition('#')
        return download(url, md5sum=md5sum or None)

    def get_installed_files(self, ref_file):
        # if [buildout] has option 'prefix', then return all the files
        # in this path which create time is newer than ref_file.
        # Exclude directory and don't follow link.
        assert self.buildout_prefix
        log = logging.getLogger(self.name)
        args = ['find', self.buildout_prefix, '-cnewer', ref_file, '!', '-type', 'd']
        try:
            files = subprocess.check_output(args,
                universal_newlines=True, close_fds=True)
        except Exception as e:
            log.error(e)
            raise zc.buildout.UserError('System error')
        return files.splitlines()

    def check_promises(self, log=None):
        result = True
        log = logging.getLogger(self.name)
        for path in self.options['promises'].splitlines():
            if path and not os.path.exists(path):
                result = False
                log.warning('could not find promise "%s"' % path)
        return result

    def call_script(self, script):
        """This method is copied from z3c.recipe.runscript.

        See http://pypi.python.org/pypi/z3c.recipe.runscript for details.
        """
        url, callable = script.rsplit(':', 1)
        filename, is_temp = self.download_file(url)
        if not is_temp:
            filename = os.path.abspath(filename)
        module = imp.load_source('script', filename)
        script = getattr(module, callable.strip())

        try:
            script(self.options, self.buildout, self.augmented_environment())
        except TypeError:
            # BBB: Support hook scripts that do not take the environment as
            # the third parameter
            script(self.options, self.buildout)
        finally:
            if is_temp:
                os.remove(filename)

    def run(self, cmd):
        """Run the given ``cmd`` in a child process."""
        log = logging.getLogger(self.name)
        try:
            subprocess.check_call('set -e;' + cmd, shell=True,
                env=self.augmented_environment(), close_fds=True)
        except Exception as e:
            log.error(e)
            raise zc.buildout.UserError('System error')

    def install(self):
        log = logging.getLogger(self.name)
        parts = []

        # In shared mode, do nothing if package has been installed.
        if (not self.options['shared'] == ''):
            log.info('Checking whether package is installed at shared path: %s', self.options['shared'])
            if self._signature.test(self.options['shared']):
                log.info('This shared package has been installed by other package')
                return parts

        # Extrapolate the environment variables using values from the current
        # environment.
        for key in self.environ:
            self.environ[key] %= os.environ

        make_cmd = self.options.get('make-binary', 'make').strip()
        make_options = ' '.join(self.options.get('make-options', '').split())
        make_targets = ' '.join(self.options.get('make-targets', 'install').split())

        configure_options = self.options.get('configure-options', '').split()
        configure_cmd = self.options.get('configure-command', '').strip()

        if not configure_cmd:
            # Default to using basic configure script.
            configure_cmd = './configure'
            # Inject the --prefix parameter if not already present
            if '--prefix' not in ' '.join(configure_options):
                configure_options.insert(0, '--prefix=\"%s\"' % self.options['prefix'])
        elif make_cmd == 'make' and make_targets == 'install':
            make_targets += ' prefix=\"%s\"' % self.options['prefix']

        configure_cmd = '%s %s' % (configure_cmd, ' '.join(configure_options)) % self.options
        install_cmd = '%s %s %s' % (make_cmd, make_options, make_targets) % self.options
        make_cmd = '%s %s' % (make_cmd, make_options) % self.options

        patch_cmd = self.options.get('patch-binary', 'patch').strip()
        patch_options = ' '.join(self.options.get('patch-options', '-p0').split())
        patches = self.options.get('patches', '').split()

        if self.environ:
            for key in sorted(self.environ.keys()):
                log.info('[ENV] %s = %s', key, self.environ[key])

        # Download the source using slapos.recipe.downloadunpacked
        if self.options['url']:
            compile_dir = self.options['compile-directory']
            if os.path.exists(compile_dir):
                # leftovers from a previous failed attempt, removing it.
                log.warning('Removing already existing directory %s' % compile_dir)
                shutil.rmtree(compile_dir)
            os.makedirs(compile_dir)
            try:
                self.options.get('md5sum') # so that buildout does not complain "unused option md5sum"
                opt = self.options.copy()
                opt['destination'] = compile_dir
                # no need to shared build for compile dir
                opt['shared'] = 'false'
                slapos.recipe.downloadunpacked.Recipe(
                    self.buildout, self.name, opt).install()
            except:
                shutil.rmtree(compile_dir)
                raise
        else:
            log.info('Using local source directory: %s' % self.options['path'])
            compile_dir = self.options['path']

        current_dir = os.getcwd()
        location = self.options['location']
        # Clean the install directory if it already exists as it is
        # a remain from a previous failed installation
        if os.path.exists(location):
          shutil.rmtree(location)
        os.mkdir(location)
        try:
            os.chdir(compile_dir)
            try:
                # We support packages that either extract contents to the $PWD
                # or alternatively have a single directory.
                contents = os.listdir(compile_dir)
                if len(contents) == 1 and os.path.isdir(contents[0]):
                    # Single container
                    os.chdir(contents[0])

                if patches:
                    log.info('Applying patches')
                    for patch in patches:
                        patch_filename, is_temp = self.download_file(patch)
                        self.run('%s %s < %s' % (patch_cmd, patch_options, patch_filename))
                        if is_temp:
                            os.remove(patch_filename)

                if 'pre-configure-hook' in self.options and len(self.options['pre-configure-hook'].strip()) > 0:
                    log.info('Executing pre-configure-hook')
                    self.call_script(self.options['pre-configure-hook'])

                pre_configure_cmd = self.options.get('pre-configure', '').strip() % self.options
                if pre_configure_cmd != '':
                    log.info('Executing pre-configure')
                    self.run(pre_configure_cmd)

                self.run(configure_cmd)

                if 'pre-make-hook' in self.options and len(self.options['pre-make-hook'].strip()) > 0:
                    log.info('Executing pre-make-hook')
                    self.call_script(self.options['pre-make-hook'])

                pre_build_cmd = self.options.get('pre-build', '').strip() % self.options
                if pre_build_cmd != '':
                    log.info('Executing pre-build')
                    self.run(pre_build_cmd)

                self.run(make_cmd)

                pre_install_cmd = self.options.get('pre-install', '').strip() % self.options
                if pre_install_cmd != '':
                    log.info('Executing pre-install')
                    self.run(pre_install_cmd)

                self.run(install_cmd)

                if 'post-make-hook' in self.options and len(self.options['post-make-hook'].strip()) > 0:
                    log.info('Executing post-make-hook')
                    self.call_script(self.options['post-make-hook'])

                post_install_cmd = self.options.get('post-install', '').strip() % self.options
                if post_install_cmd != '':
                    log.info('Executing post-install')
                    self.run(post_install_cmd)
                if (self.buildout_prefix != ''
                        and self.options['shared'] == ''
                        and os.path.exists(self.buildout_prefix)):
                    log.info('Getting installed file lists')
                    parts.extend(self.get_installed_files(compile_dir))
            except:

                with open('slapos.recipe.build.env.sh', 'w') as env_script:
                    for key, v in sorted(self.augmented_environment().items()):
                        if v != startup_environ.get(key):
                            env_script.write('%sexport %s=%s\n' % (
                                '#'[:key in ('TEMP', 'TMP', 'TMPDIR')],
                                key, quote(v)))
                    env_script.write('''\
echo "If this recipe does not use pre/post hooks or commands, you can re-run as below."
echo configure with:
echo %s
echo
echo make with:
echo %s
echo
echo install with:
echo %s
''' % (quote("  " + configure_cmd), quote("  " + make_cmd), quote("  " + install_cmd)))

                log.error('Compilation error. The package is left as is at %s where '
                          'you can inspect what went wrong.\n'
                          'A shell script slapos.recipe.build.env.sh has been generated. '
                          'You can source it in your shell to reproduce build environment.' % os.getcwd())

                # Delete shared directory if not correctly installed
                if self.options.get('shared'):
                    shutil.rmtree(self.options['shared'])
                raise
        finally:
            os.chdir(current_dir)

        if self.options['shared']:
          self._signature.save(self.options["shared"])

        # Check promises
        self.check_promises(log)

        if self.options['url']:
            if self.options.get('keep-compile-dir',
                self.buildout['buildout'].get('keep-compile-dir', '')).lower() in ('true', 'yes', '1', 'on'):
                # If we're keeping the compile directory around, add it to
                # the parts so that it's also removed when this recipe is
                # uninstalled.
                parts.append(self.options['compile-directory'])
            else:
                shutil.rmtree(compile_dir)
                del self.options['compile-directory']

        if self.options['shared'] == '':
            parts.append(location)

        self.fix_shebang(location)
        if self.options['shared']:
            slapos.recipe.downloadunpacked.make_read_only_recursively(location)
        return parts

    def fix_shebang(self, location):
        # Workaround for shebang line limit by renaming the script and
        # putting a wrapper shell script.
        for dir in ('bin', 'sbin'):
            dir_abspath = os.path.join(location, dir)
            if not os.path.isdir(dir_abspath):
                continue
            for f in os.listdir(dir_abspath):
                f_abspath = os.path.join(dir_abspath, f)
                st_mode = os.stat(f_abspath).st_mode
                if not stat.S_ISREG(st_mode):
                    continue
                with open(f_abspath, 'rb') as f:
                    header = f.readline(128)
                if header.startswith(b'#!') and header[-1] != b'\n':
                    os.rename(f_abspath, f_abspath + '.shebang')
                    with open(f_abspath, 'w') as f:
                        os.fchmod(f.fileno(), stat.S_IMODE(st_mode))
                        f.write('''#!/bin/sh -e
read -r EXE ARG < "$0.shebang"
EXE=${EXE#\\#!}
[ "$EXE" ] || read -r _ EXE ARG < "$0.shebang"
exec $EXE ${ARG:+"$ARG"} "$0.shebang" "$@"
''')
