3# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
My domain is student review of CS professor at Boston University. This knowledge might be hard to find for incoming students who are unfamiliar with resources or any students that are new to the major. 

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 500 characters

**Overlap:** 100 characters

**Reasoning:** My sources consists of short to medium length reviews where information is often contained within one or two paragraphs. I belive chunk size of 500 characters is suitable because it is large enough to preserve complete opinions and the context while remaining small enough for precise retrieval. Overlap size of 100 character is big enough to provide context in case of cut

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2 via sentence-transformers

**Top-k:**5

**Production tradeoff reflection:**The most important thing I would prioritize is retrieval accuracy since more powerful embedding models may better capture the meaning of student reviews and return more relevant results. Next is Latency/performance as users would prefer fast search results. 

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about David Sullivan's teaching style?| Students generally describe Sullivan as clear, organized, engaging, and effective at teaching introductory programming concepts.|
| 2 | What opinions do students have about Christine Papadakis-Kanaris (CPK) as an instructor for CS112?|reviews regarding CPK are controversial. Some says that she is knowledgeable and supportive while other comments that her lectures are hard to follow |
| 3 | Which BU CS professors are most frequently recommended by students?| Professor David Sullivan|
| 4 | What opinions do students have about Mark Crovella?|  Students frequently describe him as "Awesome" (13 ratings) or "Great" (9 ratings), with very few lower ratings|
| 5 | What opinions do students have about Andrew Wood?|  Students frequently describe him as funny, engaging, and highly caring. He is known for using geometric patterns to teach concepts, making complex topics more approachable.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. There can be missing source attribution as not all professors in the department is included or information that the student need is not available in public.

2. Potentially noisy or inconsistent documents because different platforms can give different opinions about the same professor. 

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

Document Ingestion (Reddit Threads, RateMyProfessor revieww in documents table) -> Chunking (500-char chunks, 100-char overlap) -> Embedding + Vector Store (all-MiniLM-L6-v2 via sentence-transformers, ChromaDB) -> Retrieval (ChromaDB Similarity, Search (Top-k = 5)) -> Generation (Groq API, model: llama-3.3-70b-versatile)

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->
I will use Claude as my AI tool
For Document Ingestion, I will give My Documents section and the assignment requirements for document ingestion, and expect Python code that loads text files.
For Chunking, I will give my choosen chunking stratgy, specifying 500-characters chunks and 100-characters overlap, and expect a chunk_text() function that produces chunks.
For Embedding and Vector Store, I will input my retrieval approach section and architecture diagram and ask it to generate Python code that generates embeddings using all-MiniLM-L6-v2.
For retrieval, I will give my retrieval approach section specifying semantic search with Top-k = 5 and ask it to output a retrieval function that returns the five most relevant chunks and their source information.
For query interface, I will give my Architecture diagram, grounding requirements, and the assignment requirements for source attribution and ask it to generate code that uses the Groq API to generate answers  and a command-line interface that accepts user questions and displays the generated answer along with source citations.


**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
