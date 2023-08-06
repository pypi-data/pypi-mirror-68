import torch
from overrides import overrides

from vtorch.common.utils import tensor_to_ohe

from .default import PredictionPostprocessor


class MulticlassPostprocessor(PredictionPostprocessor):
    @overrides  # type: ignore
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        _, max_indexes = logits.max(axis=1)  # type: ignore
        ohe_class_predictions = tensor_to_ohe(max_indexes, logits.size(1))
        return ohe_class_predictions
