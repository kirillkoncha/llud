from langchain_core.prompts import PromptTemplate


UD_PROMPT = PromptTemplate.from_template(
    """
You are a Universal Dependencies (UD) parser. Parse the given sentence into a UD-compliant representation.

Return ONLY JSON strictly matching this schema:
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

Rules:

1. **Single-root tree:**
   - Exactly ONE token must have head=0 and deprel='root'.
   - This token is the root of the sentence.

2. **No cycles (dependency tree must be a valid tree):**
   - Each token must have exactly one head (cannot be missing).
   - No token can be its own head (no self-loops).
   - Starting from any token, repeatedly follow the head links:
       token → head → head of head → ...
     This chain MUST eventually reach the root (head=0).
   - It must NEVER revisit a previously visited token.
   - Example of invalid cycles:
       5 → 7 → 5
       3 → 4 → 6 → 3
   - Example of self-loop:
       8 → 8
   - Example of valid chain:
       5 → 7 → 8 → 0

3. **Connectivity:**
   - All tokens must be connected to the root directly or indirectly.
   - No disconnected subtrees are allowed.

4. **Punctuation:**
   - Each punctuation mark is a separate token with UPOS=PUNCT.

5. **Morphological features:**
   - Include all relevant features in "feats" (e.g., Case, Gender, Number, Tense, Mood, Person, Animacy, etc.).
   - If none apply, use an empty dictionary.

6. **Coordination:**
   - Use `cc` for conjunctions and `conj` for coordinated elements.
   - Conjuncts must attach to the first conjunct or its head correctly.

7. **ADP/case attachments:**
   - Attach ADP tokens (prepositions/postpositions) as `case` to the noun they govern.

8. **Output constraints:**
   - No explanations, no markdown.
   - Only valid JSON matching the schema.

**Validation before output:**
- Confirm there is exactly one root.
- Confirm no token points to itself.
- Confirm no cycles exist (all head chains eventually reach root without loops).
- Confirm all tokens are connected to the root.

Language (glottolog): {lang_code}
Sentence: "{sentence}"
"""
)
