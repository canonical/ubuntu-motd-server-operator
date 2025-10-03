# initial hello world Flask app

import flask
import json
import yaml
import logging
import re

DEFAULT_MOTD = "Default motd"

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

app = flask.Flask(__name__)
app.config.from_prefixed_env()

def get_motds_dict():
    motds_env = app.config.get("MOTDS")
    if not motds_env:
        logger.warning("No motds found in environment")
        return {}

    try:
        raw_motds = yaml.safe_load(motds_env)
        motds = {target:"".join(content) for target, content in raw_motds.items()}
    except:
        logger.error("Could not parse MOTDs")
        return {}

    return motds

def extract_info(user_agent):
    version = re.search(r'Ubuntu/(\d{2}\.\d{2})', user_agent)
    arch = re.search(r'/(\w+) cloud_id', user_agent)
    cloud = re.search(r'cloud_id/(\w+)', user_agent)

    return (version.group(1) if version else "", arch.group(1) if arch else "", cloud.group(1) if cloud else "")

def select_motd(motds, version, arch, cloud):
    if version and arch and cloud and f"index-{version}-{arch}-{cloud}.txt" in motds:
        return motds[f"index-{version}-{arch}-{cloud}.txt"]

    if version and arch and f"index-{version}-{arch}.txt" in motds:
        return motds[f"index-{version}-{arch}.txt"]

    if version and cloud and f"index-{version}-{cloud}.txt" in motds:
        return motds[f"index-{arch}-{cloud}.txt"]

    if version and f"index-{version}.txt" in motds:
        return motds[f"index-{version}.txt"]

    if arch and f"index-{arch}.txt" in motds:
        return motds[f"index-{arch}.txt"]

    if cloud and f"index-{cloud}.txt" in motds:
        return motds[f"index-{cloud}.txt"]

    return ""

@app.route("/")
def index():
    motds = get_motds_dict()
    logger.debug("motds: %s", str(motds))
    if not motds:
        return DEFAULT_MOTD

    version, arch, cloud = extract_info(flask.request.user_agent.string)
    logger.debug("version: %s, arch: %s, cloud: %s", version, arch, cloud)

    motd = select_motd(motds, version, arch, cloud)
    logger.debug("motd: %s", motd)

    if not motd:
        return DEFAULT_MOTD

    return motd


if __name__ == "__main__":
    app.run()

