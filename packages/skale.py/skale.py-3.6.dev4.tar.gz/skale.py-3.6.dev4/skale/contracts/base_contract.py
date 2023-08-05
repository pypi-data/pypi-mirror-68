#   -*- coding: utf-8 -*-
#
#   This file is part of SKALE.py
#
#   Copyright (C) 2019-Present SKALE Labs
#
#   SKALE.py is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   SKALE.py is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with SKALE.py.  If not, see <https://www.gnu.org/licenses/>.
""" SKALE base contract class """

import logging
from functools import partial, wraps

from web3 import Web3

from skale.dataclasses.tx_res import TxRes
from skale.transactions.tools import post_transaction, make_dry_run_call
from skale.utils.web3_utils import wait_for_receipt_by_blocks


logger = logging.getLogger(__name__)


def transaction_method(transaction=None, *, gas_limit=10):
    if transaction is None:
        return partial(transaction_method, gas_limit=gas_limit)

    @wraps(transaction)
    def wrapper(self, *args, wait_for=True,
                wait_timeout=4, blocks_to_wait=50,
                gas_price=None, nonce=None,
                dry_run_only=False, skip_dry_run=False, raise_for_status=True,
                **kwargs):
        method = transaction(self, *args, **kwargs)
        tx_res = TxRes()
        if not skip_dry_run:
            tx_res.dry_run_result = make_dry_run_call(self.skale.wallet,
                                                      method, gas_limit)

        if not dry_run_only and (skip_dry_run or tx_res.dry_run_passed()):
            gas_price = gas_price or self.skale.gas_price
            tx_res.hash = post_transaction(self.skale.wallet, method,
                                           gas_limit, gas_price, nonce)
            if wait_for:
                tx_res.receipt = wait_for_receipt_by_blocks(
                    self.skale.web3,
                    tx_res.hash,
                    timeout=wait_timeout,
                    blocks_to_wait=blocks_to_wait
                )

        if raise_for_status:
            tx_res.raise_for_status()

        return tx_res

    return wrapper


class BaseContract:
    def __init__(self, skale, name, address, abi):
        self.skale = skale
        self.name = name
        self.address = Web3.toChecksumAddress(address)
        self.contract = skale.web3.eth.contract(address=self.address, abi=abi)
