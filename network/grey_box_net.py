"""
Grey-box residual network for the Franka Panda.

Novelty N1-Djeumou (goal.md Objectives 1 and 3 -- pre-existing architecture).

Architecture (project's own grey-box formulation, NOT Liu's energy network):

    tau_pred(q, qdot, qddot, delta) = RNEA(q, qdot, qddot)        [white box]
                                    + tau_res(q, qdot, delta)     [this network]

References:

  [N1-Djeumou] Compositional grey-box structure (known analytical terms + neural residual):
    Djeumou, Neary, Goubault, Putot, Topcu (2022). "Neural Networks with
    Physics-Informed Architectures and Constraints for Dynamical Systems Modeling."
    L4DC 2022, PMLR vol. 168.
    Borrowed: the compositional architecture principle of composing a known
    analytical term (here RNEA) with a neural residual (Section II, Eq. 1-2).
    The grey-box decomposition corroborates and validates this project's core design.

  [Liu et al. 2024] Smooth activations and input encoding:
    Liu, Borja, Della Santina (2024). "Physics-Informed Neural Networks to Model
    and Control Robots: A Theoretical and Experimental Investigation."
    Advanced Intelligent Systems (Wiley), vol. 6, no. 5.
    Borrowed: the requirement for smooth (twice-differentiable) activations from
    their energy-network formulation; adapted here for motor-torque smoothness
    (non-smooth ReLU outputs create torque discontinuities that jerk the motors).
    The [sin(q), cos(q)] input encoding prevents angle-wrapping singularities.

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
