## Grammar Rule Extractor

##### Domain             : Natural Language Processing
##### Sub-Domain         : Language Processing
##### Techniques         : Grammer Rule Extraction
##### Application Domain : Language Modeling

### Description
1. Extracted from the BROWN file all grammar rules embedded in parse trees. (Did not consider punctuation as a nonterminal and eliminated numbers attached to non-terminals such as '-1', '-2', etc.)
2. Reported the following:
	1. number of distinct rules found.
	2. the 10 most frequent rules regardless of the non-terminal on the left-hand side	
	3. the non-terminal with the most alternate rules (i.e. the non-terminal that can have most diverse structures).
3. Estimated the above grammar size if lexicalized (i.e. to add head words to some of the rules).

##### Languages   : Python
##### Tools/IDE   : Anaconda
##### Libraries   : 

##### Duration    : 

Current Version  : v1.0.0.13

Last Update      : 03.16.2018 (Time : 04:20 P.M)
