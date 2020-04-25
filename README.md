# EPL448-Near-Duplicate-Detection-of-Fake-News-Articles
Team Project for EPL448 Data Mining - Near Duplicate Detection of Fake News Articles 

# Overview
## Python files
* createDataset.py - Used to create out json results gossipcop_results.json and politifact_results.json. By running it with your chosen dataset it will append any new information from your dataset to our json dataset by crawling the web to find near duplicate candidates
* evaluations.py - Calculates some statistical data about our algorithms results, and makes the plots for the Precision and Recall
* extract_articles.py - Used to extract the appropriate data from eacch article (title, url, content). Called from createDataset.py
* google_search.py - Used to crawl Google to find similar documents for a given document's title and returns an array of the results. Called from createDataset.py
* main.py - Holds same general functions used in most of the other files
* minhash_lsh.py - Implementation of the Minhash algorithm using Locality Sensitive Hashing and saves the results in the lsh_dataset.csv
* simhash1.py - Implementation of the Simhash algorithm and saves the results in the simhash_dataset.csv

## Datasets
* politifact_fake.csv - Samples related to fake news collected from PolitiFact
	* id - Unique identifider for each news
	* url - Url of the article from web that published that news
	* title - Title of the news article
	* tweet_ids - Tweet ids of tweets sharing the news. This field is list of tweet ids separated by tab.
* gossipcop_fake.csv - Samples related to fake news collected from GossipCop
	* id - Unique identifider for each news
	* url - Url of the article from web that published that news
	* title - Title of the news article
	* tweet_ids - Tweet ids of tweets sharing the news. This field is list of tweet ids separated by tab.
* fake_news_domain_list.csv - Known fake news domains
	* domain - Unique fake news domain
	* flag_description - Category of fake news (e.g. fake, conspiracy, political, etc.)
	* dataset - Url of the original dataset where this domain was flagged as fake news
* gossipcop_results.json - Holds the extracted articles for every query in the gossipcop_fake.csv we searched the web for
	* data - Array with all data
		* original_article - Object with the original query
			* url - Url of the original query
			* title - Title of the original query
			* content - Content of the original query
		* extracted_articles - Array with the extracted articles from the web by the original queries title
			* url - Url of the extracted article
			* title - Title of the extracted article
			* content - Content of extracted article
* politifact_results.json - Holds the extracted articles for every query in the politifact_fake.csv we searched the web for
	* data - Array with all data
		* original_article - Object with the original query
			* url - Url of the original query
			* title - Title of the original query
			* content - Content of the original query
		* extracted_articles - Array with the extracted articles from the web by the original queries title
			* url - Url of the extracted article
			* title - Title of the extracted article
			* content - Content of extracted article
* lsh_dataset.csv - Holds the results for the gossipcop_results.json and politifact_results.json datasets usint the LSH algorithm to find their near duplicates
	* dataset - Which dataset the original queery was exctracted from (Politifact/Gossipcop)
	* query - The original query url
	* duplicates - The near duplicates urls
* simhash_dataset.csv - Holds the results for the gossipcop_results.json and politifact_results.json datasets usint the SimHash algorithm to find their near duplicates
	* dataset - Which dataset the original queery was exctracted from (Politifact/Gossipcop)
	* query - The original query url
	* duplicates - The near duplicates urls
* fingerprints.csv - Fingerprints generated from the gossipcop_results.json and politifact_results.json using the SimHash algorithm
	* dataset - Which dataset the original queery was exctracted from (Politifact/Gossipcop)
	* query - The original query url
	* duplicates - The near duplicates urls
* sample_manual_checking.json - A sample of the gossipcop_results.json dataset used for human evaluation of the SimHash algorithm
	* data - Array with all data
		* original_article - Object with the original query
			* url - Url of the original query
			* title - Title of the original query
			* content - Content of the original query
		* extracted_articles - Array with the extracted articles from the web by the original queries title
			* url - Url of the extracted article
			* title - Title of the extracted article
			* content - Content of extracted article
			* dup - False near duplicate (0), True near duplicate (1) or Unknown (2)

Each of the above CSV files is comma separated file and the arrays items are space seperated.

# Installation
Install all the libraries in requirements.txt using the following command:
```
pip install -r requirements.txt
```

# References
The minimalistic version of the politifact_fake.csv and gossipcop_fake.csv datasets are a result of the work done for the FakeNewsNet project here https://github.com/KaiDMML/FakeNewsNet.
The fake_news_domain_list.csv dataset was provided to us for the purpose of this assingment.

If you use this dataset, please cite the following papers:
```
@article{shu2018fakenewsnet,
  title={FakeNewsNet: A Data Repository with News Content, Social Context and Dynamic Information for Studying Fake News on Social Media},
  author={Shu, Kai and  Mahudeswaran, Deepak and Wang, Suhang and Lee, Dongwon and Liu, Huan},
  journal={arXiv preprint arXiv:1809.01286},
  year={2018}
}
```
```
@article{shu2017fake,
  title={Fake News Detection on Social Media: A Data Mining Perspective},
  author={Shu, Kai and Sliva, Amy and Wang, Suhang and Tang, Jiliang and Liu, Huan},
  journal={ACM SIGKDD Explorations Newsletter},
  volume={19},
  number={1},
  pages={22--36},
  year={2017},
  publisher={ACM}
}
```
```
@article{shu2017exploiting,
  title={Exploiting Tri-Relationship for Fake News Detection},
  author={Shu, Kai and Wang, Suhang and Liu, Huan},
  journal={arXiv preprint arXiv:1712.07709},
  year={2017}
}
```
