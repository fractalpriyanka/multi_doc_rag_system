# RAG Evaluation — Multi-Document RAG System

## 1. Evaluation Overview

| Property | Details |
|---|---|
| Evaluation type | Offline evaluation |
| Evaluation dataset | Employee Handbook |
| Number of evaluation questions | 10 |
| Evaluation approach | Custom Gemini-based LLM-as-a-judge evaluation |
| Main evaluation focus | Faithfulness, answer relevancy, context precision, and context recall |
| Additional measurement | Answer-generation latency |

The evaluation assesses the quality of retrieved context and generated answers using a custom Gemini-based evaluation rubric.

---

## 2. Evaluation Dataset

A total of **10 questions** were used to evaluate the RAG system against the Employee Handbook.

### Evaluation Questions

| ID | Evaluation Question | Evaluation Focus |
|---|---|---|
| Q01 | What types of information are considered confidential? | Policy details and factual retrieval |
| Q02 | How should an employee report harassment? | Policy understanding and procedural information |
| Q03 | How far in advance should an employee request work from home? | Policy details and numerical information |
| Q04 | What does remote working mean according to the handbook? | Definition-based retrieval |
| Q05 | Can a supervisor date someone who reports directly to them? | Policy interpretation and direct factual retrieval |
| Q06 | What restrictions apply when an employee refers a relative for a job? | Policy details and multiple conditions |
| Q07 | Can non-employees solicit or distribute materials in the workplace? | Policy interpretation and direct factual retrieval |
| Q08 | What should an employee do if prescription medication unexpectedly affects their senses, thinking, or movement? | Workplace safety and procedural information |
| Q09 | How many paid sick-leave days are guaranteed by this finalized company policy? | Numerical information and identification of unresolved policy placeholders |
| Q10 | What is the company's official name and mission statement? | Identification of missing or unfinalized information |

### Question Diversity

The evaluation includes questions covering several types of information from the handbook.

| Question Category | Representative Questions |
|---|---|
| Confidentiality and data protection | Q01 |
| Harassment reporting and workplace conduct | Q02 |
| Work-from-home and remote-working policies | Q03, Q04 |
| Employee relationships and hiring restrictions | Q05, Q06 |
| Workplace solicitation and distribution | Q07 |
| Workplace safety and prescription medication | Q08 |
| Sick-leave policy and numerical details | Q09 |
| Missing or unfinalized company information | Q10 |

The dataset includes direct factual questions, policy-related questions, procedural questions, a numerical-policy question, and questions that require recognizing that the handbook contains unresolved placeholders or missing information.

---

## 3. Evaluation Methodology

A custom Gemini-based LLM-as-a-judge rubric was used to evaluate the system's responses across the 10 questions.

The evaluation covers four metrics:

- **Faithfulness:** Whether the generated answer is supported by the retrieved context.
- **Answer Relevancy:** Whether the answer addresses the user's question.
- **Context Precision:** Whether the retrieved context contains relevant information for answering the question.
- **Context Recall:** Whether the retrieved context captures the information required to answer the question.

The evaluation also records the generation latency for each question.

**Note:** The reported metric scores come from a custom evaluation approach and are not official RAGAS scores.

---

## 4. Evaluation Metrics and Results

| Metric | Score | What It Measures |
|---|---:|---|
| Faithfulness | 0.9500 | How well the generated answers are supported by the retrieved context |
| Answer Relevancy | 0.9100 | How relevant the generated answers are to the questions |
| Context Precision | 0.5300 | How relevant the retrieved context is to answering the questions |
| Context Recall | 0.8800 | How much of the required information is captured in the retrieved context |

### Interpretation

- **Faithfulness — 0.9500:** The generated answers received a high score for alignment with the retrieved context.
- **Answer Relevancy — 0.9100:** The answers received a high score for relevance to the questions.
- **Context Precision — 0.5300:** The comparatively lower score indicates that retrieved context relevance is an area for further improvement.
- **Context Recall — 0.8800:** The retrieved context received a high score for capturing the information required by the evaluator.

Overall, the results indicate stronger answer-level scores than context precision. Improving the relevance of retrieved chunks is therefore an important area to investigate.

These scores represent evaluation results, **not percentages of factual accuracy**.

---

## 5. Answer-Generation Latency

Generation latency was recorded for all 10 evaluation questions.

### Question-Level Latency

| Question ID | Generation Latency |
|---|---:|
| Q01 | 1,440.32 ms |
| Q02 | 1,452.38 ms |
| Q03 | 3,122.05 ms |
| Q04 | 1,257.37 ms |
| Q05 | 2,693.42 ms |
| Q06 | 1,589.39 ms |
| Q07 | 1,140.09 ms |
| Q08 | 2,435.48 ms |
| Q09 | 1,078.47 ms |
| Q10 | 819.16 ms |

### Latency Summary

| Metric | Result |
|---|---:|
| Number of recorded responses | 10 |
| Mean generation latency | 1,702.81 ms |
| Lowest generation latency | 819.16 ms |
| Highest generation latency | 3,122.05 ms |

**Interpretation:**

- The mean generation latency was approximately **1.70 seconds per response**.
- Q10 had the lowest recorded generation latency at 819.16 ms.
- Q03 had the highest recorded generation latency at 3,122.05 ms.
- These measurements describe answer-generation latency, not necessarily the complete end-to-end response time of the RAG pipeline.

---

## 6. Evaluation Summary

| Evaluation Area | Result |
|---|---:|
| Number of evaluation questions | 10 |
| Faithfulness | 0.9500 |
| Answer Relevancy | 0.9100 |
| Context Precision | 0.5300 |
| Context Recall | 0.8800 |
| Mean generation latency | 1,702.81 ms |
| Lowest generation latency | 819.16 ms |
| Highest generation latency | 3,122.05 ms |

The evaluation covers policy retrieval, procedural questions, definitions, numerical policy details, and questions involving missing or unfinalized information.

---

## 7. Evaluation Findings

The evaluation results highlight the following findings:

1. **Strong answer-level evaluation scores:** Faithfulness and answer relevancy received high scores under the custom evaluation rubric.
2. **Context precision needs attention:** The context precision score of 0.5300 is lower than the other reported metric scores, making retrieval relevance an important area for investigation.
3. **Policy-based questions are represented:** The dataset covers confidentiality, harassment, remote working, employee relationships, workplace conduct, and safety.
4. **Missing information is represented:** Q10 asks about the company's official name and mission statement, which are not finalized in the supplied handbook. The generated answer correctly responds that the information was not found in the document.
5. **Placeholder-sensitive questions are represented:** Q09 asks about finalized sick-leave entitlement, while the handbook contains bracketed placeholders. The generated answer repeats the placeholder value rather than presenting a finalized number.
6. **Generation latency varies:** The recorded generation latency ranges from 819.16 ms to 3,122.05 ms, with a mean of 1,702.81 ms.

---

## 8. Final Assessment

The Multi-Document RAG evaluation uses 10 questions from the Employee Handbook and a custom Gemini-based LLM-as-a-judge rubric.

The system achieved scores of 0.9500 for faithfulness, 0.9100 for answer relevancy, 0.5300 for context precision, and 0.8800 for context recall. The results show strong answer-level evaluation scores, while context precision remains the comparatively weaker metric.

The question set covers policy details, definitions, procedural information, numerical details, and missing or unfinalized information. Generation latency was also recorded for all 10 responses, with a mean of approximately 1.70 seconds.

**Overall status:** The documented evaluation covers four answer-and-context quality metrics across 10 questions, along with question-level and summary generation-latency measurements.
