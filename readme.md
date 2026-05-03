# LLUD: Large Language Universal Dependencies

LLUD (Large Language Universal Dependencies) is a
small open-source library to get Universal Dependencies (UD) treebanks from LLM for any language.

The library asks LLM to parse sentence in UD format, and then converts
the output into a treebank format using LLM structured output.

## Installation

Clone the repository and install the dependencies:

```bash
pip install .
```

## Usage

Declare LLM provider and use it to initialize the UD parser (along with the language you want to parse):

```python
from core.parser import UDParser
from providers.llm import LLMProvider

provider = LLMProvider(
    provider_type="openai",
    model_name="gpt-4.1",
    api_key="sk-proj...",
)

# Use glottolog code for the language you want to parse
parser = UDParser(provider=provider, language="rus")
```

Get the output in the form of a treebank:

```python
response = parser.parse("Я вас любил, любовь еще быть может...")

print(response)
'''
Output:
# UDParse(sentence='Я вас любил, любовь еще быть может...', tokens=TokenList(tokens=[UDToken(id=1, form='Я',
lemma='я', upos='PRON', head=3, deprel='nsubj', feats={'Case': 'Nom', 'Number': 'Sing', 'Person': '1'}),
UDToken(id=2, form='вас', lemma='вы', upos='PRON', head=3,
deprel='obj', feats={'Case': 'Acc', 'Number': 'Plur', 'Person': '2'}), UDToken(id=3, form='любил',
lemma='любить', upos='VERB', head=0, deprel='root', feats={'Aspect': 'Imp', 'Gender': 'Masc', 'Mood': 'Ind', 'Number': 'Sing', 'Person': '1', 'Tense': 'Past',
'VerbForm': 'Fin'}), UDToken(id=4, form=',', lemma=',', upos='PUNCT', head=3, deprel='punct', feats={}), UDToken(id=5, form='любовь',
lemma='любовь', upos='NOUN', head=7, deprel='nsubj', feats={'Animacy': 'Inan', 'Case': 'Nom', 'Gender': 'Fem',
'Number': 'Sing'}), UDToken(id=6, form='еще', lemma='еще', upos='ADV', head=7, deprel='advmod', feats={}),
UDToken(id=7, form='быть', lemma='быть', upos='AUX', head=3, deprel='parataxis',
feats={'VerbForm': 'Inf'}), UDToken(id=8, form='может', lemma='мочь', upos='VERB',
head=7, deprel='aux', feats={'Aspect': 'Imp', 'Mood': 'Ind', 'Number': 'Sing', 'Person': '3',
'Tense': 'Pres', 'VerbForm': 'Fin'}), UDToken(id=9, form='...', lemma='...', upos='PUNCT', head=3, deprel='punct', feats={})]))
'''
```

Response also could be converted to CONLL-U string:

```python
response.to_str()
```

## Supported LLM Providers

Currently, the library supports OpenAI and Mistral AI providers. You can specify the provider type and model name when initializing the LLM provider.

More providers and capabilities (e.g., using locally deployed models) are planned for the future.

## Supported Languages

Project supports all languages, but the quality of the output depends on the LLM capabilities in a particular language. Expect better performance for high-resource languages, and worse for low-resource ones.

You can evaluate the performance of LLMs on a specific language. Instructions as well as quality metrics for the evaluated languages are available in `evals` folder.

## Contributing

Contributions are welcome! If you want to contribute, please fork the repository and create a pull request with your changes.