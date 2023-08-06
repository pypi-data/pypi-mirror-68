# dependency-paraphraser
A sentence paraphraser based on dependency parsing 
and word embedding similarity.

The basic usage (for Russian language) is based on Natasha library:


```python
import dependency_paraphraser.natasha
import random
random.seed(1)
# the command below requires additional RAM, but enables synonym replacement
# otherwise, you can support your own w2v model in Gensim format
dependency_paraphraser.natasha.use_news_embeddings()
text = 'Карл у Клары украл кораллы'
for i in range(5):
    print(dependency_paraphraser.natasha.paraphrase(text))
# Карл похитил кораллы у Клары
# украл Карл кораллы у Клары
# украл у Клары Карл кораллы
# Карл отнял у Клары кораллы
# Карл украл кораллы у Клары
```
