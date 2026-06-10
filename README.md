# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->


| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Best CS professors at BU discussion| Reddit thread| https://www.reddit.com/r/BostonU/comments/11dwqct/for_anyone_who_is_in_cs_who_are_some_professors/|
| 2 | General discussion of BU CS department quality | Reddit thread| https://www.reddit.com/r/BostonU/comments/18771oj/how_is_cs_at_bu/|
| 3 |CS112 with Papadakis-Kanaris (CPK) opinions| Reddit thread| https://www.reddit.com/r/BostonU/comments/1b208zp/cs112_cpk_opinion/|
| 4 | Rate My Professors - Prof. CPK | Professor review | https://www.ratemyprofessors.com/professor/2284300|
| 5 | Rate My Professors - Prof. Sullivan | Professor review| https://www.ratemyprofessors.com/professor/953067|
| 6 | Rate My Professors - Prof. Preethi| Professor review| https://www.ratemyprofessors.com/professor/2928441|
| 7 | Rate My Professors - Prof. Tiago | Professor review| https://www.ratemyprofessors.com/professor/2944043|
| 8 | Rate My Professors - Prof. Wood| Professor review| https://www.ratemyprofessors.com/professor/2834322|
| 9 | Rate My Professors - Prof. Erdos| Professor review| https://www.ratemyprofessors.com/professor/2239141|
| 10 | Rate My Professors - Prof. Crovella| Professor review| https://www.ratemyprofessors.com/professor/615539|

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Why these choices fit your documents:** My sources consists of short to medium length reviews where information is often contained within one or two paragraphs. I belive chunk size of 500 characters is suitable because it is large enough to preserve complete opinions and the context while remaining small enough for precise retrieval. 

**Final chunk count:**56

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**all-MiniLM-L6-v2 via sentence-transformers

**Production tradeoff reflection:**For a real deployment, the most important tradeoff I would weigh is retrieval accuracy on domain-specific informal text.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**The system prompt explicitly forbids the model from using outside knowledge with the instruction: "Answer ONLY using the information in the provided documents below. Do NOT use any outside knowledge or general assumptions about professors or courses." It also instructs the model to respond with exactly "I don't have enough information on that."
**How source attribution is surfaced in the response:**Source attribution is handled programmatically rather than being left to the LLM. After generation, the code collects the source filename from each retrieved chunk's metadata and deduplicates them with list(dict.fromkeys(...))

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about David Sullivan's teaching style?| Students generally describe Sullivan as clear, organized, engaging, and effective at teaching introductory programming concepts| According to the documents, students say that Professor Sullivan's teaching style is organized and clear. His lectures are described as "really engaging" (Document 2) and he is said to be "extremely outstanding when it comes to explaining material" (Document 3). Additionally, he provides tips in class for the weekly problem sets (Document 2) and posts lecture videos on Blackboard for students who miss class (Document 3). However, one student mentions that he can get "a little annoyed" when students talk during class (Document 3).| Relevant | Accurate|
| 2 | What opinions do students have about Christine Papadakis-Kanaris (CPK) as an instructor for CS112?| Reviews regarding CPK are controversial. Some says that she is knowledgeable and supportive while other comments that her lectures are hard to follow| Students have mixed opinions about Christine Papadakis-Kanaris (CPK) as an instructor for CS112. Some students think she is "pretty good" and "genuinely care[s] about her students", finding her explanations clear and appreciating her help outside of class. However, others criticize her as "unorganized, judgmental and condescending" and feel that she makes the course overly complicated. Some students also compare her unfavorably to another professor, Sullivan, who teaches the same course. Additionally, some students note that she has improved over time, with one student saying "it has gotten better but she used to be terrible".| Relevant | Accurate|
| 3 | Which BU CS professors are most frequently recommended by students?| Professor David Sullivan| According to the documents, the following BU CS professors are highly recommended by students: Andrew Wood, Vahid, and Erdos| Relevant | Partially accurate|
| 4 | What opinions do students have about Mark Crovella?| Students frequently describe him as "Awesome" (13 ratings) or "Great" (9 ratings), with very few lower ratings| Students have mixed opinions about Mark Crovella. Some students find his lectures "monotonous and boring" and not "super engaging" (Documents 1 and 2). However, they also respect him as a person and acknowledge his knowledge in Data Mechanics (Document 1). One student notes that despite the class content not being interesting, Crovella made the class "quite engaging and relatively easy" (Document 1). Another student calls him a "legend" and "goated in cs/ds field" (Document 2). Additionally, students appreciate his organization, online textbook, and fair exams (Document 5), with one student calling him a "GOAT prof" (Document 5).|Relevant | Accurate|
| 5 | What opinions do students have about Andrew Wood?| Students frequently describe him as funny, engaging, and highly caring. He is known for using geometric patterns to teach concepts, making complex topics more approachable.| Students have very positive opinions about Andrew Wood. They describe him as the "BEST PROF EVERRR", "the goat of goats", and "without a doubt the best professor I've had at BU so far". They praise his lectures, saying they are "amazing" and "incredibly engaging". They also appreciate his helpfulness and the relevance of his homework and projects, which they find "super fun". However, one student mentions that the class isn't the most organized and criticizes the homeworks as "very irresponsible".| Relevant | Accurate|

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**Opinions on Professor Mark Sullivan

**What the system returned:**According to the documents, students have a very positive opinion of Professor Mark Sullivan. He is described as "amazing", "the best", and "super goated". Students praise his organized and clear lectures, and appreciate that he posts lecture videos on Blackboard for easy catch-up. However, some students mention that he can get annoyed or angry during lectures, and that his grading can be a downside. Overall, students highly recommend him, with one student saying "if you put in consistent effort this class is an easy A".

**Root cause (tied to a specific pipeline stage):**The failure is in the generation stage, where the professor does not exist but the retriever still pulled chunks about David Sullivan because "Sullivan" matched semantically.

**What you would change to fix it:**Add an instruction to the system prompt telling the model to check that the retrieved documents specifically mention the person or topic being asked about, not just a similar name.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**he chunking strategy in planning.md — 500-character chunks with 100-character overlap — directly guided the implementation of chunk_text() without any ambiguity. Having the numbers decided before writing code meant the ingestion pipeline matched the spec exactly on the first attempt, and when the chunk count came back low (37 initially), it was clear the problem was document content rather than the chunking parameters.

**One way your implementation diverged from the spec, and why:**The planning.md listed Rate My Professors as direct URLs to scrape, but RMP uses JavaScript rendering that blocks automated requests. All RMP content had to be copied manually into .txt files instead. This was expected behavior noted in the assignment, but it meant the ingestion pipeline handles only local .txt files rather than live web scraping as the original architecture diagram implied.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*my Documents table, Chunking Strategy section, and pipeline diagram
- *What it produced:* ingest_and_chunk.py with a working clean_text() and chunk_text() function
- *What I changed or overrode:*I added more information to the txt files to increase the number of chunks

**Instance 2**

- *What I gave the AI:*My planning.md Retrieval Approach section, pipeline diagram, and the Milestone 5 requirement 
- *What it produced:* query.py file with a system prompt, a retrieval function that fetched top-5 chunks from ChromaDB, and a Gradio interface in app.py
- *What I changed or overrode:* I directed Claude to tighten the system prompt by adding an instruction telling the model to verify that retrieved documents mention the exact person being asked about, and to say "I don't have enough information on that" if they don't match.
