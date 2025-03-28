import utils
import json, os, io, struct, base58, base64
from sell_event_decoder import SellEvent

pumpfun_amm = "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA"

# check if file exists, if not get tx
if not os.path.exists("tx_amm.json"):
    tx = utils.getTX(
        "3W6ybgQPz3qq1XFijcH9GzBThb2oyS4NSDmyfwoioKngBPwnaFg3C3waShwuee6QtfjLcGZpForZy9jxHHUsD7BE"
    )
    with open("tx_amm.json", "w") as f:
        json.dump(tx, f)
else:
    with open("tx_amm.json", "r") as f:
        tx = json.load(f)

# pretty print json
# print(json.dumps(tx, indent=4))

amm_ix = tx["result"]["transaction"]["message"]["instructions"][4]
amm_ix_data = amm_ix["data"]
amm_ix_accounts = amm_ix["accounts"]


# amm data struct
class swap_args:
    def __init__(self):
        self.base_amount_out = 0
        self.max_quote_amount_in = 0

    def __str__(self):
        return (
            "base_amount_out: "
            + str(self.base_amount_out)
            + " max_quote_amount_in: "
            + str(self.max_quote_amount_in)
        )


def bin_to_swap_args(data: bytes) -> swap_args:
    arg = swap_args()
    buffer = io.BytesIO(data)
    # ignore first 8 bytes
    buffer.read(8)
    arg.base_amount_out = struct.unpack("<Q", buffer.read(8))[0]
    arg.max_quote_amount_in = struct.unpack("<Q", buffer.read(8))[0]
    return arg


def decode_data(data: str) -> bytes:
    if not data:
        raise ValueError("data is empty")
    try:
        decoded = base58.b58decode(data)

    except Exception as e:
        raise ValueError("Error decoding base64 data") from e
    return decoded


decoded_data = decode_data(amm_ix_data)
args = bin_to_swap_args(decoded_data)

assert len(decoded_data) == 16 + 8
assert args.base_amount_out == 24280378766
assert args.max_quote_amount_in == 7151622
assert decoded_data[:8] == bytes(
    [51, 230, 133, 164, 1, 127, 131, 173]
)  # sell identifier
# buy identifier bytes([102, 6, 61, 18, 1, 218, 235, 234])

pool = utils.get_account_by_index(tx, amm_ix_accounts[0])
user = utils.get_account_by_index(tx, amm_ix_accounts[1])
global_config = utils.get_account_by_index(tx, amm_ix_accounts[2])
base_mint = utils.get_account_by_index(tx, amm_ix_accounts[3])
quote_mint = utils.get_account_by_index(tx, amm_ix_accounts[4])
user_base_token_account = utils.get_account_by_index(tx, amm_ix_accounts[5])
user_quote_token_amount = utils.get_account_by_index(tx, amm_ix_accounts[6])
pool_base_token_account = utils.get_account_by_index(tx, amm_ix_accounts[7])
pool_quote_token_account = utils.get_account_by_index(tx, amm_ix_accounts[8])
protocol_fee_receipent = utils.get_account_by_index(tx, amm_ix_accounts[9])
protocol_fee_receipent_token_account = utils.get_account_by_index(
    tx, amm_ix_accounts[10]
)
base_token_program = utils.get_account_by_index(tx, amm_ix_accounts[11])
quote_token_program = utils.get_account_by_index(tx, amm_ix_accounts[12])
system_program = utils.get_account_by_index(tx, amm_ix_accounts[13])
ata_program = utils.get_account_by_index(tx, amm_ix_accounts[14])
event_authority = utils.get_account_by_index(tx, amm_ix_accounts[15])
program = utils.get_account_by_index(tx, amm_ix_accounts[16])


assert pool == "FZfk5akAiF1StjSLshXRVYyKUKTmEKsU3fQRHnProEGr"
assert user == "9RyAKViy6kGmMoi4qXttFdugMYzDYJdvHfEpcoyKXBeM"
assert global_config == "ADyA8hdefvWN2dbGGWFotbzWxrAvLW83WG6QCVXvJKqw"
assert base_mint == "Ghz2qnfmZjGFCYgzS3K8vA5QZzh1fbNeUYSUw346pump"
assert quote_mint == "So11111111111111111111111111111111111111112"
assert user_base_token_account == "B5oFU8nACVPMNFiutq3m7VAQh3NcYXZo9kDWhNBuAvMq"
assert user_quote_token_amount == "CdH8MTfM3uXxWyonwYz65DSja5R73W4aNp7hMc2p8u45"
assert pool_base_token_account == "2a5LH6CjTsrBK3J6h8FRnRDTqK8NyCisQZ3eDMHnAixL"
assert pool_quote_token_account == "26bPB7zj2T3Lwg6reM7hUMKiWc4p1aiJWaSfTsRRhFSm"
assert protocol_fee_receipent == "7hTckgnGnLQR6sdH7YkqFTAA7VwTfYFaZ6EhEsU3saCX"
assert (
    protocol_fee_receipent_token_account
    == "X5QPJcpph4mBAJDzc4hRziFftSbcygV59kRb2Fu6Je1"
)
assert base_token_program == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
assert quote_token_program == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
assert system_program == "11111111111111111111111111111111"
assert ata_program == "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
assert event_authority == "GS4CU59F31iL7aR2Q8zVS8DRrcRnXX1yjQ66TqNVQnaR"
assert program == "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA"


log_data = "Pi83CqUD3CpwcdxnAAAAAI4tOacFAAAABiBtAAAAAACOLTmnBQAAAAAAAAAAAAAAor8bPEXKAADrvpFrEgAAALXHgwAAAAAAFAAAAAAAAAB5QwAAAAAAAAUAAAAAAAAA3xAAAAAAAAA8hIMAAAAAAF1zgwAAAAAA2GICaSBcjvYyhpap2jRjJNRArZo5NUf3pdLOtVAUZKt9Qu+XNrjSBor8vae0hg7n648Hi26/eL/NBmjdha0arpXPfKZrymyxPap9pdiD5Npyoaq1sNkD39drGouX8zBUrLuzLac41f0NeWasYTn1ibV2tnD1El0ZqdT5nKSKo2pjg3MADqIssmTTSv9koEte+r+7dN3NBImXsZgVR9fREAe0ZyjFA6fIFZjsUWe5tjKg2nvc6Y8HxZZ7EO1veKHO"
decode_log_data = base64.b64decode(log_data)
print(len(decode_log_data))

print(8 + 14 * 8 + 6 * 32)
assert len(decode_log_data) == 8 + 14 * 8 + 6 * 32

sell_event = SellEvent.decode(decode_log_data[8:])
print(sell_event)

