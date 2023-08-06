import logging
from abc import abstractmethod, ABC

from tracker.core.connectors.webhook_parser import RefChangeRequest

logger = logging.getLogger("issue:handler")


class IssueHandler(ABC):
    def __init__(self):
        pass

    def handle(self, issues, request: RefChangeRequest):
        if len(issues) > 0:
            self.process(issues, request)
        else:
            logger.info("issues not found")

    @abstractmethod
    def process(self, issues, request: RefChangeRequest):
        pass
