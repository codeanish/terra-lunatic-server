import requests
import logging

logger = logging.getLogger()

class FlipsideCryptoService:

    _loaded = False

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
        first_90k_rows_staked_luna = requests.get("https://api.flipsidecrypto.com/api/v2/queries/81249395-a6da-4745-9442-5e028d19f721/data/latest")
        second_90k_rows_staked_luna = requests.get("https://api.flipsidecrypto.com/api/v2/queries/f15775eb-3639-4719-832f-4ffb5af81e8f/data/latest")
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
        logger.info(f"FlipsideCryptoService.load_governance_votes()")
        response = requests.get("https://api.flipsidecrypto.com/api/v2/queries/e10dafa5-67fc-41c7-9df6-496f8350a605/data/latest")
        votes_by_address = {}
        for address in response.json():
            votes_by_address[address["ADDRESS"]] = votes_by_address.get(address.get("ADDRESS")) + address.get("VOTES") if votes_by_address.get(address.get("ADDRESS")) else address.get("VOTES")
        return votes_by_address

    def _load_ust_deposits_to_anchor(self):
        """
        UST Deposits in Anchor, at time of writing, produces approximately 68k rows, within the 99k limit
        """
        logger.info(f"FlipsideCryptoService.load_ust_deposits_to_anchor()")
        response = requests.get("https://api.flipsidecrypto.com/api/v2/queries/74651668-7392-4667-8384-0ef7edf7fa59/data/latest")
        all_deposits = response.json()
        ust_deposits = {}
        for deposit in all_deposits:
            ust_deposits[deposit["DEPOSITOR"]] = ust_deposits.get(deposit.get("DEPOSITOR")) + deposit.get("DEPOSIT_AMOUNT") if ust_deposits.get(deposit.get("DEPOSITOR")) else deposit.get("DEPOSIT_AMOUNT")
        return ust_deposits

    def _load_pylon_pool_deposits(self):
        logger.info(f"FlipsideCryptoService._load_pylon_pool_deposits")
        response = requests.get("https://api.flipsidecrypto.com/api/v2/queries/5925c7c1-37ca-43a2-9c0d-7aba28170c71/data/latest")
        all_pool_deposits = response.json()
        pylon_deposits = {}
        for deposit in all_pool_deposits:
            pylon_deposits[deposit["ADDRESS"]] = pylon_deposits.get(deposit.get("ADDRESS")) + deposit.get("AMOUNT") if pylon_deposits.get(deposit.get("ADDRESS")) else deposit.get("AMOUNT")
        return pylon_deposits