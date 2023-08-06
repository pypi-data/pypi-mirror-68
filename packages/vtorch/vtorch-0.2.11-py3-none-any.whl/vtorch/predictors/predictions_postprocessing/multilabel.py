from typing import Optional

import torch
from overrides import overrides

from .default import PredictionPostprocessor


class MultilabelPostprocessor(PredictionPostprocessor):
    def __init__(self, thresholds: Optional[torch.Tensor] = None, default_threshold: float = 0.5) -> None:
        self._default_threshold = default_threshold
        self._thresholds = thresholds

    @overrides  # type: ignore
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        if self._thresholds is None:
            self._thresholds = torch.ones((1, logits.size(-1))) * self._default_threshold

        if self._thresholds.size(-1) != logits.size(-1):
            raise ValueError(
                f"Thresholds have {self._thresholds.size()} size, but should have {logits.size()} as logits"
            )

        thresholds_with_logits_shape = torch.ones_like(logits) * self._thresholds
        predictions: torch.Tensor = torch.where(
            logits >= thresholds_with_logits_shape, torch.tensor([1.0]), torch.tensor([0.0])
        )
        return predictions
