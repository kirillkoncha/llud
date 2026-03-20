from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class UDToken(BaseModel):
    id: int
    form: str
    lemma: str
    upos: str
    head: int
    deprel: str
    feats: Optional[Dict[str, str]] = Field(default_factory=dict)


class TokenList(BaseModel):
    tokens: List[UDToken]


class UDParse(BaseModel):
    sentence: str
    tokens: TokenList

    def to_str(self) -> str:
        lines: list[str] = []

        # Sentence metadata
        lines.append(f"# text = {self.sentence}")

        for tok in self.tokens.tokens:
            # FEATS formatting: key=value|key=value or "_"
            if tok.feats:
                feats_str = "|".join(f"{k}={v}" for k, v in sorted(tok.feats.items()))
            else:
                feats_str = "_"

            # CoNLL-U has 10 columns
            # ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC
            line = "\t".join(
                [
                    str(tok.id),
                    tok.form,
                    tok.lemma,
                    tok.upos,
                    "_",  # XPOS
                    feats_str,
                    str(tok.head),
                    tok.deprel,
                    "_",  # DEPS
                    "_",  # MISC
                ]
            )
            lines.append(line)

        return "\n".join(lines)
