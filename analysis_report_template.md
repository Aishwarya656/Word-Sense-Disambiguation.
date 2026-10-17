# Word Sense Disambiguation — Short Analysis Report

## Objective
Explore WordNet senses and test a baseline algorithm for choosing the contextual meaning of ambiguous words.

## Tools
Python, NLTK, WordNet, Flask, HTML, CSS.

## Method
1. Enter a sentence and target word, or use multi-word analysis.
2. Retrieve candidate WordNet synsets and lexical relations.
3. Apply simplified Lesk as a baseline.
4. Export results and compare predictions with intended meanings.

## Test cases
Record actual outputs after running the application.

| Sentence | Target word | Intended sense | Predicted sense | Correct? |
|---|---|---|---|---|
| She deposited money in the bank. | bank | Financial institution | Fill after testing | Fill after testing |
| He sat on the bank of the river. | bank | Land beside a river | Fill after testing | Fill after testing |
| The bat flew out at dusk. | bat | Flying mammal | Fill after testing | Fill after testing |
| He swung the bat during the game. | bat | Sports equipment | Fill after testing | Fill after testing |
| The crane lifted a steel beam. | crane | Lifting machine | Fill after testing | Fill after testing |

## Analysis
Accuracy = (correct predictions / total test cases) × 100. Discuss incorrect predictions honestly. Lesk may struggle when context words do not overlap with WordNet glosses.

## Conclusion
Summarize the utility of lexical resources and the baseline's limitations.
