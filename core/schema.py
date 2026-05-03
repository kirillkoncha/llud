from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class UDToken(BaseModel):
    """Single token in Universal Dependencies format."""

    id: int = Field(..., description="Token index (1-based).")
    form: str = Field(..., description="Surface form.")
    lemma: str = Field(..., description="Base form.")
    upos: str = Field(..., description="Universal POS tag.")
    head: int = Field(..., description="Head token ID (0 = root).")
    deprel: str = Field(..., description="Dependency relation.")
    feats: Optional[Dict[str, str]] = Field(
        default_factory=dict, description="Morphological features as key-value pairs."
    )


class TokenList(BaseModel):
    """List of UD tokens."""

    tokens: List[UDToken] = Field(..., description="Ordered list of tokens.")


class UDParse(BaseModel):
    """UD parse of a sentence."""

    sentence: str = Field(..., description="Original sentence.")
    tokens: TokenList = Field(..., description="Token annotations.")

    def to_str(self) -> str:
        lines: list[str] = []
        lines.append(f"# text = {self.sentence}")

        for tok in self.tokens.tokens:
            feats_str = (
                "|".join(f"{k}={v}" for k, v in sorted(tok.feats.items()))
                if tok.feats
                else "_"
            )

            line = "\t".join(
                [
                    str(tok.id),
                    tok.form,
                    tok.lemma,
                    tok.upos,
                    "_",
                    feats_str,
                    str(tok.head),
                    tok.deprel,
                    "_",
                    "_",
                ]
            )
            lines.append(line)

        return "\n".join(lines)
