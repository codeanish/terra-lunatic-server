import requests
import logging
import settings

logger = logging.getLogger()

class FlipsideCryptoService:

    _loaded = False

    def get_scores(self, address: str = None):
        logger.info(f"FlipsideCryptoService.get_scores({address})")
        if self._loaded:
            if address is not None:
                staked_luna = self.get_staked_luna(address)
                governance_votes = self.get_governance_votes(address)
                ust_on_anchor = self.get_ust_deposits_on_anchor(address)
                pylon_deposits = self.get_pylon_deposits(address)
                return [{
                    "name": "Staked Luna",
                    "description": "Luna staked",
                    "score": 50,
                    "complete": True if staked_luna > 0 else False
                },
                {
                    "name": "The Govenor",
                    "description": "Voted in at least one governance proposal",
                    "score": 30,
                    "complete": True if governance_votes > 0 else False
                },
                {
                    "name": "UST depooited in Anchor",
                    "description": "UST Deposited in Anchor",
                    "score": 20,
                    "complete": True if ust_on_anchor > 0 else False
                },
                {
                    "name": "uLP Pylon Deposits",
                    "description": "uLP deposited in Pylon",
                    "score": 20,
                    "complete": True if pylon_deposits > 0 else False
                }]
            else:
                return [{
                    "name": "Staked Luna",
                    "description": "Luna staked",
                    "score": 50,
                    "complete": False
                },
                {
                    "name": "The Govenor",
                    "description": "Voted in at least one governance proposal",
                    "score": 30,
                    "complete": False
                },
                {
                    "name": "UST depooited in Anchor",
                    "description": "UST Deposited in Anchor",
                    "score": 20,
                    "complete": False
                },
                {
                    "name": "uLP Pylon Deposits",
                    "description": "uLP deposited in Pylon",
                    "score": 20,
                    "complete": False
                }]

    def get_staked_luna(self, address: str = None):
        logger.info(f"FlipsideCryptoService.get_staked_luna({address})")
        if self._loaded:
            if address:
                return self._staked_luna.get(address) if self._staked_luna.get(address) else 0
            return self._staked_luna
        self.load()
        return self.get_staked_luna()

    def get_ust_deposits_on_anchor(self, address: str = None):
        logger.info(f"FlipsideCryptoService.get_ust_deposits_on_anchor({address})")
        if self._loaded:
            if address:
                return self._ust_deposits.get(address) if self._ust_deposits.get(address) else 0
            return self._ust_deposits
        self.load()
        return self.get_ust_deposits_on_anchor()

    
    def get_governance_votes(self, address: str = None):
        logger.info(f"FlipsideCryptoService.get_governance_votes({address})")
        if self._loaded:
            if address:
                return self._governance_votes.get(address) if self._governance_votes.get(address) else 0
            return self._governance_votes
        self.load()
        return self.get_governance_votes()

    def get_pylon_deposits(self, address: str = None):
        logger.info(f"FlipsideCryptoService.get_pylon_deposits({address})")
        if self._loaded:
            if address:
                return self._pylon_pool_deposits.get(address) if self._pylon_pool_deposits.get(address) else 0
            return self._pylon_pool_deposits

    def load(self):
        logger.info(f"FlipsideCryptoService.load()")
        self._staked_luna = self._load_staked_luna()
        self._ust_deposits = self._load_ust_deposits_to_anchor()
        self._governance_votes = self._load_governance_votes()
        self._pylon_pool_deposits = self._load_pylon_pool_deposits()
        self._loaded = True

    def _load_staked_luna(self):
        logger.info(f"FlipsideCryptoService._load_staked_luna()")
        first_90k_rows_staked_luna = requests.get(settings.STAKED_LUNA_URL_1)
        second_90k_rows_staked_luna = requests.get(settings.STAKED_LUNA_URL_2)
        total_staked_luna = first_90k_rows_staked_luna.json() + second_90k_rows_staked_luna.json()
        staked_luna = {}
        for row in total_staked_luna:
            if row["ACTION"] == "undelegate":
                staked_luna[row["ADDRESS"]] = staked_luna.get(row["ADDRESS"]) - row["STAKED"] if staked_luna.get(row["ADDRESS"]) else -row["STAKED"]
            if row["ACTION"] == "delegate":
                staked_luna[row["ADDRESS"]] = staked_luna.get(row["ADDRESS"]) + row["STAKED"] if staked_luna.get(row["ADDRESS"]) else row["STAKED"]
        return staked_luna

    def _load_governance_votes(self):
        """
        Governance votes currently amount to 13k rows, within the 99k limit
        """
        logger.info(f"FlipsideCryptoService._load_governance_votes()")
        response = requests.get(settings.GOVERNANCE_VOTES_URL)
        votes_by_address = {}
        for address in response.json():
            votes_by_address[address["ADDRESS"]] = votes_by_address.get(address.get("ADDRESS")) + address.get("VOTES") if votes_by_address.get(address.get("ADDRESS")) else address.get("VOTES")
        return votes_by_address

    def _load_ust_deposits_to_anchor(self):
        """
        UST Deposits in Anchor, at time of writing, produces approximately 68k rows, within the 99k limit
        """
        logger.info(f"FlipsideCryptoService._load_ust_deposits_to_anchor()")
        response = requests.get(settings.DEPOSITS_TO_ANCHOR_URL)
        all_deposits = response.json()
        ust_deposits = {}
        for deposit in all_deposits:
            ust_deposits[deposit["DEPOSITOR"]] = ust_deposits.get(deposit.get("DEPOSITOR")) + deposit.get("DEPOSIT_AMOUNT") if ust_deposits.get(deposit.get("DEPOSITOR")) else deposit.get("DEPOSIT_AMOUNT")
        return ust_deposits

    def _load_pylon_pool_deposits(self):
        logger.info(f"FlipsideCryptoService._load_pylon_pool_deposits")
        response = requests.get(settings.PYLON_DEPOSITS_URL)
        all_pool_deposits = response.json()
        pylon_deposits = {}
        for deposit in all_pool_deposits:
            pylon_deposits[deposit["ADDRESS"]] = pylon_deposits.get(deposit.get("ADDRESS")) + deposit.get("AMOUNT") if pylon_deposits.get(deposit.get("ADDRESS")) else deposit.get("AMOUNT")
        return pylon_deposits