from web3 import Web3
import hashlib
import json
import os

# -----------------------------
# Web3 setup (local Hardhat)
# -----------------------------

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    raise RuntimeError("Hardhat node is not running")

ACCOUNT = w3.eth.accounts[0]

# -----------------------------
# Contract ABI & address
# -----------------------------

ABI_PATH = "backend/blockchain/abi/MatchRegistry.json"
CONTRACT_ADDRESS = os.getenv(
    "MATCH_CONTRACT_ADDRESS",
    "0x5FbDB2315678afecb367f032d93F642f64180aa3"
)

with open(ABI_PATH) as f:
    abi = json.load(f)

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

# -----------------------------
# Helpers
# -----------------------------

def sha256_bytes(value: str) -> bytes:
    return hashlib.sha256(value.encode()).digest()


def generate_match_id(student_id: str, faculty_id: str, project_id: str) -> str:
    """
    Deterministic match id (important for auditability)
    """
    return hashlib.sha256(
        f"{student_id}:{faculty_id}:{project_id}".encode()
    ).hexdigest()

# -----------------------------
# Core commit function
# -----------------------------

def commit_match(
    student_id: str,
    faculty_id: str,
    project_id: str,
    final_score: float,
    match_mode: str,
    explanation: str
) -> str:
    """
    Commits a match record to blockchain.
    Returns match_id (hex string).
    """

    match_id = generate_match_id(student_id, faculty_id, project_id)

    tx = contract.functions.commitMatch(
        sha256_bytes(match_id),                  # matchId
        sha256_bytes(student_id),                # studentHash
        sha256_bytes(faculty_id),                # facultyHash
        int(final_score * 10000),                # preserve decimals
        match_mode,
        sha256_bytes(explanation)                # explanationHash
    ).transact({"from": ACCOUNT})

    w3.eth.wait_for_transaction_receipt(tx)
    return match_id
