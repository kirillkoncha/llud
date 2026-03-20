from langchain_core.prompts import PromptTemplate

UD_PROMPT = PromptTemplate.from_template("""
You are a Universal Dependencies parser. Parse the following sentence in the given language into its UD representation.

Language (glottolog): {lang_code}
Sentence: "{sentence}"

Return ONLY JSON matching this schema:
{{
  "tokens": [
    {{
      "id": int,
      "form": str,
      "lemma": str,
      "upos": str,
      "head": int,
      "deprel": str,
      "feats": dict
    }}
  ]
}}

- Follow UD standard for {lang_code}.
- Always include ALL applicable UD morphological features in "feats".
- If a feature is relevant, it MUST be included.
- Possible features include: Animacy, Case, Gender, Number, Person, Tense, Mood, Aspect, Polarity, VerbForm, etc.
- If no features apply, return an empty dict.
- Always tokenize punctuation as separate tokens (e.g., ".", ",", "!", "?" must each be their own token with appropriate UPOS such as PUNCT).
- DO NOT include explanations or markdown.
""")
