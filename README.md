# Shifting Symbols

## Description
Imagine a machine that reads a tape of finite length. The machine has two arms. One arm is labeled Head. The other is labeled Exec. Exec has an internal memory that stores a single symbol.

Head reads each symbol on the tape sequentially, and, when it reaches the end, it wraps back around to the front. Each symbol is an instruction for Exec. There are five symbols:

- Left ('<') causes Exec to move left
- Right ('>') causes Exec to move right
- Up ('^') causes Exec to increment the symbol in memory.
- Down ('\\') causes Exec to decrement the symbol in memory.
- Place ('#') causes Exec to place the symbol that is stored in memory at the position that it currently is.

The effect is that the tape contains a series of instructions for how to modify the tape. These modified instructions are used to, again, modify the tape.

## Stasis
When the tape is run for an adequate number of times, the machine trends towards a predictable state. I call this state "stasis". There are three catagories of stasis.

### Type 0
Type 0 stasis occurs when the tape lacks any ability to edit itself. This means that there are no Place symbols on the tape. Type 0 stasis can be determined by only looking at the tape, not the positions of the Head and Exec Arms. An interesting subcatagory of Type 0 stasis is homogenous stasis, when all symbols are the same.

### Type 1
Type 1 stasis occurs when the tape has symbols which allow editing of the tape, but the tape cannot be editted. To understand why this might happen, we need to talk about vectors. We can abstract the tape to a 2D plane by letting the X-axis represent a position on the tape, and the Y-axis represent symbols. The tape itself then becomes a series of points in 2D space. For example, using the encoding in the program, a left symbol at position 5 would be (5, 1).

The left, right, up and down symbols can be thought of as orienting the Exec head in the plane. A collection of these symbols can therefore be thought of as a vector. I call the vector resulting from a string of orienting symbols with no place symbols a "shift vector". The vector that points from Exec's current position to the next shift vector is called the "orienting vector". (As we may be in the middle of a shift vector)

For example, in the tape #<^^\\#>\\<, there are two shift vectors: (-1, 1) and (0, -1). If Head was over the second '^' symbol, the orienting vector would be (0, -1). 

I posit that all Type 1 stasises are the result of shift vectors that only point to points that are on the tape. Thus, the check for Type 1 stasis is like so:

Let E = Position Vector of the Exec Head.

1. Start = E+Orienting
2. Check that the tape position at Start's X coordinate is equal to Start. If so, continue. Else, this is NOT type 1 stasis.
3. Current = Start 
4. Shift_Vector = (next shift vector)
5. Current += Shift_Vector
6. If Current.y == Tape[Current.x].y, continue. Else, NOT Type 1 stasis.
7. If Current.x == Start.x, this IS Type 1 Stasis. Else, return to Step 4.

### Type 2 Stasis
Type 2 stasis occurs when the tape has symbols that allow self-modification, and the tape DOES self modify, but the modifications are periodic. No research has been done on these fascinating phenomena.