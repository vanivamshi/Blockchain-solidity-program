# Blockchain-solidity-program

Part of the paper - Enabling secure lightweight mobile narrowband internet of things (nb-iot) applications using blockchain

Developed as a part of my Ph.D. research, assessible at - https://doi.org/10.1016/j.jnca.2023.103723

Scyther verification programs
1) Device_ID.spdl - ID generation
2) Device_join.spdl - Device authentication when joining a new cell

Ethereum programs
1) Main smart contract - Defines the PoA connecting base station and devices. And ZKP to validate devices to transfer files to base stations
2) Two base station smart contract - Defines the data sharing between base stations

Authentication programs
1) Device_ID - ID generation
2) Device_join - Device authentication when joining a new cell

File nomenclature:
1) client_X.py - client file common to both real-time and full authentication
2) server_X_full - server file for full authentication
3) server_X_realtime - server file for realtime authentication
