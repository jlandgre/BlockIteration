class IterTest:
    """
    Example with block iteration to create a summary list
    JDL 5/16/22
    """
    def __init__(self, lstIters, iBlockSize, IsPrint=True):

        #iteration parameters
        self.lstIters = lstIters #list of items to process (iter counter rng
                                 #or simply a list of items)
        self.iBlockSize = iBlockSize #Block iteration reset limit
        self.IsPrint = IsPrint

        #Problem-specific params for this example
        self.lstSummary = [] #Output list created by ProcessItem()
        self.sumBlock = 0 #Interim lstSummary value
        self.sMsg = ''

    def Iterate(self):
        """
        Block iteration example; prints out interim results from while
        loop using BlockIteration class instance to manage iteration.
        BlockIteration class also in util.py for general usage
        """
        iter = BlockIteration(self.lstIters, self.iBlockSize, IsPrint=self.IsPrint)

        #Initial print (heading etc.) list posn initially 0
        self.PrintUpdate(iter)

        #Block iteration
        while iter.IsContinue:
            self.ProcessItem(iter)
            if iter.idxItem_Block >= iter.iBlockSize: self.ResetBlock(iter)
            
            #Cont if 1) not done with iters list 3) No fatal errors
            IsCond1 = iter.idxItem_Cur <= iter.nItersMax - 1
            IsCond2 = iter.iError == 0
            iter.IsContinue = IsCond1 and IsCond2
        
        #Process possible partial block at end
        if self.sumBlock > 0: self.ResetBlock(iter)

    def ProcessItem(self, iter):
        """ Process an individual list item"""

        #Add current item to sum (example processing task)
        self.sumBlock += self.lstIters[iter.idxItem_Cur]

        #[Optionally] If error occurred, set iter.iError

        #Increment item and block counters
        iter.idxItem_Cur += 1
        iter.idxItem_Block += 1

    def ResetBlock(self, iter):
        """
        Perform actions to process the block result, reset block iteration counter
        In this example, Reset appends a block-accumulated sum to a results list
        and resets sumBlock to 0
        """

        #Append the block's sum to the summary list and print an update
        self.lstSummary.append(self.sumBlock)
        self.sumBlock = 0
        iter.idxItem_Block = 0
        iter.idxCumBlocks += 1
        self.PrintUpdate(iter)

    def PrintUpdate(self, iter):
        s3 = 3 * ' '
        nl, nl2 = '\n', '\n\n'

        #If prior to first iteration
        if iter.idxItem_Cur == 0:
            iter.PrintAppendMsg(s3 + 'Starting to run:\n')

        #Otherwise, update with interim results
        else:
            sBlocks = str(iter.idxCumBlocks)
            sBlocks = sBlocks + (3 - len(sBlocks)) * ' '
            sIters = str(iter.idxItem_Cur)
            sIters = sIters + (5 - len(sIters)) * ' '
            sSubT = str(self.lstSummary[-1])
            sSubT = (3 - len(sSubT)) * ' ' + sSubT

            lst = [s3, sBlocks, s3, 'Iterations: ', sIters, 'Block subtotal: ', sSubT]
            iter.PrintAppendMsg(''.join(lst))

        #If iError != 0, print appropriate message
        if iter.iError==1: iter.PrintAppendMsg(nl2 + 'Something bad happened' + nl)

        #Add final suffix if Refresh iteration complete
        if not iter.IsContinue: iter.PrintAppendMsg(nl + s3 + 'All finished' + nl)

class BlockIteration():
    """
    Class for block iteration -  params track overall and interim reporting
    See iter_test.py for example
    JDL 6/16/22; refactored 8/12 to make attr nomenclature transparent

    Inputs
       lstIters [list; item type varies] List of items to process
       nItersMax [integer] Limit on cumulative number of sub-iterations
       iBlockSize [integer] Optional Block size, base 1 (n sub-iterations per block)
                            default 0 implies no sub-iteration
    """
    def __init__(self, lstIters, iBlockSize=0, IsPrint=True):

        #Number of iters and optional block size (used by app-specific code)
        self.nItersMax = len(lstIters) #[base 1]
        self.iBlockSize = iBlockSize #[base 1]

        #Internal variables managed by app-specific ProcessItem and ResetBlock code
        self.idxItem_Cur = 0 #idx for cum sub-iterations [base 0]
        self.idxItem_Block = 0 #idx for n sub-iterations within current block [base 0]
        self.idxCumBlocks = 0 #idx block counter [base 0]

        self.iError = 0
        self.IsContinue = True
        self.IsPrint = IsPrint
        self.sMsgs = ''
    
    def PrintAppendMsg(self, s):
        """
        Append interim message to self.sMsgs; optionally print
        """
        if self.IsPrint: print(s)
        self.sMsgs += s

print('\n\n Example where n_items doesn\'t evenly match block size\n')

test = IterTest(list(range(1, 51)), iBlockSize=3, IsPrint=True)
test.Iterate()
print('\n\n', test.lstSummary)

print('\n\n Example where n_items evenly matches block size\n')

test = IterTest(list(range(1, 51)), iBlockSize=2, IsPrint=True)
test.Iterate()
print('\n\n', test.lstSummary)