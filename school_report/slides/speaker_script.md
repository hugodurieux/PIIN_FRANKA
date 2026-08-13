# Speaker script — 15 minutes, 15 slides

Written to be **spoken, not read**. Roughly 135 words per minute; each block is
timed to its slide. Numbers are written the way you say them out loud.

Two habits worth keeping: pause after every number you want remembered, and
never read a bullet that is already on the screen — say the sentence the bullet
is a shorthand for.

---

## Slide 1 — Title · 0:00 – 0:20

Good morning. I'm Hugo Durieux, and this is the work I did during my Master's
research internship at the University of Melbourne.

In one sentence: the input to this project is a robot description file, and the
output is a robot you can actually control, in real time. Everything
interesting happens in the dynamics model in between.

---

## Slide 2 — A model that is exact, and still wrong · 0:20 – 1:20

To control a robot arm at the torque level, you need to know its dynamics — the
mapping from a joint trajectory you want, to the motor torques that produce it.

The good news is that this relation has a closed analytical form, and it's
completely determined once you know the geometry and the inertias. Both of
those are in the URDF file. So you get the model for free, and you get it
exactly.

The bad news is that on a real robot, that model is wrong. Not noisy — wrong.
It knows nothing about friction in the harmonic drives, nothing about
compliance in the transmissions, nothing about backlash, wear, or the payload
the robot happens to be carrying.

On a Franka Panda that gap is several newton-metres, and there is no reliable
analytical form for it. **That gap is the whole subject of this work.** I am
not trying to replace physics. I am trying to complete it.

---

## Slide 3 — Objective, and why it is not just engineering · 1:20 – 2:20

The objective is to build an automatic pipeline: description file in,
controlled robot out, with a learned dynamics model queried at every control
period.

Stated like that, it sounds like plumbing. Three things make it not plumbing.

First, generality costs accuracy. The literature gets its best numbers by
deriving one robot's equations by hand and fitting a network on top. Doing it
automatically from a URDF means giving all of that up.

Second, physical guarantees survive learning badly. A freely learned term can
inject energy into the system — which is absurd for something meant to
represent friction — and it can predict torques the motors cannot deliver. And
I have to hold that on seven joints at once, whose torque limits differ by a
factor of seven: eighty-seven newton-metres on the big joints, twelve on the
wrist.

Third, being accurate offline is not the same as controlling anything. A
thousand hertz means sub-millisecond inference, and a control law whose error
you can bound.

I should say plainly what this is not: there is no new learning theory here,
and no hardware. Training is in Isaac Sim, deployment is in MuJoCo.

---

## Slide 4 — What the URDF gives for free · 2:20 – 3:10

This is the standard rigid-body model — inertia, Coriolis, gravity — with n
equal to seven for the Panda.

I evaluate it with the recursive Newton–Euler algorithm, through Pinocchio,
directly from the URDF. No hand derivation anywhere.

The one point I want to land here: this term is **evaluated, not fitted**.
Nothing in the training loop can modify it. That is what makes the guarantees
later in the talk mean something, and it's also what makes the pipeline
automatic — hand it a different URDF and it just works.

---

## Slide 5 — Computed, plus learned · 3:10 – 4:10

So the model is a sum of two terms.

*(point at the first brace)* This one is computed, from the URDF, exactly as on
the previous slide.

*(point at the second)* And this one is learned. It only ever has to represent
dissipation and modelling error — it never has to learn gravity or inertia,
because those are already correct.

The residual is conditioned on the carried payload, delta. Only the residual,
not the whole model — and that's a deliberate choice, following Hu and
colleagues, who show that backlash error depends on position and velocity but
not on the carried mass.

One detail that matters more than it looks: **the residual does not take the
acceleration as input.** Acceleration is available offline, when I'm training,
but it is not available inside a thousand-hertz loop that measures only
position and velocity. So excluding it is a deployment requirement, not a
modelling preference. It comes back later — it's also why one of my results is
suspicious.

