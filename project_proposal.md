# CS-GY 6903 Fall 2024: Project 2

## Team Name
CHIVLry (**C**ollision resistant **H**ashing for **I**nsertion/deletion **V**irus **L**ocalisation)

## Team Members
Shravya Vorugallu (sv2630), Shubham Rastogi (sr7421), Giovanni Di Crescenzo

## Project Description

### Problem Statement:

The project aims to design and implement algorithms for localizing multiple insertions and deletions in a file using cryptographic hashing. This builds on existing research in the fields of single modification localization and combinatorial group testing.

#### Project 10 Summary

The project involves addressing:
1. **Single Insert/Delete Corruption**:
   - Localization of changes when only one corruption (insert or delete) occurs.
2. **Multiple Insert/Delete Corruptions**:
   - Extending the solution to handle multiple corruptions efficiently.

#### Breakup of Tasks:

1. **Literature Review**:
   - Study two referenced papers to understand existing algorithms and theoretical bounds.
2. **Localization Algorithms**:
   - Single Edit, Prepend, Append, Insert, and Delete Corruptions:
     - Extend the algorithm from Paper 1 to formally solve single insert/delete scenarios.
     - Derive theoretical bounds for these cases.
   - Multiple Insert/Delete Corruptions:
     - Take inspiration from Paper 2 to build a new algorithm.
3. **Implementation**:
   - Develop and test localization algorithms in Python.
4. **Performance Evaluation**:
   - Compare practical performance against theoretical bounds based on:
     - File size.
     - Localization factor.
     - Size of impacted block in the file due to corruption.
5. **Research Paper and Presentation**:
   - Summarize findings and prepare a visually appealing presentation.

#### Challenges:
1. Efficiently distinguishing between block shifts and actual corruptions.
2. Handling overlapping insertions and deletions.
3. Balancing accuracy and computational efficiency.

---

### Next Steps

1. **Phase 1: Problem Understanding**
   - Review referenced papers.
   - Understand single vs. multiple corruption scenarios.

2. **Phase 2: Initial Implementation**
   - Implement localization algorithms for single edit/prepend/append.
   - Extend to single insert/delete and derive theoretical bounds.
   - Test for correctness.

3. **Phase 3: Extending to Multiple Corruptions**
   - Build algorithms inspired by Paper 2 for localizing multiple inserts/deletions.
   - Focus on edge cases and computational efficiency.

4. **Phase 4: Performance Evaluation**
   - Evaluate algorithms on large-scale files using the following metrics:
     - File size.
     - Localization factor.
     - Size of impacted block by corruption.

5. **Phase 5: Research and Presentation**
   - Write the research paper summarizing findings.
   - Prepare a concise, visually appealing presentation.

---

### Detailed Additional Information

1. **Localization of Single Insertion/Deletion**:
    - **Paper 1**: Provides algorithms for single edit/prepend/append.
    - Extend Paper 1 to solve single insert/delete scenarios and derive theoretical bounds.

2. **Implementation of Localization Algorithms**:
    - **Paper 1**: Offers theoretical bounds for edit, prepend, and append.
    - Extend these algorithms to include insert/delete scenarios.
    - Evaluate performance in Python using the following parameters:
        - **File Size**: Measure scalability.
        - **Localization Factor**: Accuracy in pinpointing changes.
        - **Impacted Block Size**: Effectiveness in isolating corruption caused by a virus.

3. **Localization of Multiple Inserts/Deletions**:
    - **Paper 2**: Provides an algorithm for localizing multiple edits across files.
    - Use Paper 2 as inspiration to design algorithms for multiple inserts/deletions.
    - Implement the algorithm in Python and evaluate performance using the above metrics.

---

### Deliverables:

1. **Research Paper**:
   - Summarizes theoretical and practical findings.
   - Discusses algorithm extensions and their implications.

2. **Presentation**:
   - Highlights methodology, findings, and performance evaluation.

3. **Code**:
   - Implementation of localization algorithms for:
     - Single edits: Prepend, Append, Insert, Delete.
     - Multiple corruptions: Inserts and Deletes.
   - Performance evaluation comparing practical results with theoretical bounds.

---
### References:
1. [Cryptographic Hashing for Virus Localization](https://brightspace.nyu.edu/content/enforced/407023-204-1248_FA24CS-GYCS-UY47836903AIINET/worm06workshop-dicrescenzo.pdf)
2. [Combinatorial Group Testing
for Corruption Localizing Hashing](https://brightspace.nyu.edu/content/enforced/407023-204-1248_FA24CS-GYCS-UY47836903AIINET/LNCS%206842%20-%20Combinatorial%20Group%20Testing%20for%20Corruption%20Localizing%20Hashing.pdf)


