import argparse
from binascii import hexlify, unhexlify
from ledger_bitcoin import createClient, Chain, MultisigWallet, AddressType
from ledger_bitcoin.psbt import PSBT

# --------------------------------------------------------------
# Constants
# --------------------------------------------------------------

CHAIN_MAP = {
    "mainnet": Chain.MAIN,
    "testnet": Chain.TEST,
    "regtest": Chain.REGTEST,
    "signet": Chain.SIGNET
}

# --------------------------------------------------------------
# Argument Parsers
# --------------------------------------------------------------

def argument_parser():
    argparser = argparse.ArgumentParser(epilog="""
        For more help, include a subcommand, for
        example `python3 ledger.py register --help`
    """)
    argparser.add_argument("-n", "--network",
                           help="Bitcoin network",
                           choices=CHAIN_MAP.keys(),
                           default="mainnet")
    subparsers = argparser.add_subparsers(title='Subcommands', dest='program')
    add_register_command(subparsers)
    add_receive_command(subparsers)
    add_sign_command(subparsers)
    return argparser.parse_args()

def add_register_command(subparsers):
    parser = subparsers.add_parser(
        'register',
        help="Register a multisig quorum with the Ledger device"
    )
    add_base_arguments(parser)

def add_receive_command(subparsers):
    parser = subparsers.add_parser(
        'receive',
        help="View a receive address on the Ledger device"
    )
    add_base_arguments(parser)
    add_additional_arguments(parser)

def add_sign_command(subparsers):
    parser = subparsers.add_parser(
        'sign',
        help="Sign a PSBT on the Ledger device"
    )
    add_base_arguments(parser)
    add_additional_arguments(parser)
    parser.add_argument('--psbt-file', type=argparse.FileType('r'))

def add_base_arguments(parser):
    parser.add_argument("-w", "--wallet", type=str,
                          help="Wallet name", required=True)
    parser.add_argument("-m", "--threshold", type=int,
                          help="Signing threshold", required=True)
    parser.add_argument('-k', '--key-expression', action='append', type=str,
                          help='Key expressions (specify N)', required=True)

def add_additional_arguments(parser):
    parser.add_argument("-c", "--change", type=int,
                          help="Change flag",
                          choices={0, 1}, required=True)
    parser.add_argument("-i", "--index", type=int,
                          help="Address index", required=True)
    parser.add_argument("--policy-hmac", type=str,
                          help="Policy hmac", required=True)

# --------------------------------------------------------------
# Programs
# --------------------------------------------------------------

def register(client, wallet_name, threshold, key_expressions):
    multisig_policy = MultisigWallet(
        name=wallet_name,
        address_type=AddressType.WIT,
        threshold=threshold,
        keys_info=key_expressions)
    policy_id, policy_hmac = client.register_wallet(multisig_policy)
    print(f"Policy id: { hexlify(policy_id).decode() }")
    print(f"Policy hmac: { hexlify(policy_hmac).decode() } ")


def receive(client, wallet_name, threshold, key_expressions, change, index, policy_hmac):
    multisig_policy = MultisigWallet(
        name=wallet_name,
        address_type=AddressType.WIT,
        threshold=threshold,
        keys_info=key_expressions)
    addr = client.get_wallet_address(
        multisig_policy, unhexlify(policy_hmac),
        change=change, address_index=index, display=True)
    print(f"Receive address: { addr }")


def sign(client, wallet_name, threshold, key_expressions,
         change, index, policy_hmac, psbt_file):
    print(policy_hmac)
    multisig_policy = MultisigWallet(
        name=wallet_name,
        address_type=AddressType.WIT,
        threshold=threshold,
        keys_info=key_expressions)
    psbt = None
    with psbt_file as f:
        psbt = PSBT()
        psbt.deserialize(f.read())
    signatures = client.sign_psbt(psbt, multisig_policy, unhexlify(policy_hmac))
    fingerprint = client.get_master_fingerprint().hex()
    for psbt_in_idx, psbt_in in enumerate(psbt.inputs):
        signature = signatures[psbt_in_idx]
        for pubkey, key_origin_info in psbt_in.hd_keypaths.items():
            some_fingerprint = hexlify(key_origin_info.fingerprint).decode()
            if fingerprint == some_fingerprint:
                psbt_in.partial_sigs[pubkey] = signature
    print(f"Updated PSBT: {psbt.serialize()}")


# --------------------------------------------------------------
# Main
# --------------------------------------------------------------

def main():
    args = argument_parser()
    client = createClient(chain=CHAIN_MAP[args.network])
    if args.program == "register":
        register(client, args.wallet, args.threshold, args.key_expression)
    if args.program == "receive":
        receive(client, args.wallet, args.threshold, args.key_expression,
                args.change, args.index, args.policy_hmac)
    if args.program == "sign":
        sign(client, args.wallet, args.threshold, args.key_expression,
             args.change, args.index, args.policy_hmac, args.psbt_file)

if __name__ == "__main__":
    main()
