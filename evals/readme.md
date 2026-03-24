# Evaluation of LLM UD Quality

This folder contains the code for evaluating the quality of LLM-based UD parsing.

Metrics:
- LEMMA: Accuracy of lemmatization (number of correctly predicted lemmas / total number of tokens)
- UPOS: Accuracy of UPOS tagging (number of correctly predicted UPOS tags / total number of tokens)
- DEPREL: Accuracy of dependency relation labeling (number of correctly predicted DEPREL labels / total number of tokens)
- UAS: Unlabeled Attachment Score (number of correctly predicted head tokens / total number of tokens)
- LAS: Labeled Attachment Score (number of correctly predicted head tokens with correct DEPREL labels / total number of tokens)
- CYCLE_PROP: Proportion of sentences with cycles in the predicted dependency tree (number of sentences with cycles / total number of sentences)
- MULTI_ROOT_PROP: Proportion of sentences with multiple roots in the predicted dependency tree (number of sentences with multiple roots / total number of sentences)

## Running evaluation
To run the evaluation, you can use the `eval.py` script:

```bash 
python3 eval.py path/to/gold_conllu path/to/predicted_conllu
```

## Adding Evaluation Results

You can add the evaluation results of a language UD quality to the `results.csv` file.

Steps:
1. Run the evaluation script with the gold standard and predicted CONLL-U files for the language you want to evaluate
2. Create folder with the evaluated language name in ISO format (e.g., `eng`, `nld`, `rus`, `tat`) in `evals/languages`
3. In the crated folder, put the gold standard data in `gold` folder and LLM prediction in `output` folder
4. Add the evaluation results to `results.csv` file. Provide the following information: language ISO code, evaluated model, metrics, and link to the gold standard data