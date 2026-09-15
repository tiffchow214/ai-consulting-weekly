# Consulting Framework Reference

Static reference material for `workflows/weekly_consulting_case.md` — read
and applied every week, but not itself a run trigger. Update this file only
when the framework/curriculum/lens design itself changes, not as part of a
normal weekly run.

## Design principle: spine + lenses

This project runs on two independent layers that must not be conflated:

1. **A small, fixed core curriculum** (25 topics, one per week, never
   skipped) — general business/consulting reasoning that applies whether or
   not any technical lens is relevant that week. The core topic shapes
   *emphasis* (which questions get asked, what the challenge foregrounds,
   what the reflection focuses on) — it never bends, weakens, or
   reinterprets the real case to fit that week's topic. The case is chosen
   on its own merits (see Case Selection Criteria) first, always.
2. **A small set of Analytical Lenses** (ML Decision, Impact & Causal
   Inference, LLM/NLP Analytics, Marketplace) that activate only when the
   week's real case genuinely calls for them. Zero, one, or multiple lenses
   may activate in a given week. **A zero-lens week is a complete, valid
   outcome** — a strong process-redesign or change-management case with no
   real technical decision in it should read as a full, satisfying week on
   its own, not a lesser one.

Depth lives in the lenses; calendar cadence lives only in the core. This is
what keeps the curriculum from becoming a 70-topic list every time a new
analytical skill matters: a new *lens* gets added when a genuinely new kind
of decision-technique pairing needs teaching; a new *core topic* only gets
added when a genuinely new general consulting skill needs a guaranteed
weekly slot.

## The reasoning loop

**Mental model.** The compressed version to hold in your head:

```
Real Case → Business Problem → Business Decision → Evidence/Data →
Problem Formulation → Solution Options → Relevant Analytical Lens →
Evaluation → Architecture → Production → Experimentation/Impact →
Business Value
```

The detailed loop below is that mental model's operational elaboration — it
names the intermediate machinery (stakeholders, process, root cause,
feasibility, risk, pilot, scale/adoption) the compressed version assumes but
doesn't spell out. Use the compressed version to keep orientation; use the
detailed loop to actually do the work. The sequence a real engagement (and
every "Model Approach" section) should be checked against:

```
Problem
  ↓
Stakeholders & Objectives      — who wants what, what does success look like
                                  to them (see AI Value Discovery Framework
                                  below — User-Centred Discovery)
  ↓
Process                        — where does the work actually happen today
                                  (see AI Value Discovery Framework below —
                                  Business Process Mapping)
  ↓
Root Cause                     — why is the problem happening
  ↓
Opportunity                    — where could technology/process redesign help
                                  (see AI Value Discovery Framework below —
                                  AI Use-Case Prioritisation, once more than
                                  one candidate opportunity exists)
  ↓
Options                        — incl. non-AI, build/buy, RAG/LLM/agent, ML/DL
  ↓
Lens Selection                 — for each of the 4 lenses below, does this
                                  case's actual decision/data genuinely call
                                  for it? Zero, one, or multiple may
                                  activate. State which activated and why —
                                  or state plainly that none did.
  ↓
[Activated lens(es) run here — see Analytical Lenses below]
  ↓
Feasibility & Data Readiness   — is the data actually accessible, is this
                                  organizationally/technically doable
  ↓
Value & ROI                    — per option, before committing to one. Any
                                  claim of impact carries the standing
                                  question "how do we know this worked?" —
                                  live every week a value claim is made, not
                                  only in the week curriculum topic 17
                                  rotates up. Where the case's actual
                                  decision is a causal "did this work"
                                  question rather than a prediction, this is
                                  where the Impact & Causal Inference Lens
                                  gets checked for activation. (See AI Value
                                  Discovery Framework below — Benefits
                                  Mapping & Business Case.)
  ↓
Risk                           — per option, before committing to one (see
                                  AI Value Discovery Framework below —
                                  Responsible AI & Assurance)
  ↓
Recommendation                 — now defensible, because value/risk/
                                  feasibility were assessed first. "No
                                  AI/ML" or "no lens needed at all" is a
                                  fully valid recommendation when the
                                  reasoning supports it. Every recommendation
                                  — model choice, architecture choice,
                                  experimentation/method choice, or general
                                  consulting recommendation — answers both
                                  "why this approach?" and "why not the
                                  alternatives?"; a recommendation that only
                                  answers the first is incomplete.
  ↓
Architecture                   — what would we build/buy (see Architecture
                                  Spine below; specialized per activated lens)
  ↓
Pilot                          — how to test safely
  ↓
Scale & Adoption                — what has to happen to operationalize +
                                  change management
```

Deliberate departures from a naive "problem → recommendation → then check
value/risk" ordering:
1. **Value & Risk come before Recommendation.** A recommendation made before
   knowing its value/risk profile isn't defensible.
