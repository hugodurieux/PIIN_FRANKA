"""
Model loader for trained GreyBoxNet checkpoints.

Plan:
  1. Load a checkpoint saved by training/train.py (state_dict .pt file + config.json).
  2. Reconstruct the GreyBoxNet with the correct architecture hyper-parameters.
  3. Return the model in eval mode with gradients globally disabled for inference speed.

This serves goal.md Objective 2 (1000 Hz real-time control) by providing the
fastest possible model loading path for the controller.
"""

from __future__ import annotations

import json
import os
from typing import Optional

import torch

from network.grey_box_net import GreyBoxNet


def load_grey_box_model(
    checkpoint_path: str,
    config_path: Optional[str] = None,
    device: str = "cpu",
) -> GreyBoxNet:
    """
    Load a trained GreyBoxNet from a checkpoint file.

    The training loop (training/train.py) saves:
      - ``<run_dir>/greybox_best.pt``  -- model state_dict
      - ``<run_dir>/config.json``      -- training args (hidden_dim, n_hidden_layers,
                                          activation, etc.)

    This function reads both files to reconstruct the exact architecture, loads
    the weights, and returns the model ready for inference (eval mode, no grad).

    Args:
        checkpoint_path: Path to the ``.pt`` state_dict file (e.g.
            ``models/run_20260601_120000/greybox_best.pt``).
        config_path: Path to the corresponding ``config.json``. If *None*,
            the loader looks for ``config.json`` in the same directory as
            the checkpoint. If no config is found, default architecture
            hyper-parameters are used (256 hidden, 4 layers, mish).
        device: Torch device string (``'cpu'`` or ``'cuda'``).

    Returns:
        A ``GreyBoxNet`` instance in eval mode with gradients disabled.

    Raises:
        FileNotFoundError: If *checkpoint_path* does not exist.
    """
    if not os.path.isfile(checkpoint_path):
        raise FileNotFoundError(
            f"Checkpoint not found: {checkpoint_path}"
        )

    # --- resolve config path ---
    if config_path is None:
        candidate = os.path.join(os.path.dirname(checkpoint_path), "config.json")
        if os.path.isfile(candidate):
            config_path = candidate

    # --- read architecture hyper-parameters ---
    hidden_dim = 256
    n_hidden_layers = 4
    activation = "mish"

    if config_path is not None and os.path.isfile(config_path):
        with open(config_path, "r") as fh:
            cfg = json.load(fh)
        hidden_dim = cfg.get("hidden_dim", hidden_dim)
        n_hidden_layers = cfg.get("n_hidden_layers", n_hidden_layers)
        activation = cfg.get("activation", activation)

    # --- build model and load weights ---
    model = GreyBoxNet(
        hidden_dim=hidden_dim,
        n_hidden_layers=n_hidden_layers,
        activation=activation,
    )
    state_dict = torch.load(checkpoint_path, map_location=device, weights_only=True)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()

    # Disable gradient computation globally for this model -- every parameter
    # is frozen so torch.no_grad() contexts are not strictly needed at call
    # sites, but the controller wraps inference in torch.no_grad() anyway for
    # explicitness.
    for param in model.parameters():
        param.requires_grad_(False)

    return model


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import tempfile

    # Create a dummy model, save it, and reload it.
    net = GreyBoxNet(hidden_dim=64, n_hidden_layers=2, activation="mish")

    with tempfile.TemporaryDirectory() as tmpdir:
        ckpt_path = os.path.join(tmpdir, "greybox_best.pt")
        cfg_path = os.path.join(tmpdir, "config.json")

        torch.save(net.state_dict(), ckpt_path)
        with open(cfg_path, "w") as fh:
            json.dump({"hidden_dim": 64, "n_hidden_layers": 2, "activation": "mish"}, fh)

        loaded = load_grey_box_model(ckpt_path, device="cpu")
        assert isinstance(loaded, GreyBoxNet)
        assert not any(p.requires_grad for p in loaded.parameters())

        # Verify identical output
        q = torch.randn(1, 7)
        qdot = torch.randn(1, 7)
        delta = torch.zeros(1, 1)
        with torch.no_grad():
            out_orig = net(q, qdot, delta)
            out_loaded = loaded(q, qdot, delta)
        assert torch.allclose(out_orig, out_loaded, atol=1e-6), "Outputs diverge!"

    print("model_loader smoke test OK")
