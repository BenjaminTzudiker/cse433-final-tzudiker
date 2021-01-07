### File Structure

* mine.py - Python file for running attack code
* miners - Folder containing example scenarios
    - miners_trusting.txt - Example where the merchant just needs to receive a single up to date block to ship an order. As soon as alice mines a single block, her attack is successful.
    - miners_oneblock.txt - Slightly more secure example; the merchant waits until the payment block is followed by a second block in its active chain. This likely isn't enough, and even alice's <50% share of the total computation power should let her almost immediately cheat bob.
    - miners_fiveblocks.txt - As above, but waits five blocks; in this example, the attacker is unlikely to trick the merchant into delivering the item with its only 20% computer power.
    - miners_majoritycomputation.txt - As above, but the attacker has more than 50% of the available computation power and thus can bypass the merchant's security measures. Alice should pretty quickly be able ot trick bob into a false delivery.
    - miners_manyminers.txt - Example involving many additional parties to demonstrate blockchain building.
    - miners_complex.txt - A scernario meant to highlight the possible complex scenarios one can playw ith using this tool. Here, there are two merchants and three attackers. With the current settings, it's unlikely any of the attacks will be successful.


### Setup and Run

Make sure you have python installed. Set your command line directory to the project folder.

```
cd [path_to_project]
python3 mine.py miners_text_file_location [iteration_time]
```

For example, to run the miners_trusting example scenario, run mine.py like so:

```
cd [path_to_project]
python3 mine.py miners/miners_trusting.txt 0.01
```

The program will print out each time a user mines a block, as well as whenever a merchant is tricked into delivering a product.

End the program (ctrl+c) to see each user's current longest blockchain (the chain considered valid at that moment).


### Specifying Custom Scenarios

The miners text file defines all the cryptocurrency users that will mine blocks or otherwise participate in the simulation. You'll need to make a new one to define your own custom scenarios.

Each miner has its own line, formatted like so:

name processing_power [role [role_arguments...]]

* name: The name is a unique string identifier used to track the miner for log and attack/defense purposes
* processing_power: The chance of a new block being mined every iteration; set to 0 to disable mining altogether
* role: Optional argument to denote a role apart from a generic miner; options include attacker and merchant
    - attacker: Will attempt to cheat a merchant by sending them fake blocks with fraudulent "temporary" transaction information; takes the name of the target merchant as its only role_argument and must be declared after the merchant in miners text file
    - merchant: Will send a fake product to another miner if the merchant is given money in a transaction; takes the number of additional blocks needed after the payment block before the "product" is delivered as a role_argument

Example miners.txt with attacker posessing 20% of the world's computation power and the merchant needing 5 blocks (the payment block plsu the 4 additional blocks) before delivering the product:

```
alice 0.01 attacker bob
bob 0.0 merchant 4
world 0.04
```