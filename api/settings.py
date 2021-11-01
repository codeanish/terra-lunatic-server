import os
from dotenv import load_dotenv

load_dotenv()

STAKED_LUNA_URL_1 = os.getenv("STAKED_LUNA_URL_1")
STAKED_LUNA_URL_2 = os.getenv("STAKED_LUNA_URL_2")
GOVERNANCE_VOTES_URL = os.getenv("GOVERNANCE_VOTES_URL")
DEPOSITS_TO_ANCHOR_URL = os.getenv("DEPOSITS_TO_ANCHOR_URL")
PYLON_DEPOSITS_URL=os.getenv("PYLON_DEPOSITS_URL")