---

## Slide 6 — Three degrees of guarantee · 4:10 – 5:10

Here is the problem I actually solve. Minimise the prediction error, subject to
two constraints.

The first says: never predict a torque the actuators cannot produce. The second
says the residual must be dissipative — it must never inject mechanical energy.
That second one is just the formal way of writing "this term represents
friction".

I handle those constraints at three increasing degrees of strictness, and this
ladder is the structure of the whole method.

Degree zero is a free residual — smooth, payload-conditioned. I use Mish
activation, never ReLU, because I need a continuous derivative: a discontinuous
one becomes a torque jerk in the motors.

Degree one imposes the constraints through an augmented Lagrangian with dual
ascent. The multipliers get optimised, so I reach constraint satisfaction
without driving the penalty weight to infinity and wrecking the conditioning.

Degree two is structural — guaranteed by construction. That's two slides away.

---

## Slide 7 — Architecture and gradient flow · 5:10 – 6:10

Let me walk this once, left to right.

Top path: the URDF goes into RNEA, which produces the analytical torque. Grey
background means computed — nothing is learned along that path.

Bottom path: the measured state and the payload get encoded — sines and cosines
of the joint angles, the velocities, and delta — and that feeds two networks
with thick outlines, which are the only trained things in the picture.

They meet at the sum, and that gives the predicted torque.

Along the bottom are the three loss terms: the data term, the torque-limit
term, and the dissipativity term. And the dashed line is the gradient.

The thing to notice is where the gradient goes. It reaches the two trained
networks, and **nowhere else**. RNEA is never updated.

---

## Slide 8 — Degree 2: dissipativity by construction · 6:10 – 7:00

This is the structural guarantee.

The friction module doesn't output a torque directly. It outputs a diagonal
damping matrix, built from a Softplus plus a small epsilon — so every diagonal
entry is strictly positive. The torque is then minus that matrix times the
velocity.

Which means the dissipativity condition holds for every possible input, by
algebra. It does not depend on the data, and it does not depend on the
optimiser converging.

One honest caveat: the guarantee is on the *sign*, not the magnitude. If the
network learned a strongly negative weight tied to a large payload, the
friction could be driven towards zero. It would still be dissipative. It just
wouldn't be useful.

Remember this slide — in five minutes I'm going to show you that this module
buys almost no accuracy, and I want you to already know that accuracy was never
what it was for.

---

## Slide 9 — From model to torque, at 1 kHz · 7:00 – 8:00

The control law is computed torque plus a PD term. The model supplies the
feedforward, and the PD handles what's left.

The gains come from Liu and colleagues' stability template: the derivative gain
is proportional to an error bound epsilon-j, and the proportional gain is that
squared over four.

The important thing is that **epsilon-j is measured, not tuned**. It's the
99.9th percentile of my model's error on the held-out test set. So a better
model gives a smaller bound, gives lower gains, gives a softer and safer arm.
The learning result feeds the control design directly.

Now, there's a consequence of that template which I think is worth stating,
because it's counter-intuitive. The proportional gain comes from the error
bound. So a joint that is modelled *better* gets a *lower* gain. And the
steady-state error under a constant residual torque is torque over K-p. So the
best-learned joints track the worst.

I measured exactly that on joint five. It is a limitation of the template I
borrowed, not a bug in my implementation.

---

## Slide 10 — Experimental design · 8:00 – 9:00

Data: thirty continuous five-second trajectories in Isaac Sim, Fourier
excitation around Sobol centres, three payload values, sampled at a kilohertz.
About a hundred and fifty thousand samples.

Samples the simulator clipped are filtered out. A saturated sample tells you
about the actuator's limit, not about the torque the motion needed — keeping it
would train the residual to reproduce clipping.

Then an eighty-ten-ten split, shared by training, by the baseline evaluation,
and by the computation of epsilon-j, so every comparison is on identical
samples.

