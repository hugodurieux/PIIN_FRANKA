"""
Grey-box residual network for the Franka Panda.

Architecture (project's own grey-box formulation, NOT Liu's energy network):

    tau_pred(q, qdot, qddot, delta) = RNEA(q, qdot, qddot)        [white box]
                                    + tau_res(q, qdot, delta)     [this network]

Design choices grounded in Liu et al. (2024):
  - Smooth activations (Mish/Softplus): Liu's energy network must be differentiated
    twice, so it requires smooth activations. We keep smooth activations here too,
    but for a control-specific reason: non-smooth (ReLU) outputs create torque
    discontinuities that jerk the motors. ReLU is therefore FORBIDDEN.
  - The residual is a function of (q, qdot, delta) only, NOT qddot: friction and
    transmission effects are acceleration-independent (Coulomb/viscous depend on
    qdot and sign(qdot)). The known payload mass delta is also fed to RNEA, so the
    residual only learns the genuinely unmodeled part + load-dependent friction.

Input encoding: X = [sin(q), cos(q), qdot, delta] in R^22
Output: tau_res in R^7
"""

import torch
import torch.nn as nn

from network.constants import N_JOINTS, INPUT_DIM, OUTPUT_DIM


def encode_state(q: torch.Tensor, qdot: torch.Tensor, delta: torch.Tensor) -> torch.Tensor:
    """
    Encode raw state into the network input X in R^22.

    Args:
        q:     (B, 7) joint positions [rad]
        qdot:  (B, 7) joint velocities [rad/s]
        delta: (B, 1) or (B,) payload mass [kg]

    Returns:
        X: (B, 22) encoded input
    """
    if delta.dim() == 1:
        delta = delta.unsqueeze(-1)
    return torch.cat([torch.sin(q), torch.cos(q), qdot, delta], dim=-1)


class GreyBoxNet(nn.Module):
    """MLP that predicts the residual torque tau_res in R^7."""

    def __init__(
        self,
        hidden_dim: int = 256,
        n_hidden_layers: int = 4,
        activation: str = "mish",
    ):
        super().__init__()

        act = self._make_activation(activation)

        layers = [nn.Linear(INPUT_DIM, hidden_dim), act()]
        for _ in range(n_hidden_layers - 1):
            layers += [nn.Linear(hidden_dim, hidden_dim), act()]
        layers += [nn.Linear(hidden_dim, OUTPUT_DIM)]  # no activation on output
        self.net = nn.Sequential(*layers)

    @staticmethod
    def _make_activation(name: str):
        """Return an activation class. ReLU is forbidden by project rule."""
        name = name.lower()
        if name == "mish":
            return nn.Mish
        if name == "softplus":
            return nn.Softplus
        raise ValueError(
            f"Activation '{name}' not allowed. Use 'mish' or 'softplus'. "
            "ReLU and other non-smooth activations are forbidden (motor jerk)."
        )

    def forward(
        self, q: torch.Tensor, qdot: torch.Tensor, delta: torch.Tensor
    ) -> torch.Tensor:
        """
        Args:
            q:     (B, 7)
            qdot:  (B, 7)
            delta: (B, 1) or (B,)
        Returns:
            tau_res: (B, 7)
        """
        x = encode_state(q, qdot, delta)
        return self.net(x)


if __name__ == "__main__":
    # Smoke test with random inputs of the correct shape
    B = 8
    net = GreyBoxNet(hidden_dim=64, n_hidden_layers=3, activation="mish")
    q = torch.randn(B, N_JOINTS)
    qdot = torch.randn(B, N_JOINTS)
    delta = torch.rand(B, 1)
    out = net(q, qdot, delta)
    assert out.shape == (B, OUTPUT_DIM), out.shape
    print("GreyBoxNet smoke test OK — output shape", tuple(out.shape))
    print("Parameters:", sum(p.numel() for p in net.parameters()))
