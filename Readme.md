This shares a "block iteration" Python utility class with an example that uses it to iterate in blocks.  We use this in consulting projects where it is desirable to iteratively perform some task such as updating from an eCommerce database where there is a limit on query size or a need to report results in chunks.

Project file **iter_test.py** contains a class called **IterTest** that serves as driver code.  It instances the **BlockIteration()** utility class, which manages iteration parameters.

To illustrate usage of the block iteration utility, **iter_test.py** instances the **IterTest** class with an integer range limit and block size to perform the dummy task of iterating from 1 to 50 in blocks of 3. Its example output is a list of subtotals of the integers in each block.  It prints interim updates with each block reset throughout the overall task.

<p align="center">
  iter_test.py block_iteration_output</br>
<img src=images/block_iteration_output.png "Block Iteration Output" width=600></br>
</p>

In general, basic code architecture for block iteration is:
* Instance the driver class with an integer block size input and any other inputs needed to define the iteration list [iter_test.py IterTest class].
  * In an **Iterate()** method, create a list of values to iterate over. This is a required input for the **BlockIterate** class. The nature of the list can vary depending on the use case.  It might be a range of integers as in the example, or it might consist of a list of strings or other values needed for the iteration task.  The **BlockIteration** utility uses length of the list to determine the maximum number of iterations
  * Instance the **BlockIteration** class to track iteration parameters
  * While loop until complete
    * Call **ProcessItem()** method to perform the "action" required for a single iteration
    * Whenever the current block's count index reaches the block size limit, call a **ResetBlock()** method to record or output the block's result and reset to begin a new block
    * If an error occurs or the task is completed prematurely, exit the loop
  * Outuput the overall results


  J.D. Landgrebe, DataDelve LLC