2. **Lens Selection is a detour, not a parallel track.** It attaches after
   Options and rejoins the main loop at Feasibility — it never replaces or
   reorders the surrounding stages, and answering "does any lens apply
   here?" happens every week regardless of the answer.

Not every case will touch every stage explicitly, and a shallow public case
study may only give enough evidence to reconstruct half of these — say so
rather than inventing the rest (see Evidence & Source Discipline below).

## Analytical Lenses

### ML Decision Lens

Activates when the case's actual decision is a prediction problem where ML
is a real candidate. Full comprehensive pipeline — nothing here is
summarized or thinned relative to how deeply it should be taught:

```
Business problem                — the decision to improve, not "build a
                                    model." ("Identify customers likely to
                                    churn early enough for the retention
                                    team to intervene," not "build a churn
                                    model.")
  ↓
ML problem formulation          — translate the business problem into a
                                    problem shape: classification, regression/
                                    forecasting, clustering, ranking/
                                    recommendation, anomaly detection,
                                    computer vision, etc.
  ↓
Data characteristics            — dataset size, target/label quality,
                                    feature types, missing values, class
                                    imbalance, outliers, temporal structure,
                                    leakage risk, data freshness,
                                    representativeness, training/production
                                    skew. Explicitly ask: what does the
                                    structure of this data imply about model
                                    choice?
  ↓
Baseline                        — always considered before complexity:
                                    majority class, a business rule, a simple
                                    regression, a naive forecast. The goal is
                                    to know whether complexity earns its
                                    keep over the baseline.
  ↓
Candidate models                — compare only problem-appropriate
                                    candidates (e.g. for tabular
                                    classification: logistic regression,
                                    random forest, gradient boosting, a
                                    small neural net) — never recommend a
                                    model because it's fashionable.
  ↓
Model selection & trade-offs    — compare candidates across predictive
                                    performance, interpretability, data
                                    requirements, training complexity,
                                    inference complexity, deployment
                                    complexity, latency, cost, scalability,
                                    business fit, regulatory constraints.
                                    Explain both "why this model" and "why
                                    not the alternatives."
  ↓
Evaluation & metric selection   — tied explicitly to the business cost of
                                    false positives/negatives (see Metric
                                    Selection below), not metric definitions
                                    in the abstract.
  ↓
Threshold / decision policy     — the operating point follows from the
                                    relative cost of errors and the
                                    business's actual intervention capacity
                                    (e.g. a retention team that can only
                                    contact 20,000 customers/day cares more
                                    about ranking quality at the top of the
                                    list than overall accuracy).
  ↓
Deployment                      — see Production ML Sub-Framework below.
  ↓
Monitoring & drift              — see Production ML Sub-Framework below.
  ↓
Retraining                      — see Production ML Sub-Framework below.
  ↓
Business impact                 — does the incremental complexity over the
                                    baseline translate into real, measured
                                    business value? If not, recommend the
                                    baseline (or no ML at all) — a fully
                                    legitimate, rewarded outcome even in a
                                    week whose core curriculum topic happens
                                    to be about AI/ML suitability.
```

This lens rejoins the main reasoning loop at **Feasibility & Data
Readiness**. Pass progression (own counter, derived per Lens Depth Tracking
below): **Pass 1 — Understand.** Each concept explained in isolation on a
clean, well-documented case. **Pass 2 — Apply.** An ambiguous case with
incomplete or conflicting evidence; given constraints (cost ceiling,
latency budget, team size), the challenge asks the reader to choose the
model, threshold, deployment pattern, monitoring approach themselves.
**Pass 3+ — Design/Defend.** A complex case with conflicting constraints,
multiple stakeholders, production failures, or regulatory constraints —
including defending a chosen architecture against a skeptical stakeholder,
or diagnosing a scenario where production performance has degraded.

#### Metric selection & the business cost of errors

The recurring lesson to teach every time this lens is used: **a model can
have excellent offline metrics and still be the wrong business solution.**
Metric choice and threshold selection follow from the relative cost of
false positives vs. false negatives, not the other way around.

Example — fraud detection: a false negative means fraud gets through; a
false positive means a legitimate transaction gets blocked. The metric and
threshold follow from which error costs more, in which direction, to whom.

Reference metrics by problem shape (teach the metric in service of the
business question it answers, never as a bare definition):

- **Classification** — accuracy, precision, recall, F1, ROC-AUC, PR-AUC,
  confusion matrix, threshold selection.
- **Regression / forecasting** — MAE, RMSE, MAPE/WAPE (where appropriate),
  R², forecast bias.
- **Ranking / recommendation** — Precision@K, Recall@K, NDCG.

Business requirements that shape metric/threshold choice: what decision is
being supported, cost of false positives, cost of false negatives, required
explainability, regulatory requirements, the user's actual workflow,
intervention capacity, acceptable latency, required improvement over
baseline, financial value per correct/incorrect prediction.

