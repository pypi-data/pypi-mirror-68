import logging
import re
from concurrent.futures import ThreadPoolExecutor

from flask import Blueprint, request, make_response
from injector import inject
from jsonpickle import json

from tracker.core.connectors.issue_handler import IssueHandler
from tracker.core.connectors.webhook_parser import WebHookDataParser, ParseError
from tracker.core.fix_version_detection import process_hook_data
from tracker.env import TRACKED_BRANCH_REGEXP, WHITE_LISTED_REPOS

account_api = Blueprint('git_ba408479325a51ea5078cb427422f490df19dfb0', __name__)
logger = logging.getLogger("git:push:hook")
__git_pool__ = ThreadPoolExecutor(1)


@inject
@account_api.route("/git/ba408479325a51ea5078cb427422f490df19dfb0", methods=["POST"])
def git_push_hook(webhook_parser: WebHookDataParser, handler: IssueHandler):
    data = request.data
    if len(data) == 0:
        return make_response("", 200)

    event_request = json.loads(data)
    logger.info("Request {}".format(json.dumps(event_request)))
    try:
        ref = webhook_parser.parse(event_request)
    except ParseError:
        return make_response("", 200)

    search = re.search(TRACKED_BRANCH_REGEXP, ref.ref_id)
    if (ref.update_type == "UPDATE") and (search is not None) and (re.search(WHITE_LISTED_REPOS, ref.repo_name)):
        logger.info("Submit commit for processing")
        __git_pool__.submit(process_hook_data, ref, handler)
    else:
        logger.info("Either repo {} or branch {} is not tracked".format(ref.repo_name, ref.ref_id))

    return make_response("", 200)
