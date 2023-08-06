import logging

from tracker.core.connectors.webhook_parser import WebHookDataParser, ParseError, RefChangeRequest

logger = logging.getLogger("webhook-parser")


class BitBucketHookParser(WebHookDataParser):

    def parse(self, request) -> RefChangeRequest:
        if len(request["changes"]) == 0:
            logger.info("Nothing was changed")
            raise ParseError()

        event_key = request["eventKey"]
        link = list(filter(lambda x: x["name"] == "http", request["repository"]["links"]["clone"]))[0]["href"]
        changes = request["changes"][0]
        type = changes["type"]
        to_hash = changes["toHash"]
        from_hash = changes["fromHash"]
        ref_id = changes["refId"].replace("refs/heads", "refs/remotes/origin")

        logger.info("Parsed request: {} {} {} {} {} {}".format(event_key, link, type, to_hash, from_hash, ref_id))
        ref_request = RefChangeRequest(
            repo_name=request["repository"]["name"],
            repo_link=link,
            update_type=type,
            to_hash=to_hash,
            from_hash=from_hash,
            ref_id=ref_id
        )
        return ref_request
