import struct
from typing import NamedTuple
from solders.pubkey import Pubkey

class SellEvent(NamedTuple):
    timestamp: int
    base_amount_in: int
    min_quote_amount_out: int
    user_base_token_reserves: int
    user_quote_token_reserves: int
    pool_base_token_reserves: int
    pool_quote_token_reserves: int
    quote_amount_out: int
    lp_fee_basis_points: int
    lp_fee: int
    protocol_fee_basis_points: int
    protocol_fee: int
    quote_amount_out_without_lp_fee: int
    user_quote_amount_out: int
    pool: Pubkey
    user: Pubkey
    user_base_token_account: Pubkey
    user_quote_token_account: Pubkey
    protocol_fee_recipient: Pubkey
    protocol_fee_recipient_token_account: Pubkey

    @staticmethod
    def decode(data: bytes) -> "SellEvent":
        unpacked = struct.unpack(
            "<qQQQQQQQQQQQQQ32s32s32s32s32s32s", data
        )
        return SellEvent(
            timestamp=unpacked[0],
            base_amount_in=unpacked[1],
            min_quote_amount_out=unpacked[2],
            user_base_token_reserves=unpacked[3],
            user_quote_token_reserves=unpacked[4],
            pool_base_token_reserves=unpacked[5],
            pool_quote_token_reserves=unpacked[6],
            quote_amount_out=unpacked[7],
            lp_fee_basis_points=unpacked[8],
            lp_fee=unpacked[9],
            protocol_fee_basis_points=unpacked[10],
            protocol_fee=unpacked[11],
            quote_amount_out_without_lp_fee=unpacked[12],
            user_quote_amount_out=unpacked[13],
            pool=Pubkey(unpacked[14]),
            user=Pubkey(unpacked[15]),
            user_base_token_account=Pubkey(unpacked[16]),
            user_quote_token_account=Pubkey(unpacked[17]),
            protocol_fee_recipient=Pubkey(unpacked[18]),
            protocol_fee_recipient_token_account=Pubkey(unpacked[19]),
        )
