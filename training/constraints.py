"""
Physics constraints enforced via an Augmented Lagrangian.

Novelties N2-Djeumou and N2-Liu (goal.md Objectives 3 and 4).

Two constraints:

  1. Torque limits  -- |tau_pred| <= TORQUE_LIMITS  (safety; mostly inactive in-distribution)
  2. Dissipativity  -- tau_res . qdot <= 0           (the informative one)

References:

  [N2-Djeumou] Augmented Lagrangian training algorithm (Algorithm 1):
    Djeumou, Neary, Goubault, Putot, Topcu (2022). "Neural Networks with
    Physics-Informed Architectures and Constraints for Dynamical Systems Modeling."
    L4DC 2022, PMLR vol. 168.
    Borrowed: augmented Lagrangian penalty form with dual-ascent multiplier updates
    (lambda <- max(0, lambda + rho * g_mean)), applied here to torque-limit and
    dissipativity constraints on the learned residual.

  [N2-Liu] Dissipativity constraint motivation:
    Liu, Borja, Della Santina (2024). "Physics-Informed Neural Networks to Model
    and Control Robots: A Theoretical and Experimental Investigation."
    Advanced Intelligent Systems (Wiley), vol. 6, no. 5.
    Borrowed: the physical requirement that the residual friction/damping term must
    dissipate energy (tau_res . qdot <= 0), which Liu et al. enforce via their
    D-NN sub-network structure. Here we enforce the same property as a soft
    AL constraint on the plain MLP residual, bridging their energy-network
    formulation with our RNEA grey-box architecture.

Sign convention: friction opposes motion, so friction power tau_friction . qdot <= 0.
If tau_res models friction + unmodeled effects, we penalise the positive part
max(0, tau_res . qdot), i.e. any energy the residual would INJECT into the system.

Augmented Lagrangian for an inequality g(x) <= 0:
    L_AL = lambda * c + (rho / 2) * c^2 ,  with  c = max(0, g + lambda/rho)... 
We use the standard penalty form:  psi = max(0, g),  term = lambda*psi + (rho/2)*psi^2,
and multiplier update  lambda <- max(0, lambda + rho * g_mean).
"""

import torch

from network.constants import TORQUE_LIMITS


class AugmentedLagrangian:
    """Holds multipliers and penalty weights for the physics constraints."""

    def __init__(self, rho: float = 1.0, device: str = "cpu"):
        self.rho = rho
        # one multiplier per constraint family (scalars are enough to start)
        self.lambda_torque = torch.zeros(1, device=device)
        self.lambda_dissip = torch.zeros(1, device=device)
        self._limits = TORQUE_LIMITS.to(device)

    # ---- constraint definitions -------------------------------------------------

    def constraint_torque_limit(self, tau_pred: torch.Tensor) -> torch.Tensor:
        """g = |tau_pred| - limit  (<= 0 desired). Returns per-element violation."""
        return tau_pred.abs() - self._limits  # (B, 7)

    def constraint_dissipativity(
        self, tau_res: torch.Tensor, qdot: torch.Tensor
    ) -> torch.Tensor:
        """g = tau_res . qdot  (<= 0 desired). Returns per-sample violation (B, 1)."""
        power = (tau_res * qdot).sum(dim=-1, keepdim=True)  # (B, 1)
        return power

    # ---- augmented Lagrangian terms --------------------------------------------

    def penalty(self, tau_pred: torch.Tensor, tau_res: torch.Tensor,
                qdot: torch.Tensor) -> torch.Tensor:
        """Total AL penalty added to the MSE loss (a scalar)."""
        g_t = self.constraint_torque_limit(tau_pred)
        g_d = self.constraint_dissipativity(tau_res, qdot)

        psi_t = torch.clamp(g_t, min=0.0)
        psi_d = torch.clamp(g_d, min=0.0)

        term_t = (self.lambda_torque * psi_t + 0.5 * self.rho * psi_t.pow(2)).mean()
        term_d = (self.lambda_dissip * psi_d + 0.5 * self.rho * psi_d.pow(2)).mean()
        return term_t + term_d

    @torch.no_grad()
    def update_multipliers(self, tau_pred: torch.Tensor, tau_res: torch.Tensor,
                           qdot: torch.Tensor) -> None:
        """Dual ascent step on the multipliers, called once per epoch."""
        g_t = self.constraint_torque_limit(tau_pred).clamp(min=0.0).mean()
        g_d = self.constraint_dissipativity(tau_res, qdot).clamp(min=0.0).mean()
        self.lambda_torque = torch.clamp(self.lambda_torque + self.rho * g_t, min=0.0)
        self.lambda_dissip = torch.clamp(self.lambda_dissip + self.rho * g_d, min=0.0)

    def violation_report(self, tau_pred, tau_res, qdot) -> dict:
        """Diagnostics for logging."""
        with torch.no_grad():
            return {
                "max_torque_violation": self.constraint_torque_limit(tau_pred).clamp(min=0).max().item(),
                "mean_dissip_violation": self.constraint_dissipativity(tau_res, qdot).clamp(min=0).mean().item(),
                "lambda_torque": self.lambda_torque.item(),
                "lambda_dissip": self.lambda_dissip.item(),
            }


if __name__ == "__main__":
    B = 16
    al = AugmentedLagrangian(rho=1.0)
    tau_pred = torch.randn(B, 7) * 50
    tau_res = torch.randn(B, 7)
    qdot = torch.randn(B, 7)
    p = al.penalty(tau_pred, tau_res, qdot)
    al.update_multipliers(tau_pred, tau_res, qdot)
    print("AugmentedLagrangian smoke test OK — penalty =", float(p))
    print("report:", al.violation_report(tau_pred, tau_res, qdot))