#### Production ML Sub-Framework

Part of the ML Decision Lens's Architecture stage. Uses the same Verified /
Inferred / Reference-architecture evidence labels as any other architecture
claim — reference architecture is expected far more often than verified
detail, since production ML internals are rarely public.

```
DATA SOURCES → DATA PIPELINE → FEATURE ENGINEERING
  → [FEATURE STORE / DATA LAYER — where warranted] → MODEL TRAINING
  → MODEL EVALUATION → MODEL REGISTRY → DEPLOYMENT
  → BATCH JOB or PREDICTION API → BUSINESS APPLICATION
  → HUMAN / AUTOMATED ACTION → MONITORING → RETRAINING
```

**Not every component is always needed.** Justify inclusion or exclusion
per case (e.g. "no feature store: one small nightly batch job, features
computed inline") rather than mechanically drawing every box every time.

**This is not an MLOps checklist.** For every component below, teach three
things, not a bare definition: *why it exists*, *what failure or risk it
addresses*, and *what trade-off it introduces*. A component that can't earn
that 3-part answer for a given case is a component that's honestly excluded
rather than mentioned for completeness.

Topics to cover when relevant:

- **Serving** — batch inference vs. real-time inference, and when to
  choose each (latency requirement, request volume, freshness need).
- **Deployment** — how the model is packaged and deployed (containers,
  APIs, cloud infra) at a level appropriate to the case's evidence.
- **Versioning** — model versions, training-data versions, feature
  versions where relevant.
- **Model registry** — why it exists, when it earns its complexity.
- **Monitoring** — data drift, concept drift, prediction drift, feature
  distribution shift, model performance decay, latency, errors,
  infrastructure health.
- **Retraining** — scheduled, performance-triggered, drift-triggered, or
  manual-approval retraining, and the trade-offs between them.
- **Failure handling & rollback** — model unavailable, bad input, stale
  model, pipeline failure, unexpected data, degraded performance, and how
  to safely roll back to a previous model version.
- **Human fallback** — what happens when confidence is low or the model
  cannot make a safe prediction.

**The recurring thread to close every ML-relevant week on:** model
performance is not business performance. The loop that actually creates
value is `MODEL → PREDICTION → BUSINESS SYSTEM → ACTION/HUMAN DECISION →
OUTCOME → BUSINESS VALUE`. Introduce A/B testing, control vs. treatment,
experimentation, and uplift/causal thinking only from Pass 2 onward (that
machinery lives in the Impact & Causal Inference Lens below) — not as a
Pass-1 requirement.

### Impact & Causal Inference Lens

Activates when the case's actual decision is "did this work / what caused
this," not "what will happen" (contrast with the ML Decision Lens's
prediction framing). Core curriculum topic 17 ("Experimentation & measuring
business impact") always asks *whether* something worked — this lens
supplies the rigorous *methodology* for answering that question credibly.

```
Business question                — what are we actually trying to
                                     establish?
  ↓
Prediction or causality?          — predict an outcome, or estimate an
                                     intervention's effect / establish what
                                     caused an outcome? ("which customers
                                     will churn" vs. "did the retention
                                     program reduce churn")
  ↓
Available evidence                — randomized experiment? observational
                                     data? treatment/control groups?
                                     before/after data? multiple geographic
                                     units? longitudinal data?
  ↓
Is randomisation possible?         — the first fork, asked before any
                                     method is chosen. If yes, A/B testing
                                     is the natural default — the simplest,
                                     most credible design, and the one to
                                     reach for first rather than jumping to
                                     observational methods. Only if
                                     randomisation genuinely isn't available
                                     (already rolled out, ethical/practical
                                     constraints, no control group possible)
                                     move to observational methods.
  ↓
Candidate methods                  — A/B testing (first-choice when
                                     randomisation is possible: design,
                                     sample size/power, guardrail metrics,
                                     novelty effects) — otherwise
                                     difference-in-differences, propensity
                                     methods, synthetic controls, regression
                                     adjustment, or Bayesian approaches
                                     (one candidate method among several
                                     here, not a separate lens) — compared
                                     on when each is appropriate, never
                                     taught as bare definitions.
  ↓
Assumptions                        — what must be true for the method to
                                     give a credible answer?
  ↓
Limitations                        — what could bias the result?
  ↓
Business interpretation             — what should the organization actually
                                     conclude, and how confidently?
```

Pass progression: **Pass 1 — Understand.** Recognize the prediction-vs-
causal distinction and apply A/B testing on a clean case where
randomisation was genuinely possible — the anchor method for a first
exposure to this lens, not one option among equals. **Pass 2 — Apply.**
Observational data, no randomization available (DiD/propensity),
assumption-checking required. **Pass 3+ — Design/Defend.** Defend a causal
claim's assumptions under stakeholder scrutiny, or reconcile two studies
reaching different conclusions.

### LLM/NLP Analytics Lens

Activates when the case uses an LLM/NLP component as a pipeline step (raw
text → structured data → analytics), not as a chatbot/agent front-end. The
core idea to teach: **LLMs aren't only for chatbots or agents — they can be
components inside data pipelines and analytics systems.**

```
Problem                       — what information needs to be extracted or
                                 transformed from unstructured data?
  ↓
Data                          — what does the raw unstructured input
                                 actually look like (volume, structure,
                                 noise, language)?
  ↓
Options                        — rules, traditional NLP, supervised ML,
                                 embeddings, LLM classification, LLM
                                 extraction, RAG, agentic workflow —
                                 compared, never defaulting to "LLM because
                                 there's text."
  ↓
Evaluation                    — how do we know the output is correct?
                                 (accuracy against a labeled sample, human
                                 spot-check rate, hallucination/error risk)
  ↓
Architecture                  — raw data → ingestion → preprocessing →
                                 LLM/NLP → validation → structured data →
                                 warehouse → analytics/ML → business decision
  ↓
Economics                     — cost/latency at the actual volume
                                 (per-record cost × millions of records is a
                                 real number, not an afterthought)
  ↓
Production                    — batch or real-time, retries, validation,
                                 monitoring, model/API versioning, human
                                 review, fallback
```

Pass progression: **Pass 1 — Understand.** Recognize the pattern and
choose correctly between rules/NLP/ML/LLM on a clean case. **Pass 2 —
Apply.** Design the enrichment architecture + evaluation approach for an
ambiguous case with noisier data. **Pass 3+ — Design/Defend.** Defend
cost/accuracy/hallucination trade-offs against a stakeholder pushing either
"just use an LLM for everything" or "we can't trust AI-generated data at
all."

### Marketplace Lens

Activates when the case involves two-sided supply/demand matching. Taught
as a systems-thinking discipline — reasoning about the whole marketplace
rather than optimizing one metric in isolation.

```
Supply         — who provides the product/service?
Demand         — who consumes it?
Matching       — how are supply and demand matched?
Geography      — how does supply/demand vary by location?
Pricing        — how does pricing affect both sides?
Incentives     — what incentives shape supplier behavior?
Trade-offs     — could improving one side hurt the other? (e.g. raising
                 commission may raise platform revenue but reduce supplier
                 participation)
```

Pass progression: **Pass 1 — Understand.** Map supply/demand/matching for a
clean, well-documented marketplace case. **Pass 2 — Apply.** Reason about a
two-sided trade-off with incomplete data on one side. **Pass 3+ —
Design/Defend.** Defend a pricing/incentive recommendation against a
stakeholder representing the *other* side of the marketplace.

### Future lens (not active): Optimisation

Not built out yet — documented here only so the intended shape isn't lost.
Once the ML Decision Lens is comfortable (later pass), introduce the
distinction between prediction and optimization:

```
Prediction → Optimisation → Decision → Intervention → Experiment → Business Impact
```

("ML predicts what might happen; optimisation determines what to do about
it" — e.g. demand forecast → inventory optimisation → stocking decision, or
demand prediction → pricing optimisation → price decision.) No reasoning
steps, pass progression, or lens-activation logic exist for this yet — it
is a placeholder for future design work, not a lens the weekly workflow
should attempt to activate.

## Lens depth tracking

No new sheet, no new tool. `tools/manage_sheet.py`'s Tracker tab has a
`lenses_used` column (comma-separated lens names, empty if none activated).
A lens's current depth is derived, not stored: after the required
`tracker-read` at the start of every run, count how many past rows mention
that lens in `lenses_used` — 1st-2nd occurrence = Pass 1 (Understand),
3rd-4th = Pass 2 (Apply), 5th+ = Pass 3+ (Design/Defend). This is
independent of the core curriculum's own pass counter (below) — a
frequently-relevant lens naturally reaches "Design/Defend" faster than a
rarely-relevant one, which is correct: don't drill at an advanced level on
a lens barely touched.

## Weekly challenge sourcing (real case first)

The "Your Turn" challenge is never vignette-dependent. In priority order:

1. **A real-case extension** — a new, related problem that grows naturally
   out of this week's actual case. Preferred whenever the case supports it.
2. **A related-but-new scenario** — a plausible adjacent problem in the same
   or a similar domain, when the real case itself doesn't stretch far enough
   for a satisfying challenge.
3. **A short vignette** — used only when it adds genuine learning value,
   most often to practise a lens/concept the real case doesn't touch and
   that has gone stale (see Vignette mechanism below). Never the default.

## Vignette mechanism (judgment call, not a fixed rule)

A short illustrative vignette (a paragraph, never a second case study) is
*considered*, not mechanically triggered, when a lens has gone unused for a
while. Weigh three things together: **how stale** the lens actually is
(rough sense from `lenses_used` history, not a precise countdown), **how
important** that lens is to the broader learning goal right now, and
**whether this week's real case offers any natural angle** into it at all,
even partial, before resorting to an invented scenario. Mere staleness
alone is not sufficient reason to force one in — this stays a judgment
call, weighted toward letting real cases carry the teaching whenever they
can, and toward options 1-2 above over inventing a vignette. When a
vignette does fire, it becomes the seed for that week's "Your Turn"
challenge. The real case is always analyzed on its own merits first and is
never discarded, weakened, or reinterpreted to manufacture lens relevance.

## Architecture spine

One general architecture spine, specialized per activated lens rather than
each lens teaching its own from-scratch architecture:

```
BUSINESS PROBLEM → DATA SOURCES → DATA PIPELINE → ANALYTICAL/AI LAYER
  → APPLICATION → INTEGRATION → HUMAN/AUTOMATED ACTION → BUSINESS OUTCOME
  → MONITORING
```

How each lens specializes it:
- **ML Decision Lens** → the Production ML Sub-Framework (feature
  engineering → training → evaluation → registry → deployment → inference;
  monitoring → drift/retraining).
- **LLM/NLP Analytics Lens** → ingestion → preprocessing → LLM/NLP →
  validation → structured data → warehouse.
- **Impact & Causal Inference Lens** → identification strategy → analysis
  → robustness checks → estimated impact (more analytical pipeline than
  software system, but the same spine position and evidence-labeling
  convention still applies).
- **Marketplace Lens** → doesn't specialize the Analytical/AI Layer; it's a
  decision-framing lens, not a data-pipeline lens — it plugs into
  "Business Outcome" (both-sides trade-off framing) instead.

Same Verified / Inferred / Reference-architecture evidence labels apply
throughout, regardless of lens.

## Cross-cutting: Evidence & Source Discipline

Considered whenever a case makes it material — independent of which
curriculum topic is rotating up and independent of whether any Analytical
Lens is active. Not a lens, not gated behind lens activation, and
newsletter-primary (see workflows/weekly_consulting_case.md): every
material claim, every week; see the Evidence & Source Discipline section
below.

## Engineering Dimensions (deck-primary — the recurring systems-engineering curriculum)

Where Evidence & Source Discipline is newsletter-primary, these 13
dimensions are the deck's recurring engineering-judgment curriculum — see
`workflows/weekly_consulting_case.md`'s **Dimension Selection** step for how
materiality is assessed and translated into deck slides each week. None of
these are lenses; a lens (if active) supplies technology-specific detail
that feeds into the relevant dimension below rather than replacing it.
**Architecture** and **Technical Evaluation** are near-always material —
every real system has one and some way to know if it's working. The other
11 are genuinely selective: assessed every week, but typically only 2-4
earn real slide depth in any given week; the rest get at most a one-line
mention or are silently not material, exactly like an inactive lens.

1. **Architecture & data flow** — the general spine above, whether or not a
   lens specializes it that week. Teaches architectural *reasoning*, not
   just component drawing — for the case's key architectural decision(s),
   explicitly answer: why this architecture? why not the alternatives? what
   trade-off does the choice introduce? what happens at 10x scale? what
   happens when a dependency fails? how is it operated and maintained?
2. **Data quality / readiness** — completeness, freshness, label/ground-
   truth quality, representativeness, and what breaks downstream if input
   data quietly degrades.
3. **Performance & latency** — throughput, response time, batch vs.
   real-time trade-offs.
4. **Reliability** — *whether the system consistently performs its intended
   function* (uptime, correctness under load, graceful degradation).
5. **Observability** — *whether engineers can understand what the system is
   doing and diagnose failures in production* (logging, tracing, metrics,
   alerting). Kept explicitly distinct from Reliability — a system can be
   reliable and unobservable (works, but nobody would know if it stopped),
   or observable and unreliable (fails constantly, but the failures are
   easy to see) — never conflate the two.
6. **Security** — treated explicitly whenever material, drawing from
   whichever of these actually apply to the case's architecture: access
   control, data leakage, prompt injection (LLM/agent systems), unsafe tool
   use, PII handling, least privilege.
7. **Scalability** — what changes *structurally* at 10x volume (not just
   "does it get slower" — does the architecture itself need to change).
8. **Maintainability** — ownership, versioning, testing, documentation,
   coupling, vendor lock-in, and explicitly: what happens after the
   consultancy leaves — who operates this system a year from now?
9. **Cost / unit economics** — unit cost, volume, operating cost.
10. **Business impact / value** — expected benefit and whether the
    engineering complexity is actually justified by it. Usually assessed
    together with Cost as one slide when either is material — the real
    question is "is this complexity worth it," not two separate numbers.
11. **Failure modes** — what fails, how it's detected, what the blast
    radius is.
12. **Human oversight** — where a human is in the loop, and what happens
    when the system can't safely decide alone.
13. **Technical evaluation** — near-always material, technology-specific:
    - *ML* → the ML Decision Lens's own Metric Selection framework above
      (cross-referenced, not duplicated here): classification/regression/
      ranking metrics tied to business error cost, threshold policy.
    - *LLM/NLP* → task accuracy, hallucination/groundedness, human
      evaluation rate.
    - *RAG* — not a named lens, but a real technology pattern worth its own
      evaluation split: retrieval quality (precision@k/recall@k over the
      retrieved context) evaluated separately from generation quality
      (faithfulness/groundedness to that retrieved context).
    - *Agentic systems* — task-completion rate, tool-use correctness, and
      trajectory evaluation (did it take a reasonable path, not just reach
      a reasonable answer).
    - *Process / data systems* — conformance/fitness checking, event-log
      completeness, data-quality gates (covers cases like process mining
      that activate no lens at all but still have a real system to
      evaluate).
    - **Always distinguish technical system performance from downstream
      business impact** — the same discipline the ML Decision Lens already
      closes on ("model performance is not business performance"),
      generalized here to every technology type, every week, lens-active or
      not.

## Statistical reasoning (foundational, not a lens)

Underpins ML evaluation, experimentation, causal inference, and business
analysis alike. Not a lens and not a dedicated curriculum slot — it
surfaces inside whichever lens or topic needs it that week. Concepts:
sampling, uncertainty, confidence intervals, hypothesis testing,
statistical vs. practical significance, regression, correlation vs.
causation, and Bayesian reasoning. Teach each concept in service of the
decision it supports (same discipline as Metric Selection above), never as
a bare statistical definition.

## AI Value Discovery Framework (cross-cutting, tiered)

The upstream discovery-and-justification methodology that Phase 1 (topics
1-6) and part of Phase 3 (topics 13-15, 19) of the Core curriculum below
draw from. Not a lens — nothing here activates/deactivates, and it isn't
gated behind a selection step like Lens Selection or Dimension Selection.
Three tiers, each with its own weekly application discipline:

- **Essential** (Business Process Mapping, User-Centred Discovery, Benefits
  Mapping & Business Case) — considered on every case, same "whenever the
  case makes it material" discipline as Evidence & Source Discipline. These
  underpin the newsletter's "Behind the Engagement" process/problem
  reconstruction and any value/ROI claim, regardless of which curriculum
  topic is rotating up that week.
- **AI-specific** (AI Use-Case Prioritisation) — material whenever the case
  involved choosing among multiple candidate opportunities rather than
  executing a single predetermined one; it's curriculum topic 15's
  (Prioritisation & feasibility) deep-dive.
- **Government-specific** (Responsible AI & Assurance) — the named
  frameworks below are UK public-sector references. Apply their underlying
  questions (data sensitivity, fairness, explainability, oversight,
  accountability) to any case where the AI system affects decisions about
  individuals; cite the named frameworks directly when the case itself is
  UK public sector. It's curriculum topic 19's (Risk, privacy & security)
  deep-dive.

Any named framework/technique below that becomes newsletter-visible (cited
in a Further Reading link, or given its own Key Terms slide entry) follows
the same discipline as every other external link in this project: WebSearch
for the current official URL at the time of the actual run — never guess or
reuse a stale one (see the Terminology step and Further Reading section in
`workflows/weekly_consulting_case.md`).

### 1. Business Process Mapping — Essential

Purpose: understand how work is actually done before proposing improvements.
Attaches to the reasoning loop's **Process** stage and curriculum topic 4
(Process mapping).

Techniques: SIPOC, BPMN (Business Process Model and Notation), value stream
mapping, service blueprints — use these to identify activities, handoffs,
bottlenecks, rework, manual data entry, and unnecessary steps.

Learn: BPMN — Business Process Model and Notation.

### 2. User-Centred Discovery — Essential

Purpose: understand what users actually need, rather than assuming the
process owner already knows every problem. Attaches to the reasoning loop's
**Stakeholders & Objectives** stage and curriculum topic 3 (Discovery
questions).

Techniques: stakeholder interviews, observation, journey mapping, service
design, user research — especially load-bearing in government cases, where
services must meet real user needs.

Learn: GOV.UK Service Manual.

### 3. Benefits Mapping & Business Case — Essential

Purpose: connect a proposed change to measurable benefits and justify the
investment. Attaches to the reasoning loop's **Value & ROI** stage and
curriculum topics 13-14 (Value creation; ROI & cost modelling) — and
directly sharpens the existing ROI/savings evidence checklist (Evidence &
Source Discipline above): what was the baseline, over what period, does it
translate into actual financial value.

Techniques: benefits maps, benefits dependency networks, cost-benefit
analysis, and (UK public sector) the HM Treasury Green Book appraisal
approach. Explicitly distinguish operational benefit from cash benefit — a
reduction in review time may free organizational capacity without being an
automatic cash saving; say so rather than treating the two as equivalent.

Learn: Digital and Data Benefits Framework; HM Treasury Green Book.

### 4. AI Use-Case Prioritisation — AI-specific

Purpose: decide which opportunities are worth investigating first, once more
than one candidate exists. Attaches to the reasoning loop's
**Opportunity**/**Options** stages and is curriculum topic 15's
(Prioritisation & feasibility) deep-dive.

Technique: score each candidate opportunity against business impact,
feasibility, risk, implementation effort, and strategic alignment (the
BridgeAI AI Use Case Framework publishes one version of this scoring
approach) — the same discipline the Case Selection Criteria below apply to
choosing *this newsletter's* case, applied instead to a client's internal
portfolio of AI opportunities.

Learn: Innovate UK / BridgeAI — AI Use Case Framework.

### 5. Responsible AI & Assurance — Government-specific

Purpose: assess whether an AI opportunity is safe, lawful, appropriate, and
capable of being trusted. Attaches to the reasoning loop's **Risk** stage,
Engineering Dimensions 6 (Security) and 12 (Human oversight), and is
curriculum topic 19's (Risk, privacy & security) deep-dive.

Considerations: data sensitivity, fairness, explainability, human oversight,
security, evaluation, accountability.

Learn: Data and AI Ethics Framework; Ethics, Transparency and Accountability
Framework for Automated Decision-Making. Apply their underlying questions to
any case touching automated decisions about individuals; cite them directly
when the case itself is UK public sector.

## Core curriculum (25 topics, 4 phases)

One topic per week, fixed order, never skipped — a learning *spine*, not a
weekly content template (see Design Principle above). Tracked via
`tools/manage_sheet.py`'s `curriculum_topic` + `pass` tracker columns.

**Phase 1 — Business problem understanding**
1. Evidence & source discipline
2. Problem framing
3. Discovery questions — see AI Value Discovery Framework above,
   User-Centred Discovery (stakeholder interviews, observation, journey
   mapping, service design, user research)
4. Process mapping — see AI Value Discovery Framework above, Business
   Process Mapping (SIPOC, BPMN, value stream mapping, service blueprints)
5. Root-cause analysis
6. Opportunity identification

**Phase 2 — Solution selection meta-skill** (deciding *whether and which
category* of technical intervention is warranted — not the mechanics of
any one lens, which live in Analytical Lenses above)
7. Automation vs AI vs ML
8. AI/ML suitability
9. Solution options (incl. non-technical: process redesign, existing
   SaaS, no change)
10. Build vs buy
11. RAG vs LLM vs agent
12. Solution architecture (the general spine above)

**Phase 3 — Business value & implementation**
13. Value creation — see AI Value Discovery Framework above, Benefits
    Mapping & Business Case (benefits maps, benefits dependency networks)
14. ROI & cost modelling — see AI Value Discovery Framework above, Benefits
    Mapping & Business Case (cost-benefit analysis, HM Treasury Green Book)
15. Prioritisation & feasibility — see AI Value Discovery Framework above,
    AI Use-Case Prioritisation (impact/feasibility/risk/effort/strategic-fit
    scoring, e.g. the BridgeAI AI Use Case Framework)
16. Pilot design
17. Experimentation & measuring business impact — this week's dedicated
    deep-dive slot, but the underlying question "how do we know it worked?"
    is a standing cross-cutting question asked every week a value claim is
    made (see Cross-cutting dimensions above), not confined to this
    rotation; the rigorous methodology lives in the Impact & Causal
    Inference Lens (A/B testing first when randomisation is possible, then
    observational methods when it isn't)
18. Human-in-the-loop
19. Risk, privacy & security — this week's dedicated deep-dive slot, but
    also a standing cross-cutting dimension evaluated whenever a case makes
    it material (see Cross-cutting dimensions above); see AI Value Discovery
    Framework above, Responsible AI & Assurance for the named UK
    public-sector reference frameworks
20. Change management

**Phase 4 — Consulting communication**
21. Making recommendations
22. Executive communication
23. Handling objections
24. Defending recommendations
25. Executive case presentation

**Determining this week's topic and pass:**
- If the tracker has no rows yet: topic = #1 (Evidence & source discipline),
  pass = 1.
- Otherwise, find the most recent row's `curriculum_topic` in the list
  above.
  - If it isn't #25 (Executive case presentation): this week's topic is the
    next one in the list, same pass number.
  - If it is #25: this week's topic is #1 again, pass = previous pass + 1.

**Pass progression** (spaced repetition — assume the reader already has the
prior pass's basics): **Pass 1 — Understand** the concept on a clean,
well-documented case. **Pass 2 — Apply** the concept to an ambiguous case
with incomplete or conflicting evidence. **Pass 3+ — Design/Defend** the
concept on a complex case with conflicting constraints, multiple
stakeholders, competing priorities, and no single clean answer.

If the tracker is unreadable, default to topic #1, pass 1, and add a
footer line to the newsletter noting sequence tracking failed this run —
don't skip the send.

## Evidence & source discipline — uniform across every lens

Every material claim in the newsletter and deck gets exactly one label,
**regardless of which lens (if any) produced it:**

| Label | Meaning |
|---|---|
| **VERIFIED FACT** | Explicitly supported by a reliable primary source. |
| **CLIENT-REPORTED RESULT** | The client states it. |
| **CONSULTANCY-REPORTED CLAIM** | The consultancy states it — marketing material by default; treat with skepticism. |
| **INFERENCE** | A reasonable conclusion from available evidence, explicitly labeled as such. |
| **UNKNOWN** | The source material does not establish this — say so directly rather than filling the gap. |

The same 3-way Verified / Inferred / Reference-architecture distinction
applies to architecture claims from any lens (see Architecture Spine
above):

- **Verified** — the vendor/consultancy/client explicitly documents this
  component.
- **Inferred** — not publicly documented, but the documented workflow
  strongly implies it.
- **Reference architecture** — a typical design for a comparable production
  system; not claimed to be this case's actual proprietary implementation.

**Any productivity/ROI/savings/adoption claim** must be run through this
checklist before it's allowed into the newsletter at all: What was the
baseline? What exactly does the metric mean? How was it measured? Over
what period? Was there a control group? Were other process changes
introduced at the same time? Is the figure client-reported or
consultancy-reported? Is it independently verified anywhere? Does it
translate into actual, quantifiable financial value?

**Any model-performance claim** ("the model achieved 92% accuracy," ML
Decision Lens) additionally needs: What was the evaluation set — held-out,
cross-validated, or (worse) the training set? Was the split random or
time-based (a random split on temporal data leaks future information)? Is
this offline evaluation or live production performance? Was there a
champion/challenger comparison, or just a single reported number? What was
the class balance / baseline performance for comparison? Is the sample
size large enough for the figure to be meaningful?

**Any causal/impact claim** (Impact & Causal Inference Lens) needs: Is the
reported effect from a randomized experiment (closer to verified,
conditional on power/guardrails holding) or an observational method
(inference, conditional on the method's stated assumptions holding)? Was
the effect size client-reported, consultancy-reported, or independently
replicated? What would have to be true for the estimate to be biased?

**Any extraction/classification-accuracy claim** (LLM/NLP Analytics Lens)
needs: Is this verified against a labeled holdout set, or an unverified
vendor/consultancy claim about "high accuracy" with no holdout described?

**Any two-sided trade-off claim** (Marketplace Lens, e.g. "raising
commission increased revenue without hurting supply") needs: Is the
supply-side effect actually measured, or assumed/inferred from a
demand-side metric alone?

If the answer to most of a checklist is "unknown," the newsletter says so
explicitly (e.g. "The public case study does not establish a baseline for
this figure") rather than smoothing over the gap. Never invent: ROI,
savings, adoption numbers, architecture details, model performance
figures, causal effects, or extraction accuracy — for any lens, without
exception.

## Case selection criteria

Score every candidate case against these before committing (checked against
the tracker for duplicate `client_or_case` first):

- **Strong problem** — a meaningful business/operational problem.
- **Clear intervention** — we can understand what the consultancy actually
  did.
- **Technology relevance** — the case involves interesting data/AI/technology.
- **Business relevance** — a clear connection between technology and
  business outcomes.
- **Architecture value** — we can understand or reasonably infer the
  technical solution.
- **Critical-thinking value** — there are assumptions, trade-offs, missing
  information, or decisions worth questioning.
- **Transferability** — the lessons apply to other companies/industries.

When multiple candidate cases score equally well on the criteria above,
mild preference for travel, e-commerce, marketplace, retail, or
consumer-platform domains — this never overrides case quality, and a
weaker case is never chosen for domain fit. This preference exists purely
to occasionally surface cases the Marketplace Lens can activate on; it
creates no dedicated curriculum topics and no other domain-specific lenses.

Reject cases that amount to "we partnered with Company X to unlock AI
transformation" with no substantive detail — prefer a well-documented 2024
case over a thin 2026 one. Never pick a *weaker* case just because it
happens to match this week's curriculum topic or a lens more neatly — the
real case is chosen on its own merits (this list, plus the domain
tie-breaker) independent of the week's topic; see
`workflows/weekly_consulting_case.md`'s Edge Cases for how a topic/case or
lens/case mismatch is handled instead (never by weakening case selection).
