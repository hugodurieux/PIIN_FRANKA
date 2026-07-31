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

from network.friction_net import FrictionNet
from network.grey_box_net import GreyBoxNet

# Filename training/train.py saves the FrictionNet weights under, alongside
# greybox_best.pt in the same run directory (see train.py's save block).
_FRICTION_CHECKPOINT_NAME = "friction_net_best.pt"


def load_friction_net(
    checkpoint_path: str,
    config_path: Optional[str] = None,
    device: str = "cpu",
) -> Optional[FrictionNet]:
    """
    Load the FrictionNet that was trained *jointly* with a GreyBoxNet checkpoint.

    2026-07-27: this closes a real train/deploy mismatch. ``training/train.py``
    composes the residual as

        tau_res = tau_res_grey + tau_res_fric      (step_loss(), --use_friction_net)

    and saves the two nets to two separate files in the same run directory
    (``greybox_best.pt`` and ``friction_net_best.pt``). Stage 3 only ever loaded
    the first one, so the deployed feedforward was missing a term the GreyBoxNet
    weights had been *jointly optimised against* -- the greybox head never had to
    explain the dissipative part of the residual, because FrictionNet was
    explaining it during training. Dropping it at inference does not just remove a
    small friction correction, it makes the remaining greybox output a biased
    estimate of the full residual. The current reference checkpoint
    (models/run_20260716_121302, config.json ``"use_friction_net": true``) is
    exactly such a checkpoint, and it is the one Stage 3 runs.

    Detection is driven by the checkpoint's OWN config.json (``use_friction_net``),
    not by a new caller-facing flag: a checkpoint knows how it was trained, and
    the controller must reproduce that composition or it is evaluating a different
    model than the one that was validated.

    Args:
        checkpoint_path: Path to the GreyBoxNet ``.pt`` file. The FrictionNet
            weights are looked for as ``friction_net_best.pt`` in the same directory.
        config_path: Path to ``config.json``. If *None*, looked up next to
            *checkpoint_path* (same rule as :func:`load_grey_box_model`).
        device: Torch device string.

    Returns:
        A ``FrictionNet`` in eval mode with gradients disabled, or *None* when the
        checkpoint was trained without one (``use_friction_net`` absent/false).

    Raises:
        FileNotFoundError: If the config says ``use_friction_net: true`` but the
            weights file is missing. This is deliberately loud rather than a
            silent fall-through to a greybox-only model -- a silently incomplete
            feedforward is precisely the failure this function exists to remove.
    """
    if config_path is None:
        candidate = os.path.join(os.path.dirname(checkpoint_path), "config.json")
        config_path = candidate if os.path.isfile(candidate) else None

    if config_path is None or not os.path.isfile(config_path):
        return None

    with open(config_path, "r") as fh:
        cfg = json.load(fh)
    if not cfg.get("use_friction_net", False):
        return None

    friction_path = os.path.join(
        os.path.dirname(checkpoint_path), _FRICTION_CHECKPOINT_NAME
    )
    if not os.path.isfile(friction_path):
        raise FileNotFoundError(
            f"{config_path} declares use_friction_net=true, but "
            f"{friction_path} is missing. Stage 3 would silently run a "
            "greybox-only feedforward that does not match the trained model."
        )

    # Must match the encoding the checkpoint was trained with, or the first
    # Linear layer's width will not match the saved weights.
    friction_net = FrictionNet(encoding=cfg.get("encoding", "sincos"))
    state_dict = torch.load(friction_path, map_location=device, weights_only=True)
    friction_net.load_state_dict(state_dict)
    friction_net.to(device)
    friction_net.eval()
    for param in friction_net.parameters():
        param.requires_grad_(False)
    return friction_net


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
    # Checkpoints saved before the encoding ablation existed have no
    # "encoding" key; they were all trained with sin/cos, so that is the
    # correct default. Getting this wrong is not a silent error -- the first
    # Linear layer would be 22-wide against 15-wide weights and load_state_dict
    # would raise -- but defaulting correctly keeps every existing run loadable.
    encoding = "sincos"

    if config_path is not None and os.path.isfile(config_path):
        with open(config_path, "r") as fh:
            cfg = json.load(fh)
        hidden_dim = cfg.get("hidden_dim", hidden_dim)
        n_hidden_layers = cfg.get("n_hidden_layers", n_hidden_layers)
        activation = cfg.get("activation", activation)
        encoding = cfg.get("encoding", encoding)

    # --- build model and load weights ---
    model = GreyBoxNet(
        hidden_dim=hidden_dim,
        n_hidden_layers=n_hidden_layers,
        activation=activation,
        encoding=encoding,
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
