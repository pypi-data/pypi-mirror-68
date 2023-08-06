from django.contrib.staticfiles.finders import get_finders
from django.core.management.base import BaseCommand
from django.conf import settings

import sass
import time
import os


class Command(BaseCommand):
    """
    Simplify the use of Sass in Django.
    Using libsass, compile all .scss files found in the paths defined in settings.STATICFILES_FINDERS.
    """
    help = "Simplify the use of Sass in Django"

    @staticmethod
    def add_arguments(parser):

        parser.add_argument(
            '-s',
            '--style',
            dest='style',
            type=str,
            choices=['expanded', 'nested', 'compact', 'compressed'],
            help=('An optional coding style of the compiled result. '
                  'Choose one of: `\'nested\'`, `\'expanded\'` (default), `\'compact\'`, `\'compressed\'` '
                  'You can also define this argument in SASS_COMPILER_STYLE environment variable.'),
        )

        parser.add_argument(
            '-p',
            '--precision',
            dest='precision',
            type=int,
            help='Optional precision for numbers. 8 by default. '
                 'You can also define this argument in SASS_COMPILER_PRECISION environment variable.',
        )

        parser.add_argument(
            '-nb',
            '--no-build',
            dest='build',
            action='store_true',
            help=('Don\'t create build folder, e.g. "app/static/app/css/style.css" '
                  'instead "app/static/app/build/css/style.css". '
                  'You can also define this argument in SASS_COMPILER_NO_BUILD environment variable.'),
        )

        parser.add_argument(
            '-m',
            '--map',
            dest='map',
            action='store_true',
            help=('Build a source map "style.css.map". '
                  'You can also define this argument in SASS_COMPILER_IGNORE environment variable.'),
        )

        parser.add_argument(
            '-c',
            '--clean',
            dest='clean',
            action='store_true',
            help=('Remove "style.css", "style.css.map", "style.min.css", "style.min.css.map" files before '
                  'compilation. This action will only take effect on current destination folder. '
                  'You can also define this argument in SASS_COMPILER_CLEAN environment variable.'),
        )

        parser.add_argument(
            '-i',
            '--ignore',
            action='append',
            default=[],
            dest='ignore',
            metavar='PATTERN',
            help=('Ignore files or directories matching this glob-style pattern. '
                  'Use multiple times to ignore more. '
                  'NOTE: The patterns will applied in the path since the `static` folder to the file name. '
                  'E.g. to ignore "apps/app/static/app/scss/style.scss" the longest path would be '
                  '"--ignore=app/scss/style.scss" or "-i=**/**/style.scss" or some other glob-style pattern. '
                  'You can also define this argument in SASS_COMPILER_IGNORE environment variable.'),
        )

        parser.add_argument(
            '-w',
            '--watch',
            dest='watch',
            action='store_true',
            help=('Watch and compile files when scss files are changed. '
                  'You can also define this argument in SASS_COMPILER_IGNORE environment variable.'),
        )

    def handle(self, *args, **options):
        """
        Runs Sass Compiler once time or in watch mode.
        :param args:
        :param options:
        """
        style = self.get_argument(options, 'style', 'SASS_COMPILER_STYLE', 'expanded')
        precision = self.get_argument(options, 'precision', 'SASS_COMPILER_PRECISION', 8)
        build = not self.get_argument(options, 'build', 'SASS_COMPILER_NO_BUILD', False)
        map = self.get_argument(options, 'map', 'SASS_COMPILER_MAP', False)
        clean = self.get_argument(options, 'clean', 'SASS_COMPILER_CLEAN', False)
        watch = self.get_argument(options, 'watch', 'SASS_COMPILER_WATCH', False)

        include_paths = self.get_static_paths()                             # List of paths to find @import
        ignore_patterns = self.get_ignore_patterns(options.get('ignore'))   # List of patterns to exclude paths

        self.stdout.write('--style: ' + str(style))
        self.stdout.write('--precision: ' + str(precision))
        self.stdout.write('--no-build: ' + str(not build))
        self.stdout.write('--map: ' + str(map))
        self.stdout.write('--clean: ' + str(clean))
        self.stdout.write('--watching: ' + str(watch))
        self.stdout.write('--ignore: ' + str(ignore_patterns))

        if watch:
            self.stdout.write('Start watching...')
            try:
                files = {}
                while True:
                    files, recompile = self.needs_recompile(files)
                    if recompile:
                        self.compile_files(style, build, include_paths, ignore_patterns, precision, map, clean)
                    time.sleep(1)

            except (InterruptedError, KeyboardInterrupt):
                self.stdout.write('Stop watching.')

        else:
            self.compile_files(style, build, include_paths, ignore_patterns, precision, map, clean)

        self.stdout.write('End.')

    def compile_files(self, output_style, build, include_paths, ignore_patterns, precision, source_map, clean):
        """
        Finds all scss files in all apps (except who starts with _ e.g.: _variable.scss) and runs sass compile
        :param output_style:        'expanded' | 'nested' | 'compact' | 'compressed'
        :param build:               True | False
        :param include_paths:       List of paths to find @import
        :param ignore_patterns:     List of patterns to ignore
        :param precision:           8
        :param source_map:          True | False
        :param clean:               True | False
        """

        for scss_filename in self.get_scss_files(ignore_patterns):

            css_filename, source_map_filename = self.get_output_files(scss_filename, build, output_style)

            try:
                output = sass.compile(
                    filename=scss_filename,
                    source_map_filename=source_map_filename,
                    include_paths=include_paths,
                    output_style=output_style,
                    precision=precision,
                    omit_source_map_url=not source_map
                )

                if output and isinstance(output, tuple):
                    self.clean_files(css_filename) if clean else None
                    self.store_file(css_filename, output[0])
                    self.store_file(source_map_filename, output[1]) if source_map and len(output) > 1 else None

            except sass.CompileError as exc:
                self.stdout.write(str(exc))

        self.stdout.write("Files compiled at %s" % time.time())

    def needs_recompile(self, files):
        """
        Check if any files have been changed and compilation is necessary
        Return dict with file and modified datetime
        :param files: {'Your/Path/project/apps/app1/static/app1/scss/style.scss: 1587830257.0483491, ...}
        :return:
        True|False,
        {
            'Your/Path/project/apps/app1/static/app1/scss/style.scss: 1587830257.0483491
            ...
        }
        """
        update = False
        for file in self.get_scss_files():
            modified = os.path.getmtime(file)
            if modified > files.get(file, 0):
                files.update({file: modified})
                update = True

        return files, update

    @staticmethod
    def get_argument(options, argument_name, settings_argument, default):
        """
        Ger argument passed or declared in settings
        :param options:
        :param argument_name:       'style' | 'precision' | 'build' | 'map' | 'clean'
        :param settings_argument:   'SASS_COMPILER_STYLE' | 'SASS_COMPILER_PRECISION' | ...
        :param default:             'expanded' | 8 | False | ...
        :return:                    'expanded'
        """
        if not options.get(argument_name) and hasattr(settings, settings_argument):
            result = getattr(settings, settings_argument, default)
        elif options.get(argument_name):
            result = options.get(argument_name)
        else:
            result = default

        return result

    @staticmethod
    def get_output_files(filename, build, style):
        """
        Gets output css and source map file names
        Manage the output path according to the arguments --no-build and --style
        :param filename:    'Your/Path/project/apps/app1/static/app1/scss/style.scss'
        :param build:       True | False
        :param style:       'expanded' | 'nested' | 'compact' | 'compressed'
        :return:
        'Your/Path/project/apps/app1/static/app1/build/css/style.css',
        'Your/Path/project/apps/app1/static/app1/build/css/style.css.map'
        """
        scss_folder = ''.join([os.sep, 'scss', os.sep])                                 # \scss\
        build_folder = ''.join([os.sep, 'build']) if build else ''                      # \build | ''
        css_folder = ''.join([build_folder, os.sep, 'css', os.sep])                     # \build\css\ | \css\
        css_file = filename.replace(scss_folder, css_folder).replace('.scss', '.css')   # ...\build\css\style.css
        source_map_filename = ''.join([css_file, '.map'])                               # ...\build\css\style.css.map
        if style == 'compressed':
            css_file = css_file.replace('.css', '.min.css')                             # ...\build\css\style.min.css

        return css_file, source_map_filename

    @staticmethod
    def get_scss_files(ignore_patterns=[]):
        """
        Get scss files
        :param ignore_patterns: List ['_*.scss'] Exclude all files who starts with _ and end .scss e.g: _variables.scss
        :return:
        [
            'Your/Path/project/apps/app1/static/app1/scss/style.scss,
            'Your/Path/project/apps/app2/static/app2/scss/style.scss
            ...
        ]
        """

        results = []
        for finder in get_finders():
            results += [finder.find(p) for p, s in finder.list(ignore_patterns) if p.endswith('.scss')]
        return results

    @staticmethod
    def get_static_paths():
        """
        Get all static paths
        :return:
        [
            'Your/Path/project/apps/app1/static',
            'Your/Path/project/apps/app2/static'
            ...
        ]
        """
        results = []
        for f in get_finders():
            if hasattr(f, 'storages'):
                results += [f.storages.get(x).location for x in f.storages if hasattr(f.storages.get(x), 'location')]

        return results

    @staticmethod
    def get_ignore_patterns(ignore_args):
        """
        Get a list of ignore patterns
        :param ignore_args: ['*/*/*.scss', 'groups/scss/*']  -i='*/*/*.scss' -i='app/scss/*'
        :return:
        """
        patterns = ['_*.scss'] + list(set(ignore_args))
        if hasattr(settings, 'SASS_COMPILER_IGNORE'):
            patterns += settings.SASS_COMPILER_IGNORE
        return [x.replace('\\', os.sep).replace('/', os.sep) for x in patterns]

    @staticmethod
    def store_file(filename, raw):
        """
        Store sass.compile output in file
        :param filename:    'Your/Path/project/apps/users/static/users/build/css/style.css'
        :param raw:         'body {background-color: #f4f7f9;}...'
        """
        file_path = os.path.dirname(filename)
        if not os.path.exists(file_path):
            os.makedirs(file_path, exist_ok=True)

        file = open(filename, 'w', encoding='utf8')
        file.write(raw)
        file.close()

    @staticmethod
    def clean_files(filename):
        """
        Remove 'style.css', 'style.css.map', 'style.min.css', 'style.min.css.map' files from css folder
        :param filename:    'Your/Path/project/apps/users/static/users/build/css/style.css'
        """
        file, ext = os.path.splitext(filename)
        file = file[:-4] if file.endswith('.min') else file
        for extension in ('css', 'css.map', 'min.css', 'min.css.map'):
            path = '.'.join([file, extension])
            if os.path.isfile(path):
                os.remove(path)
