// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract TenderRegistry {
    struct Tender {
        bool exists;
        bool active;
        bytes32 dataHash;
    }

    struct Offer {
        address contractor;
        uint256 price;
        bytes32 dataHash; // хэш данных предложения
    }

    mapping(uint => Tender) public tenders;
    mapping(uint => Offer[]) public tenderOffers;

    function addTender(uint tenderId, bytes32 dataHash) public {
        require(!tenders[tenderId].exists, "Tender already exists");
        tenders[tenderId] = Tender({
            exists: true,
            active: true,
            dataHash: dataHash
        });
    }

    function addOffer(uint tenderId, bytes32 dataHash, uint256 price) public {
        require(tenders[tenderId].exists, "Tender does not exist");
        require(tenders[tenderId].active == true, "Tender not active");
        tenderOffers[tenderId].push(Offer({
            contractor: msg.sender,
            price: price,
            dataHash: dataHash
        }));
    }

    function getTenderHash(uint tenderId) public view returns (bytes32) {
        require(tenders[tenderId].exists, "Tender does not exist");
        return tenders[tenderId].dataHash;
    }

    function closeTender(uint tenderId, uint winnerOfferIndex) public {
        require(tenders[tenderId].exists, "Tender does not exist");
        require(tenders[tenderId].active == true, "Already closed");
        require(winnerOfferIndex < tenderOffers[tenderId].length, "Invalid offer index");
        tenders[tenderId].active = false;
        // Можно добавить логику записи победителя, но для простоты здесь только закрываем.
    }

    // Дополнительно можно сделать getter для офферов
    function getOfferCount(uint tenderId) public view returns (uint) {
        return tenderOffers[tenderId].length;
    }

    function getOffer(uint tenderId, uint index) public view returns (address contractor, uint256 price, bytes32 dataHash) {
        require(tenderOffers[tenderId].length > index, "No such offer");
        Offer memory o = tenderOffers[tenderId][index];
        return (o.contractor, o.price, o.dataHash);
    }
}
