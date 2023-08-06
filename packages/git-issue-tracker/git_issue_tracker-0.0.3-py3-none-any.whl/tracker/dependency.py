from injector import singleton

from tracker.core.connectors.git.bitbucket import BitBucketHookParser
from tracker.core.connectors.issue_handler import IssueHandler
from tracker.core.connectors.webhook_parser import WebHookDataParser


def configure(binder):
    binder.bind(WebHookDataParser, to=BitBucketHookParser, scope=singleton)
    binder.bind(IssueHandler, to=IssueHandler, scope=singleton)

