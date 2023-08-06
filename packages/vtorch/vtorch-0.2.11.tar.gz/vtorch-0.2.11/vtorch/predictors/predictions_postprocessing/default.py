import torch


class PredictionPostprocessor:
    def postprocess(self, logits: torch.Tensor) -> torch.Tensor:
        pass
