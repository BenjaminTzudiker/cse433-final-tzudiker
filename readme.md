### Setup

Make sure you have python installed. Set your command line directory to the project folder.

`cd [path_to_project]`


### Specifying Miners

The miners.txt file defines all the cryptocurrency users that will mine blocks or otherwise participate in the simulation. Each miner has its own line, formatted like so:

name processing_power [role [role_arguments...]]

* name: The name is a unique string identifier used to track the miner for log and attack/defense purposes
* processing_power: The chance of a new block being mined every second; set to 0 to disable mining altogether
* role: Optional argument to denote a role apart from a generic miner; options include attacker and merchant
    - attacker: Will attempt to cheat a merchant by sending them fake blocks with fraudulent "temporary" transaction information; takes the name of the target merchant as its only role_argument and must be declared after the merchant in miners.txt
    - merchant: Will send a fake product to another miner if the merchant is given money in a transaction; takes the number of additional blocks needed after the payment block before the "product" is delivered as a role_argument

Example miners.txt with attacker posessing 20% of the world's computation power and the merchant needing 5 blocks (the payment block plsu the 4 additional blocks) before delivering the product:

alice 0.1 attacker bob
bob 0.0 merchant 4
world 0.4