Three models, same test set, same capacity, same two hundred epochs: RNEA
alone; a direct MLP with the same input and capacity but no analytical term;
and the grey box.

And there's one thing I have to say here rather than bury it. **Until the 31st
of July, this project had no test set at all.** The RMSE being reported was the
validation error — measured on the very set the checkpoint was selected on. And
epsilon-j, which sets the gains the arm physically runs with, was derived from
it too. Everything I'm about to show you is the first set of numbers in this
project measured outside the selection criterion.

---

## Slide 11 — Prediction error against the baselines · 9:00 – 10:15

Here are the three models on fourteen thousand eight hundred held-out samples.

RNEA alone: one point four six newton-metres mean error, and it exceeds the
torque limit on a hundred and forty-seven samples — about one percent.

The grey box: nought point six two. So it **cuts the analytical model's error
by a factor of two point three**, and it holds zero torque-limit violations
where the analytical model violates on one percent. That's the result I set out
to get.

And then there's this row. *(point at the MLP row)* The black box — same
capacity, same input, same budget, no physics at all — gets nought point four
four seven. It is **twenty-eight percent more accurate than my grey box.**

That contradicts my starting hypothesis. I'm reporting it as a result rather
than hiding it, for two reasons. The first is on the next slide: that
twenty-eight percent is an upper bound, and I can show you why. The second is
the last column — the black box offers no dissipativity guarantee, and that
column is ultimately the argument for the whole approach.

---

## Slide 12 — A caveat on the partition · 10:15 – 11:30

So here's the methodological problem with that comparison.

My data are thirty continuous trajectories sampled at a kilohertz. But the
split is drawn **per sample**. Which means two consecutive time steps, one
millisecond apart on the same trajectory, can land on opposite sides of the
split. Every test point has an almost identical neighbour sitting in training.

Now — the selection defect I mentioned earlier is genuinely fixed. Sample
independence is not. And the reason that matters is that the leakage does not
help all three models equally. It helps most the model that has to memorise
most.

The analytical baseline isn't fitted to anything, so it gains nothing. The grey
box only has a residual to learn — inertia and gravity are handed to it. The
black box has to reconstruct everything from data. It is the one that benefits.

And there's a clue that makes this concrete. The black box never receives the
acceleration as input. So it is **structurally incapable** of representing the
inertial torque — the dominant term in the dynamics. And it wins anyway. With
only thirty trajectories, the position and velocity pair almost always
identifies which trajectory you're on and where in it, which makes acceleration
implicitly recoverable by memorising.

So I read that twenty-eight percent as an upper bound on the black box's
advantage, not as an established result. The correct measurement is a
group-wise split, by trajectory. It's implemented in the repository, but it
rests on too few test trajectories to report responsibly, so I've left it out.

---

## Slide 13 — The residual degrades what RNEA gets right · 11:30 – 12:45

Now the per-joint breakdown, which is where the more interesting failure is.

Look at joint seven. RNEA alone reaches nought point zero four two
newton-metres — that's a third of a percent of its limit. It's a wrist roll,
the axis passes through the flange, gravity barely acts on it. There is
essentially nothing to learn.

And my residual makes it **six point nine times worse**.

The worst samples show the mechanism outright. The true torque is minus nought
point zero one. RNEA predicts minus nought point zero eight — already
essentially correct. And the network adds minus two point zero four.

The learned damping coefficient for joint seven converges to nought point six
seven, the largest of all seven joints, while joint one's collapses to nought
point zero one nine. So the dissipative module is most active exactly where
there is no friction to model.

The cause is that the loss is unweighted and aggregates over joints. A joint
contributing almost nothing to the total gets almost no gradient pressure to
stay at zero. The fix is a diagonal weighting by the inverse squared torque
limits, and that's named as future work.

And while we're here — the two ablations, same protocol. The sine-cosine
encoding buys one point one percent. FrictionNet buys one point four percent.
Neither is justified by accuracy, which is exactly what I said on slide eight.

---

