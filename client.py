from fountain import Fountain
from glass import Glass

import time

m = """
DNA Fountain contains
a few adjustments so that the Fountain Codes algorithm can work specifically for DNA
data storage. These alterations include a preprocessing stage and a post-processing
stage. In the preprocessing stage, the data files to be stored are compressed. Not only
does this step make the dataset smaller, it also gives the data a large amount of
entropy, or randomness. The randomization of data is important for the adjustments
made in the post-processing stage. The type of compression tool used can be deter-
mined by the user   . After
compressing the dataset, the next steps are the same as Fountain Codes. Based on
the packet length l, chosen by the user, the dataset is split up into K equal length
segments. The robust Soliton distribution is used to generate droplets based off of
the standard LT codes algorithm and the seed used for the PRNGs is prepended to
each resulting sequence.The post-processing stage includes the possible addition of an error correction
code, converting the data with a mapping scheme, and screening droplets based off
of biological constraints. For the error correction code, DNA Fountain uses a Reed
Solomon code that is appended to each droplet’s sequence This can be checked for errors during
decoding. Next, bits are converted to nucleotides with a basic mapping scheme After each droplet’s sequence is converted to nucleotides, the
droplet reaches the screening stage.
The screening stage checks that each droplet’s sequence conforms to two of the
biological constraints The algorithm watches for sequences
that contain repeating nucleotides or an amount of GC content that is outside of an
accepted range around 50%. If the sequence of a given droplet is found to have either
of these two properties, the droplet is thrown out. The specifics of these constraints
can be set by the user, however, the DNA Fountain implementation was tested with
three for the maximum amount of repeating nucleotides and a range of 5% around
50% GC content. While many droplets are screened in this stage, Fountain Codes
are rateless, and the algorithm can continue to generate droplets. When droplets
are excluded for not passing both biological constraints, more droplets are simply
generated until a certain number of sequences are accepted. The number of sequences
generated can be determined by the user for a variable amount of redundancy.
At this point, it is important to note that the Fountain Code is no longer rateless.
Once a given number of sequences are generated, those are the only ones that will
be stored. When decoding the information from the DNA, more droplets cannot
be generated and the system must be able to recover the dataset from the stored
DNA. Since information can also be lost during the synthesis, storage, and sequencing
processes, generating the number of droplets necessary for recovering the information
is a vital feature of the algorithm. We performed an analysis on the DNA Fountain
implementation in order to determine the overall ability to recover encoded datasets.
It was discovered that the DNA Fountain implementation was not successful in
decoding the encoded data in all cases. There are some small flaws in the DNA
Fountain implementation of the Fountain Codes algorithm that can make the data
recovery improbable.
In particular, the screening stage of DNA Fountain can have a negative impact
on the performance of the algorithm in practice. In test runs for decoding random
binary data of different sizes, the average number of screened droplets can reach
around 90%. 
This means that there is
a high probability of losing any given droplet even before DNA synthesis, storage, and
sequencing. Since a certain distribution of degree values for each droplet is expected,
and certain single-segment droplets are needed for the decoding process, this screening
can potentially remove the metaphorical pieces needed to complete the puzzle.
Specifically, this algorithm does not work well for encoding small files (less than
100 KB) because it is difficult for the algorithm to achieve the desired degree distribution and to gather the needed droplets. For example, an analysis on a 1 KB file
found that two of the single-segment droplets had the same segment. Fortunately,
storing small files is not an efficient use of the DNA data storage architecture at this
point in time.
This algorithm also works well if the dataset is compressed beforehand. After a
compression algorithm is applied, the resulting randomized data is less likely to map
to sequences that would be screened out. If the dataset is compressed and efficiently
randomized, single-segment droplets are not likely to be screened out more often than
other multiple-segment droplets. However, since there is a high probability that any
given droplet will be excluded, there is potential to lose a highly important “linchpin”
type of droplet that could make the difference in a successful decoding process.
In the DNA Fountain program a bug was discovered on the decoding side that
could effect the ability of the program to decode an encoded dataset. As was previously described, the encoding screens sequences for homopolymer runs and GC
content. Therefore, sequences that do not pass these requirements should not be
seen when attempting to decode. If sequences are seen on the decoding side that
would not have passed screening during encoding, then there must have been an error
that occurred in that sequence and the program would not process those sequences
Screening for these types of sequences on the decoding side is a valid step but the code
is located in the wrong spot. On the encoding side, this stage happens after the seed
and error correction values are appended to the payload. However, on the decoding
side, the screening happens after the error correction value has been removed. Because
of this difference (with and without the error correction value), the GC content may
be different and the decoding ends up excluding sequences that did not have errors in
them. Excluding these extra sequences can have a negative impact on the program’s
ability to recover the original information.
Another issue with the DNA Fountain program is the runtime performance. For
files larger than 10 MB, the decoding time becomes an issue for a realistic DNA data
storage application. Since a DNA data storage architecture would be needed to store
large amounts of data, an application that takes days or even weeks to decode tens to
hundreds of megabytes of information is not feasible. A decrease in runtime was found
in two main areas. The first is the screening stage. It takes the encoding longer by
generating more droplets in order to find a given number of valid sequences that can
pass the screening stage. Secondly, a bug was discovered in the decoding code that
added an exponential amount of processing time. This single line of code mapped
the decoded bytes of data to a char representation before writing to the output file.
This line is not necessary as python allows bytes to be written directly to a file.
For our encoding and decoding implementation, we chose to integrate our hex-tocodon 
mapping scheme and translation process into the DNA Fountain codes algorithm. 
we decided that the Fountain Codes algorithm was one of the most promising designs.
The Fountain Codes algorithm balances a variable amount of parity and redundancy
that can be fine-tuned by the user. Another helpful element of this design is the use
of the XOR operation which can minimize repeating patterns within the data. Since
the indexing seed values represent droplets instead of sequences, this algorithm can
be configured to be scalable for large amounts of data. The Fountain Codes algorithm
is also ideal because the mapping scheme is completely separate from the rest of the
encoding and decoding processes.

Much of the algorithm follows the original LT codes design for Fountain Codes. We
split the data into equal length segments, where the number of bytes encoded in each
segment is determined by the user. From those segments, we generate droplets with
the same robust Soliton distribution. We also use a Reed Solomon code appended to
each droplet’s sequence. Then, the major difference is that we convert each droplet’s
sequence of binary data to a sequence of nucleotides using the mapping scheme and
translation process detailed in Section 4.1. On the decoding side, the map is also
used to convert nucleotides back to their binary representation, before the segment
recovery process can begin. More details about the code implementation can be found
in the documentation located in Appendix A.
73
Besides employing our hex-to-codon mapping scheme, we integrated two other
major updates to the algorithm. These updates include removing the screening stage
and altering the decoding algorithm.
Now, for our implementation, droplets are no longer
discarded if their sequences do not pass the two biological constraints. Instead,
our translation process attempts to find a valid sequence within a given number
of backtracks. By setting a limit for the number of times the system can backtrack,
we shorten the running time. However, there is a chance that the system cannot
find a valid sequence within the limit of times backtracked. If a valid sequence is not
found, the droplets with these types of sequences are then excluded. Although, by
moving the biological constraint satisfaction process from a post-processing screening
stage to the translation process we still observed two main improvements over the
DNA Fountain algorithm.
The fact that droplets are not excluded at as high of a rate has a positive affect on
the the algorithm’s ability to recover encoded data. Our algorithm typically discards
about 10% of the droplets generated, while DNA Fountain can exclude up to 88%.
Since our algorithm does not exclude a majority of droplets, we are more likely to
reach the intended distribution. We are also more likely to keep the single-segment
droplets that are imperative to the successful recovery of the data. As an unintended
side affect, we also achieved an decrease in running time. Since DNA Fountain has
74
to generate more droplets than are actually accepted, there is a waste in processing
time. Another chance to improve the running time was discovered in the decoding
algorithm.
We made changes to the decoding algorithm in order to speed up the computational
running time. More specifically, we changed the way single-segment droplets are
propagated throughout other droplets with the same segment. Erlich and Zeilinski’s
DNA Fountain implementation used a depth-first approach for following the path
of connected droplets. We instead used a breadth-first approach which showed a
significant decrease in running time.
After the preliminary recovery and translation of each sequence, the key value
is used to seed both random number generators and eventually, each droplet knows
how many segments it contains and exactly which segments from the original dataset
it contains. Similar to the DNA Fountain decoding algorithm, our implementation
also starts by examining droplets with exactly one segment. Now, other recovered
droplets may also include that segment and need to remove it. The difference in our
decoding approach is the order in which individual recovered segments are removed
from the other droplets that also contain that segment.
DNA Fountain solves the depth-first approach with a recursive function. The
function starts with a recovered segment. It then finds other droplets that have the
same segment. It starts at the beginning of that list of other droplets and removes
the segment from the first droplet. There is a chance that the first droplet in the list
only has two total segments. So if the initial segment is removed, the process has now
recovered one other single-segment.
Instead of moving on to the other droplets that contain the initial segment, the function now processes the newly recovered segment.
Each time a single-segment is recovered, it is processed immediately.
On the other hand, we implemented a breadth-first approach for processing these
single-segments. Therefore, when a recovered segment is removed from a droplet
with two segments and a new single-segment is discovered, that segment is added
to a first-in-first-out (FIFO) queue, instead of being immediately processed. The
starting single-segment is first removed from all other droplets that also contain that
segment. Any time a new single-segment is discovered, it is simply added to the
queue. Once the starting single-segment is finished being removed from all other
droplets, the algorithm moves on to process the first segment in the queue. This
process is repeated until the queue is empty. If all single-segments in the queue have
been processed and the dataset has not been completely encoded, more droplets are
processed.
The results of a breadth-first decoding approach versus a depth-first approach
includes less calls to the XOR operation in the code. For example, for tests run on a
randomly generated one megabyte file, the depth-first DNA Fountain implementation
made 723,706 calls to the XOR operation. On the other hand, our REDNAM
breadth-first implementation only made 14,636 calls to the XOR operation. The line
of code for the XOR operation is one of the most expensive in terms of computational
runtime.

"""

fountain_object = Fountain(m)
