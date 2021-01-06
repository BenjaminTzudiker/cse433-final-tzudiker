import sys, random, time



class Miner:
    def __init__(self, name, processingPower, target=None, blocksBeforeDelivery=None):
        self.name = name
        self.processingPower = processingPower
        self.target = target
        self.blocksBeforeDelivery = blocksBeforeDelivery
        self.rootBlock = Block(None, 0, [])
        self.headBlock = self.rootBlock
        self.blocks = {0: self.rootBlock}
    
    def mine(self, miners):
        if self.processingPower > random.random():
            print(self.name + " mined new block")
            if self.target:
                # Attacker
                newBlock = Block(self, random.randint(1, 2147483647), transactions=[(self.target, self)], parent=self.headBlock)
                self.headBlock = newBlock
                self.blocks[newBlock.uid] = newBlock
                self.target.addBlock(newBlock)
            else:
                # Normal miner
                newBlock = Block(self, random.randint(1, 2147483647), parent=self.headBlock)
                self.headBlock = newBlock
                self.blocks[newBlock.uid] = newBlock
                for miner in miners:
                    miner.addBlock(newBlock)
        return False
    
    def addBlock(self, newBlock):
        if not newBlock.uid in self.blocks.keys():
            if newBlock.parentUID in self.blocks.keys():
                self.blocks[newBlock.uid] = newBlock
                if newBlock.depth > self.headBlock.depth:
                    self.headBlock = newBlock
                    if self.blocksBeforeDelivery:
                        upstreamBlock = self.headBlock
                        for i in range(self.blocksBeforeDelivery):
                            if upstreamBlock:
                                upstreamBlock = self.blocks[upstreamBlock.parentUID]
                        if upstreamBlock:
                            for transaction in upstreamBlock.transactions:
                                if transaction[0].name == self.name:
                                    transaction[1].deliver(self)
    
    def deliver(self, merchant):
        print("### " + merchant.name + " delivered product to " + self.name + "!")

class Block:
    def __init__(self, miner, uid, transactions=[], parent=None):
        self.miner = miner
        self.uid = uid
        self.transactions = transactions
        self.parentUID = parent.uid if parent else 0
        self.childUIDs = []
        if parent:
            parent.childUIDs.append(self.uid)
        self.depth = parent.depth + 1 if parent else 0


timeInterval = 1.0
miners = []


if len(sys.argv) < 2:
    print("Must specify miner list file in args")
    exit(0)

if len(sys.argv) > 2:
    timeInterval = float(sys.argv[2])

with open(sys.argv[1], 'r') as minersFile:
    minerStrings = minersFile.readlines()
    for minerString in minerStrings:
        minerArgs = minerString.strip('\n').strip('\r').split(' ')
        name = minerArgs[0]
        processingPower = float(minerArgs[1])
        role = minerArgs[2] if len(minerArgs) > 2 else None
        targetName = minerArgs[3] if role == "attacker" else None
        target = None
        for miner in miners:
            if targetName == miner.name:
                target = miner
        blocksBeforeDelivery = int(minerArgs[3]) if role == "merchant" else None
        miners.append(Miner(name, processingPower, target=target, blocksBeforeDelivery=blocksBeforeDelivery))

while True:
    for miner in miners:
        miner.mine(miners)
    time.sleep(timeInterval)