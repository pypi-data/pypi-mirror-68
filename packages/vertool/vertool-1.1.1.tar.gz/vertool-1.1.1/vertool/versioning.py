from os import environ
from subprocess import DEVNULL, CalledProcessError, check_output


def get_local_version() -> str:
    """Dynamically get the version based on git commits.

    To generate a version of the application, use the git to describe
    command. This method is used to obtain the current version of the
    project and format it according to a given standard. This format
    is set by python standard: https://www.python.org/dev/peps/pep-0440.

    Returns:
        A formatted version of the application.
    """
    command = 'git describe --tags --long --dirty'
    version = check_output(command.split(), stderr=DEVNULL).decode().strip().split('-')

    # Version checking for uncommitted changes.
    commit_is_dirty = len(version) == 4

    # Formatting an application version according to a given format.
    tag, commit_count, commit_hash = version[:3]
    if commit_count == '0' and not commit_is_dirty:
        return tag

    version = '{0}.dev{1}+{2}'.format(tag, commit_count, commit_hash.lstrip('g'))

    # If regional code changes are not committed, this version is considered
    # dirty and has a corresponding prefix at the end of the version.
    return '{0}.dirty'.format(version) if commit_is_dirty else version


def get_remote_version() -> str:
    """Dynamically get the version based on bitbucket variables.

    To generate a version of the application, use the bitbucket
    variables. This method is used to obtain the current version
    of the project and format it according one of two available
    version formats.

    Returns:
        A formatted version of the application.
    """
    if 'CI_SERVER_NAME' in environ:
        if environ.get('CI_COMMIT_TAG', False):
            return environ['CI_COMMIT_TAG']
        return '{}-{}'.format(
            environ['CI_COMMIT_BRANCH'],
            environ['CI_COMMIT_SHORT_SHA'],
        )
    else:
        if environ.get('BITBUCKET_TAG', False):
            return environ['BITBUCKET_TAG']
        return '{}-{}'.format(
            environ['BITBUCKET_BRANCH'],
            environ['BITBUCKET_COMMIT'][:7],
        )


def get_version() -> str:
    """Dynamically get the version.

    To generate a version of the application, use one of two
    available method. This method is used to generate actual
    version of the current project.

    Returns:
        A formatted actual version of the application.
    """
    if environ.get('CI', False):
        return get_remote_version()

    # Use git version if the machine is local. If there is no
    # possibility to get a version using git, then getting a
    # project version is not possible.
    try:
        return get_local_version()
    except (FileNotFoundError, CalledProcessError):
        return 'unknown'
