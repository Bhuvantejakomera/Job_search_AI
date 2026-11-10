---
name: indeed-search
version: 1.0.0
description: >
  Search live job listings from Indeed (indeed.com / in.indeed.com) for India,
  remote, or international markets. Supports queries for Generative AI, Machine
  Learning, Python development, Data Science, and Software Engineering roles.
context: fork
enabled: true
---

# Indeed Search Skill

Search job listings on **Indeed** for India, remote, or international markets.

## Scope
- Generative AI & LLM Engineering roles
- Machine Learning & Computer Vision roles
- Data Science & Data Analytics roles
- Full-Stack & Python Software Development roles

## Search Query Pattern
When searching Indeed, use web search queries targeting active job postings:
- `site:in.indeed.com/viewjob "<Job Title>" "<Location/Remote>"`
- `site:indeed.com/viewjob "<Skill or Title>" remote`

## Output Schema
Each discovered listing should record:
- **Title**: Job designation
- **Company**: Employer name
- **Location**: City or Remote
- **Summary**: Key requirements and technology stack
- **URL**: Direct posting link

