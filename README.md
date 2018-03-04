# hacktech-human-computer

This project was hacked together at Hacktech 2018 by
* Eric Chen
* Nicholas Currault
* Faith Dennis
* Emily Liang

The Human Computer is tool created for use in computer-science education.  It uses (reasonably) large groups of people to illustrate how basic computations can be broken into simple parts.  We have created the following use cases:

* simple communication (simple_signal.html)
    - Demonstrates how voltage can carry information over time.
* bitwise communication (binary_signal.html)
    - Really just a formalism of the simple communication framework
* binary adder (binary_adder.html)
    - Performs addition of binary numbers, an actual computation
    - Each user performs an operation equivalent to a single full adder
    - Carry bits are sent from user to user, and an overall result is gathered
* simplified binary adder (idea, not implemented yet)
* networking (idea, not implemented yet)
    - Each person simulates a router
    - A message is given to some user with a goal and several paths are calculated
    - The user must either copy the payload directly (slow) or split it into packets that are each sent on separate paths (fast)
