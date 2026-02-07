// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract MatchRegistry {

    struct MatchRecord {
        bytes32 studentHash;
        bytes32 facultyHash;
        uint256 finalScore;
        string matchMode;
        bytes32 explanationHash;
        uint256 timestamp;
    }

    // matchId => MatchRecord
    mapping(bytes32 => MatchRecord) private matches;

    event MatchCommitted(bytes32 indexed matchId);

    /**
     * Commit a match decision to the blockchain.
     * Each matchId can be committed only once.
     */
    function commitMatch(
        bytes32 matchId,
        bytes32 studentHash,
        bytes32 facultyHash,
        uint256 finalScore,
        string memory matchMode,
        bytes32 explanationHash
    ) public {
        require(matches[matchId].timestamp == 0, "Already committed");

        matches[matchId] = MatchRecord(
            studentHash,
            facultyHash,
            finalScore,
            matchMode,
            explanationHash,
            block.timestamp
        );

        emit MatchCommitted(matchId);
    }

    /**
     * Read-only helper to verify a committed match.
     * Returns empty values if matchId does not exist.
     */
    function getMatch(bytes32 matchId)
        public
        view
        returns (MatchRecord memory)
    {
        return matches[matchId];
    }
}
