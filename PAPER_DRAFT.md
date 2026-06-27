# From URDF to Real-Time Control: An Automated Physics-Informed Neural Network Pipeline for 7-DoF Robot Dynamics Learning

**Hugo Durieux** — Master's Internship, 2026

_Working draft — updated automatically at the end of each session._
_Last updated: 2026-06-27_

---

## Section 2: Related Work

Our grey-box architecture (RNEA white-box + neural torque residual) aligns with recent independent findings. Li et al. (2025) demonstrate the same decomposition on compliant manipulators via their DeLaN-FFNN architecture, validating the grey-box principle across rigid and compliant domains. Toscano et al. (2025) provide a comprehensive survey corroborating our design choices: grey-box architectures, augmented Lagrangian constraint enforcement, and frozen-backbone fine-tuning as cutting-edge practices in physics-informed machine learning for robotics.

---

## References

[1] Liu, X. et al. (2024). Physics-Informed Neural Networks to Model and Control Robots. _IEEE Transactions on Robotics_.

[2] Duong, H. et al. (2024). Port-Hamiltonian Neural ODE Networks on Lie Groups. _Proceedings of ICLR 2024_.

[3] Wang, Y. et al. (2024). Trajectory Control of Multi-Axis Robotic Arms. _IEEE Control and Automation Conference_.

[4] Li, X. et al. (2025). Physics-informed neural networks for compliant robotic manipulators dynamic modeling. _arXiv preprint_.

[5] Toscano, R. et al. (2025). From PINNs to PIKANs: recent advances in physics-informed machine learning. _Survey_.

[6] Prabhakar, A. et al. (2026). When Does Physics Help? Negative Results on Physics-Informed Neural Networks for Temporal Extrapolation. _Proceedings of ICLR 2026_.

[7] Djeumou, F. et al. (2022). Neural Networks with Physics-Informed Architectures and Constraints for System Identification. _ICLR 2023 Workshop on AI for Science_.

---

_Note: Full PAPER_DRAFT.md sections (Method, Experiments, Appendix A) to be populated upon Stage 1 GPU training completion._
