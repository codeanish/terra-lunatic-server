import flask

from app.fllipside_crypto_service import FlipsideCryptoService
import json
import logging
from sys import stdout
from flask_cors import CORS
import werkzeug

app = flask.Flask(__name__)
CORS(app)
flipside_crypto_client = FlipsideCryptoService()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler(stdout)
logger.addHandler(consoleHandler)


@app.route('/', methods=['GET'])
def health_check():
    logger.info(f"health_check()")
    return "OK"


@app.route('/sync', methods=['PUT'])
def sync():
    logger.info(f"sync()")
    flipside_crypto_client.load()
    return "OK"

@app.route('/scores')
def get_score_categories():
    logger.info("get_score_categories()")
    return json.dumps(flipside_crypto_client.get_scores())

@app.route('/address/<address>/scores', methods=['GET'])
def get_my_scores(address: str):
    logger.info(f"get_my_scores({address}")
    return json.dumps(flipside_crypto_client.get_scores(address))


@app.route('/address/<address>/stakedluna', methods=['GET'])
def get_my_staked_luna(address: str):
    logger.info(f"get_my_staked_luna({address})")
    return json.dumps(flipside_crypto_client.get_staked_luna(address))


@app.route('/address/<address>/governancevotes', methods=['GET'])
def get_my_governance_votes(address: str):
    logger.info(f"get_my_governance_votes({address})")
    return json.dumps(flipside_crypto_client.get_governance_votes(address))


@app.route('/address/<address>/ustdeposits', methods=['GET'])
def get_my_ust_deposits_on_anchor(address: str):
    logger.info(f"get_my_ust_deposits_on_anchor({address})")
    return json.dumps(flipside_crypto_client.get_ust_deposits_on_anchor(address))


@app.route('/address/<address>/pylonmimeustdeposits', methods=['GET'])
def get_my_pylon_mime_ust_deposits(address: str):
    logger.info(f"get_my_pylon_mime_ust_deposits({address})")
    return json.dumps(flipside_crypto_client.get_pylon_deposits(address))


@app.route('/stakedluna', methods=['GET'])
def get_staked_luna():
    logger.info(f"get_staked_luna()")
    return json.dumps(flipside_crypto_client.get_staked_luna())


@app.route('/ustdeposits', methods=['GET'])
def get_ust_deposits_on_anchor():
    logger.info(f"get_ust_deposits_on_anchor()")
    return json.dumps(flipside_crypto_client.get_ust_deposits_on_anchor())


@app.route('/governancevotes', methods=['GET'])
def get_governance_votes():
    logger.info(f"get_governance_votes()")
    return json.dumps(flipside_crypto_client.get_governance_votes())


@app.route('/pylonmimeustdeposits', methods=['GET'])
def get_pylon_mime_ust_deposits():
    logger.info(f"get_pylon_mime_ust_deposits()")
    return json.dumps(flipside_crypto_client.get_pylon_deposits())

if __name__ == "__main__":
    app.run(host='0.0.0.0')