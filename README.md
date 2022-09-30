# zephyr
Zephyr is a service which allows users to pay for good and services using a crypto debit card. Users deposit crypto of any type into their Zephyr wallet. The user selects which type of crypto is their 'active' payment method. When a user pays with their card, Zephyr writes an IOU to it's ledger, indicating how much the user owes to the merchant. Funds are deducted from the wallet corresponding to the user's active payment method.

This repo serves as a demo for the Zephyr system, which is written in solidity on top of the Ethereum blockchain.
This repo contains four core components:
- Payment processor: processes transactions and maintains the transaction ledger 
- User Accout GUI: displays the user's account (wallets, active payment method, transaction list, balance, etc..)
- Point-of-sale GUI: Used by the merchant. Builds transactions, reads the user's debit card info from the card reader, then submits transactions to the server
- Card reader: Connected to the PoS GUI. Reads debit card data

Each component uses:
- Payment processor: Python, MySQL, Docker, flask RESTFUL
- User Accout GUI: Python, Django, Javascript, HTML, CSS
- Point-of-sale GUI: Python, Django, Javascript, HTML, CSS, PySerial
- Card reader: Arduino, C++

User Account GUI:
https://user-images.githubusercontent.com/28720154/193166789-424bcd17-e4c2-46b7-9d2d-a7df7143721a.mp4

PoS GUI:
<img width="1323" alt="image" src="https://user-images.githubusercontent.com/28720154/193166579-f71db018-459e-49de-9e47-42beb34b3e3f.png">
