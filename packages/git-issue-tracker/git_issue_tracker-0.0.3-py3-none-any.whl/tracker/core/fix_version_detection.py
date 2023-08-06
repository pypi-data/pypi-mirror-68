import logging
import re
import shutil

import git
from git import Repo

from tracker.core.connectors.issue_handler import IssueHandler
from tracker.core.connectors.webhook_parser import RefChangeRequest
from tracker.env import GIT_USER_PASS, MERGE_PATTERN_SEARCH_TO_SKIP, ISSUE_TRACKER_PATTERN

logger = logging.getLogger("git:repository:process")
separator = "======="


def process_hook_data(request: RefChangeRequest, handler: IssueHandler):
    try:
        committed_issues = __find_merged_commits__(request)
        handler.handle(committed_issues, request)
    except Exception as e:
        logger.error("Error has happened either on processing ref change or post hook" + str(e))


def __find_merged_commits__(request: RefChangeRequest) -> [str]:
    repo_path = '/tmp/tracker_{}'.format(request.repo_name)

    def checkout_repo(path):
        r: Repo = None
        try:
            r = git.Repo(path)
        except Exception as e:
            logger.error(e)

        if r is None:
            logger.info("Cloning with GitPython over https with the username and token")
            try:
                r = git.Repo.clone_from("https://{}:{}@{}".format(
                    GIT_USER_PASS["username"],
                    GIT_USER_PASS["token"],
                    request.repo_link.split("https://")[1]), path)
            except Exception as e:
                logger.error(e)
        return r

    repo = checkout_repo(repo_path)
    try:
        logger.info("Fetch changes from remote")
        repo.git.fetch()
    except Exception as e:
        try:
            logger.info("Remove folder with project due to error in git tree {}".format(repo_path))
            shutil.rmtree(repo_path)
        except OSError as e:
            logger.error("Error: {} : {}".format(repo_path, e.strerror))
        checkout_repo(repo_path)

    included_issues = set()
    commits = repo.git.log('--pretty=Commit: %h Date: %ci%nAuthor: %ce%n%n%s%n%b%n{}'.format(separator),
                           '{}'.format(request.to_hash[:8]),
                           '^{}'.format(request.from_hash[:8]))
    for commit_str in re.split("{}\n?".format(separator), commits):
        if re.search(MERGE_PATTERN_SEARCH_TO_SKIP, commit_str) is not None:
            logger.info(
                "Found merge commit which skip further processing. Pattern {}".format(MERGE_PATTERN_SEARCH_TO_SKIP))
            logger.info(commit_str)
            break
        stripped_commit_msg = commit_str.strip()
        if stripped_commit_msg == '':
            continue

        logger.info("Parsed msg:\n{}".format(stripped_commit_msg))

        search = re.findall(ISSUE_TRACKER_PATTERN, commit_str)
        if len(search) > 0:
            for issue in search:
                included_issues.add(issue)

    return included_issues
