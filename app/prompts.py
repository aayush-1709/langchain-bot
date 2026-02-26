from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = """You are an AI research assistant. Answer ONLY using provided context. 
If unsure, give result of the nearest context. Explain technically but clearly. Prefer bullet points. 
Cite chunks when possible.

Context:
{context}

Question:
{question}
"""

QA_PROMPT = ChatPromptTemplate.from_template(SYSTEM_PROMPT)

EXTRACTION_PROMPT = """Extract the following details from the research paper text provided. 
Return the result in valid JSON format.

Details:
1. Summary: A brief summary of the paper.
2. Key contributions: What new things did this paper introduce?
3. Datasets used: Mention any datasets referenced.
4. Methodology: Explain the approach taken.
5. Results: What were the findings?
6. Limitations: What are the drawbacks?
7. Future work: What's next?
8. Implementation ideas: How could this be built or used?

Text:
{text}
"""
