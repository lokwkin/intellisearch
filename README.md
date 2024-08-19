# intellisearch
***Ever experienced that when searching on Google, you often have to tweak or refine your keywords multiple times even for the same topic, and turns out the results are full of noises?*** 

**Intellisearch** aims to solve this problem by enhancing the pre and post-processing of search queries and results. It is a search optimizer for developers, integrators, and AI agents, to enhance search results by leveraging LLM-driven query refinement, search aggregation, and ML models filtering to deliver tailored, credible information and provide a more intelligent search experience. 

## What does it do?
#### Query Refinement
We leverage the latest advancements in reasoning and knowledge capabilities with LLMs to refine and suggest better queries and achieve optimal search results. Intellisearch classifies the original user’s query into vaiours categories, like broad or specific / question based / relates to geolocation or time, and more, and suggest queries according to the nature of the query.

#### Search Aggregation
Intellisearch currently aggregates news searches results from both Google News and Bing News, avoiding reliance on a single source. Upcoming we plan to integrate additional engines including Yahoo, Brave, Baidu, and possibly Exa.AI, and broaden the scope and variety of the results as possible.

#### Result Filtering / Reranking
The core strength of Intellisearch lies lies in its ability to filter or rerank search results by different criterias which are not commonly provided by popular search engines. We examine each of the resulting contents by applying a set of self-trained NLP Models and obtain a score indicating the credibility, timeniness, sentiment and other factors that are important to users and to the query.