## Slide 14 — Closed loop: the cost of cross-simulator transfer · 12:45 – 13:50

This is the experiment I find most informative, and it's in closed loop.

Identical configuration, identical planned trajectory, identical gain margin.
The only thing I change is whether the learned residual is switched on.

With it on, joint five carries a steady-state bias of about minus nought point
zero three four radians, and the flange error is fourteen millimetres. With it
off — minus nought point zero zero one five radians, and seven and a half
millimetres.

**Turning off my learned model makes the robot track twenty-two times better on
that joint, and halves the Cartesian error.**

Here's what that does and doesn't establish. This checkpoint was trained on
Isaac Sim data and deployed in MuJoCo. So it learned the gap between RNEA and
*Isaac's* dynamics, and it's adding that gap to an engine that doesn't have it.
It is being evaluated out of distribution.

So the defensible claim is: the Isaac-trained residual degrades tracking under
cross-simulator transfer. The claim I am *not* making is that the grey-box
approach fails.

And I checked the obvious confounder — the gain margin is held constant across
both conditions, and in any case a lower gain would push the steady-state error
the other way.

Notice this is the same phenomenon as the previous slide, measured a completely
different way. Offline, the residual degrades joint seven by seven times. In
closed loop, removing it improves joint five by twenty-two times. Two
independent measurements, one cause.

---

## Slide 15 — What the grey structure is actually for · 13:50 – 15:00

So, to close.

The pipeline works: a URDF file goes in, a payload-conditioned dynamics model
comes out, and it drives a real thousand-hertz control loop with torque limits
and dissipativity guaranteed rather than hoped for.

But I want to be straight about the argument. **The case for the grey box is
not accuracy.** On this data a black box beats it, and even with the caveat
about the partition, I can't claim a precision win.

The case is what the black box cannot offer. Guarantees that hold by
construction rather than by penalty. And an automatic pipeline that never has
to relearn the inertia and the gravity the description file already contains
exactly. That's the claim I'll defend, and it's the one the report makes.

Three things next, in order of scientific value. Run the frozen-backbone
fine-tuning on MuJoCo data and replay that last ablation — that's a direct test
of whether the transfer cost can be closed. Then the group-wise split, to
settle the twenty-eight percent properly. Then exercise the payload
conditioning by actually varying the mass of the grasped object, which is the
most specific claim in this work and the one that's least tested.

Thank you. I'm happy to take questions.

---

# Appendix — likely questions

**"Why didn't you use the real robot?"**
No hardware access during the internship. Everything is Isaac Sim for training
and MuJoCo for deployment. That's also precisely why the transfer experiment on
slide 14 exists — it's the closest proxy I had for a sim-to-real gap.

**"If the black box wins, why the grey box at all?"**
Slide 15. Two reasons: the guarantee column, and the automation. Also note the
black box cannot represent the inertial torque at all, so its win is
partly a measurement artefact — slide 12.

**"How exactly was the split made?"**
Eighty-ten-ten, deterministic, drawn per sample, shared by training, evaluation
and the error bound. Its weakness is slide 12, and I'd rather raise that
myself.

**"What did the group-wise split actually show?"**
Directionally, the black box collapses, which is what the argument on slide 12
predicts. But it rests on three test trajectories per seed, so I'm not
reporting a number from it.

**"So joint 7 is just broken?"**
It's not broken, it's unregularised. Nothing in the loss tells the residual to
stay at zero where the analytical term is already right. The diag(1/τ̄²)
weighting is the partial fix; an explicit per-joint penalty on the residual
norm, calibrated against RNEA's own error, would be the direct one.

**"Is dissipativity really guaranteed, or just penalised?"**
Both, at different degrees. The torque-limit constraint is a penalty — degree
one. The friction module's dissipativity is algebraic — degree two — and holds
for every input regardless of training.

**"Did you measure the inference latency?"**
No. The loop runs at a kilohertz with no observed overrun, but I never put it
on a dedicated bench, and I say so in the limitations.
