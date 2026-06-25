"""
FrictionNet sub-module: structurally dissipative friction torque predictor.

Novelty N2-Liu (goal.md Objective 3 -- Scaling to 7-DoF with enforced physics).

Architecture:
    Input:  x = [sin(q), cos(q), qdot, delta] in R^22  (same encoding as GreyBoxNet)
    Hidden: Linear(22 -> 64) -> Mish -> Linear(64 -> 64) -> Mish
    Output: d = Linear(64 -> 7) (raw logits, one per joint)
    Friction matrix:  D = diag(Softplus(d) + eps),  eps = 1e-6  (strict positivity)
    Friction torque:  tau_friction = -D * qdot   (elementwise, D is diagonal)

Dissipativity guarantee (by construction):
    tau_friction . qdot = -sum_i Softplus(d_i) * qdot_i^2  <=  0   always

Activation constraint: Mish only in hidden layers. Softplus on output diagonal
is not an activation but a positivity transform -- allowed by project rules.

Design synthesises three sources:

  [N2-Liu] The Cholesky positive-definiteness idea originates in:
    Liu, Borja, Della Santina (2024). "Physics-Informed Neural Networks to Model
    and Control Robots: A Theoretical and Experimental Investigation."
    Advanced Intelligent Systems (Wiley), vol. 6, no. 5.
    Borrowed: the principle of enforcing positive-definiteness on the dissipation
    sub-network via a factored parameterisation (Section III-B, D-NN sub-network).

  [N1-Duong] The L L^T + eps*I algebraic kernel comes from:
    Duong, Altawaitan, Stanley, Atanasov (2024). "Port-Hamiltonian Neural ODE
    Networks on Lie Groups For Robot Dynamics Learning and Control."
    IEEE Transactions on Robotics.
    Borrowed: Cholesky-factored dissipation matrix L_v L_v^T (Section II-C),
    adapted here to joint space as diag(Softplus(d)) instead of full L L^T.

  [N1-SPEL] The diagonal sparsity mask (7 params instead of 28) comes from:
    Wang, Chen, Ding (2025). "Symplectic Physics-Embedded Learning via Lie Groups
    Hamiltonian Formulation for Serial Manipulator Dynamics Prediction."
    Scientific Reports (Nature), vol. 15, art. 33179.
    Borrowed: geometric argument that revolute joints rotating about a single axis
    produce a rank-1 per-link dissipation matrix (Section II-B), which collapses
    to a per-joint scalar in joint space for Franka's serial independent-motor chain.
"""

import torch
import torch.nn as nn

from network.constants import N_JOINTS, INPUT_DIM, OUTPUT_DIM, FRICTION_NET_HIDDEN
from network.grey_box_net import encode_state


class FrictionNet(nn.Module):
    """Predicts a structurally dissipative friction torque in R^7.

    The friction matrix D = diag(Softplus(d) + eps) is always positive-definite,
    so tau_friction = -D * qdot is guaranteed to satisfy tau_friction . qdot <= 0,
    i.e. the friction torque always removes energy from the system.

    Args:
        hidden_dim: Width of hidden layers (default: FRICTION_NET_HIDDEN = 64).
        eps: Small constant added to Softplus output for numerical stability.
    """

    def __init__(self, hidden_dim: int = FRICTION_NET_HIDDEN, eps: float = 1e-6):
        super().__init__()
        self.eps = eps
        self._softplus = nn.Softplus()

        self.backbone = nn.Sequential(
            nn.Linear(INPUT_DIM, hidden_dim),
            nn.Mish(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.Mish(),
        )
        self.head = nn.Linear(hidden_dim, OUTPUT_DIM)

    def forward_D(
        self, q: torch.Tensor, qdot: torch.Tensor, delta: torch.Tensor
    ) -> torch.Tensor:
        """Compute the diagonal of the friction matrix D.

        Args:
            q:     (B, 7) joint positions [rad].
            qdot:  (B, 7) joint velocities [rad/s].
            delta: (B, 1) or (B,) payload mass [kg].

        Returns:
            D_diag: (B, 7) diagonal entries of D (all strictly positive).
        """
        x = encode_state(q, qdot, delta)
        h = self.backbone(x)
        d = self.head(h)
        return self._softplus(d) + self.eps

    def forward(
        self, q: torch.Tensor, qdot: torch.Tensor, delta: torch.Tensor
    ) -> torch.Tensor:
        """Compute the dissipative friction torque.

        Args:
            q:     (B, 7) joint positions [rad].
            qdot:  (B, 7) joint velocities [rad/s].
            delta: (B, 1) or (B,) payload mass [kg].

        Returns:
            tau_friction: (B, 7)  =  -D_diag * qdot,  dissipative by construction.
        """
        D_diag = self.forward_D(q, qdot, delta)
        return -D_diag * qdot


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Smoke test: instantiate, forward pass, shape check, dissipativity
    # ------------------------------------------------------------------
    B = 8
    net = FrictionNet(hidden_dim=FRICTION_NET_HIDDEN)

    q = torch.randn(B, N_JOINTS)
    qdot = torch.randn(B, N_JOINTS)
    delta = torch.rand(B, 1)

    tau_friction = net(q, qdot, delta)
    assert tau_friction.shape == (B, OUTPUT_DIM), (
        f"Expected shape ({B}, {OUTPUT_DIM}), got {tuple(tau_friction.shape)}"
    )

    # Dissipativity check: tau_friction . qdot <= 0 for every sample
    power = (tau_friction * qdot).sum(dim=-1)
    assert (power <= 0).all(), (
        f"Dissipativity violated! power per sample = {power.tolist()}"
    )

    D_diag = net.forward_D(q, qdot, delta)
    assert D_diag.shape == (B, OUTPUT_DIM), (
        f"D_diag shape mismatch: expected ({B}, {OUTPUT_DIM}), got {tuple(D_diag.shape)}"
    )
    assert (D_diag > 0).all(), "D_diag must be strictly positive"

    n_params = sum(p.numel() for p in net.parameters())
    print(f"FrictionNet smoke test OK")
    print(f"  tau_friction shape: {tuple(tau_friction.shape)}")
    print(f"  D_diag shape:       {tuple(D_diag.shape)}")
    print(f"  D_diag mean/joint:  {D_diag.mean(0).tolist()}")
    print(f"  Power (should <= 0): {power.tolist()}")
    print(f"  Parameters:          {n_params}")
