# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirrormaker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'requests>=2.23.0,<3.0.0', 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['gitlab-mirror-maker = '
                     'mirrormaker.mirrormaker:mirrormaker']}

setup_kwargs = {
    'name': 'gitlab-mirror-maker',
    'version': '0.3.0',
    'description': 'Automatically mirror your repositories from GitLab to GitHub',
    'long_description': "# GitLab Mirror Maker\n\nGitLab Mirror Maker is a small tool written in Python that automatically mirrors your public repositories from GitLab to GitHub.\n\n![Example](./example.svg)\n\n\n# Why?\n\n- Maybe you like GitLab better but the current market favors developers with a strong GitHub presence?\n- Maybe as a form of backup?\n- Or maybe you have other reasons... :wink:\n\n\n# Installation\n\nInstall with pip or pipx:\n```\npip install gitlab-mirror-maker\n```\n\nThere's also a Docker image available:\n```\ndocker run registry.gitlab.com/grdl/gitlab-mirror-maker \n```\n\n\n# Usage\n\nRun: `gitlab-mirror-maker --github-token xxx --gitlab-token xxx`\n\nSee [Authentication](#authentication) below on how to get the authentication tokens.\n\n## Environment variables\n\nInstead of using cli flags you can provide configuration via environment variables with the `MIRRORMAKER_` prefix:\n```\nexport MIRRORMAKER_GITHUB_TOKEN xxx\nexport MIRRORMAKER_GITLAB_TOKEN xxx\n\ngitlab-mirror-maker\n```\n\n## Dry run\n\nRun with `--dry-run` flag to only print the summary and don't make any changes.\n\n## Full synopsis\n\n```\nUsage: gitlab-mirror-maker [OPTIONS]\n\nOptions:\n  --version            Show the version and exit.\n  --github-token TEXT  GitHub authentication token  [required]\n  --gitlab-token TEXT  GitLab authentication token  [required]\n  --github-user TEXT   GitHub username. If not provided, your GitLab username\n                       will be used by default.\n\n  --dry-run            If enabled, a summary will be printed and no mirrors\n                       will be created.\n\n  --help               Show this message and exit.\n```\n\n# How it works?\n\nGitLab Mirror Maker uses the [remote mirrors API](https://docs.gitlab.com/ee/api/remote_mirrors.html) to create [push mirrors](https://docs.gitlab.com/ee/user/project/repository/repository_mirroring.html#pushing-to-a-remote-repository-core) of your GitLab repositories.\n\nFor each public repository in your GitLab account a new GitHub repository is created using the same name and description. It also adds a `[mirror]` suffix at the end of the description and sets the website URL the original GitLab repo. See [the mirror of this repo](https://github.com/grdl/gitlab-mirror-maker) as an example.\n\nOnce the mirror is created it automatically updates the target GitHub repository every time changes are pushed to the original GitLab repo.\n\n## What is mirrored?\n\nOnly public repositories are mirrored to avoid publishing something private.\n\nOnly the commits, branches and tags are mirrored. No other repository data such as issues, pull requests, comments, wikis etc. are mirrored.\n\n\n# Authentication\n\nGitLab Mirror Maker needs authentication tokens for both GitLab and GitHub to be able to create mirrors.\n\n## How to get the GitLab token?\n\n- Click on your GitLab user -> Settings -> Access Tokens\n- Pick a name for your token and choose the `api` scope\n- Click `Create personal access token` and save it somewhere secure\n- Do not share it! It grants full access to your account!\n\nHere's more information about [GitLab personal tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html).\n\n## How to get the GitHub token?\n\n- Click on your GitHub user -> Settings -> Developer settings -> Personal access tokens -> Generate new token\n- Pick a name for your token and choose the `public_repo` scope\n- Click `Generate token` and save it somewhere secure\n\nHere's more information about [GitHub personal tokens](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line).\n\n\n# Automate with GitLab CI\n\nInstead of running the tool manually you may want to schedule it to run periodically with GitLab CI to make sure that any new repositories are automatically mirrored.\n\nHere's a `.gitlab-ci.yml` snippet you can use:\n```yaml\njob:\n  image: registry.gitlab.com/grdl/gitlab-mirror-maker:latest\n  script:\n    - gitlab-mirror-maker\n  only:\n    - schedules\n```\n\nHere's more info about creating [scheduled pipelines with GitLab CI](https://docs.gitlab.com/ee/ci/pipelines/schedules.html).\n",
    'author': 'Grzegorz Dlugoszewski',
    'author_email': 'pypi@grdl.dev',
    'maintainer': 'Grzegorz Dlugoszewski',
    'maintainer_email': 'pypi@grdl.dev',
    'url': 'https://gitlab.com/grdl/gitlab-mirror-maker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
