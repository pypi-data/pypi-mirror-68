# CyStack

CyStack is a small collection of FIFO and FILO data structures. In both cases 
the internal data structure is an std::vector<int>.

### Installation
`pip install CyStack`

## CyStack: Iterator
Integer FILO Data Structure
- push: adds an int value to the stack
- pop: removes and returns the newest int value
- Implements:
    - `__init__`: Takes any iterable
    - `__iter__`: Iterator
    - `__len__`: Size
    - `__str__`: String

## CyQueue: Iterator
Integer FIFO Data Structure
- push: adds an int value to the queue
- pop: removes and returns the oldest int value 
- Implements:
    - `__init__`: Takes any iterable
    - `__iter__`: Iterator
    - `__len__`: Size
    - `__str__`: String
