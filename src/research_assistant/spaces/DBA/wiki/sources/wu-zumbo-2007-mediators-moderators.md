---
type: source
title: "Understanding and Using Mediators and Moderators"
maturity: seed
tags: [mediation, moderation, causal-design, sem, moderated-mediation, mediated-moderation, research-methods]
schema_version: "1.0"
created: 2026-06-18
last_updated: 2026-06-18
originating_space: DBA
applicable_to: [thesis, research_paper, quantitative_study, mixed_methods]
draws_from: []
authors: ["Wu, A.D.", "Zumbo, B.D."]
year: 2007
journal: "Social Indicators Research"
volume: "87"
pages: "367-392"
doi: "[PENDING CrossRef lookup]"
source_path: "src/research_assistant/spaces/DBA/knowledge/Marketing & Commerce in Intnl Context/Understanding and Using Mediators and Moderators.pdf"
source_origin: knowledge_directory
ingested: 2026-06-18
related:
  - data/wiki/shared/methods/baron-kenny-moderation-mediation.md
---

# Understanding and Using Mediators and Moderators (Wu & Zumbo 2007)

## Core Argument

Wu and Zumbo argue that mediation and moderation are causal models requiring an integrated research design rather than the "data analyses driven approach often seen in the literature" [source_path, p.1]. Their central contention is that "empirical investigation of mediators and moderators requires an integrated research plan from articulating the theoretical rationale, choosing a research design, analyzing the data, to drawing conclusions" [source_path, p.1]. The paper positions mediation and moderation as "researchers' hypotheses about how a cause leads to an effect," not mere statistical techniques [source_path, p.1].

## Key Arguments

### 1. Mediation and Moderation as Causal Models

The authors state that "mediation and moderation models are, by nature, causal models because the underlying theories suggest directional inferences that are intrinsically causal" [source_path, p.2]. Even when data does not permit causal conclusions (e.g., cross-sectional data), the underlying theory is causal [source_path, p.2].

Three types of causal hypotheses (per Wegener and Fabrigar 2000): direct causal effect, mediated causal effect, and moderated causal effect [source_path, p.2].

### 2. Four Levels of Design Control

The paper identifies a hierarchy of design control relevant to establishing causation [source_path, pp.5-6]:

1. **Observation**: The independent variable is simply observed or measured (typically a stable trait/attribute)
2. **Precedence**: Observation of IV precedes observation of DV in time
3. **Manipulation**: Each level of IV is assigned to different groups of participants
4. **Randomization**: Participants are randomly assigned to each level of the IV

These levels are hierarchical: "if a higher level of control is gained, a lower level of control is certainly gained" [source_path, p.6]. Most methodologists agree that level one alone is not eligible for causal inference (at best correlational), while level four is legitimate for causal inference [source_path, p.6].

### 3. Three Frameworks for Mediation

**a) The Kenny Approach (Baron & Kenny 1986)**

The classic four-step method: (1) show X predicts Y (effect c), (2) show X predicts Me (effect a), (3) show Me predicts Y controlling for X (effect b), (4) compare c with c' [source_path, pp.7-8]. Complete mediation occurs when c' turns to zero; partial mediation when c' departs from zero [source_path, p.8].

Wu and Zumbo note that Kenny et al. (1998) later specified that only steps 2 and 3 are essential conditions, and that step 1 is not strictly necessary because: (1) an overall effect is implied if steps 2 and 3 are met, (2) suppressor effects are possible, and (3) multiple mediation effects can cancel each other out [source_path, p.8].

Key limitation: "the mediator is merely measured, despite the independent variable being randomly manipulated" which means "Kenny's mediational model cannot provide convincing evidence that the mediator actually causes Y" [source_path, p.9].

**b) Experimental-Causal-Chain Design (Spencer et al. 2005)**

The mediator is manipulated subsequently to act as an independent variable for Y, requiring two separate experiments: one establishing X causes Me, the other establishing Me causes Y [source_path, p.10]. Provides stronger causal inference but requires feasibility of manipulating the mediator [source_path, pp.10-11].

Drawback: the mediator measured in experiment 1 and manipulated in experiment 2 must be shown to be the same variable for the two causal links to connect [source_path, p.11].

**c) Sequence-Stage-Chain-Reaction Design (Collins et al. 1998)**

An alternative for categorical dependent variables and within-subject designs, emphasizing "the intra-individual, time-ordered nature of mediation" [source_path, p.11]. Mediation is viewed as "a chain reaction" with the same individuals going through the temporal chain [source_path, p.11]. Based on probability rather than regression [source_path, p.11].

Table 1 in the paper compares the minimum design requirements: Kenny requires manipulation of IV with observed Me and DV; Spencer requires manipulation of both IV and Me; Collins requires only precedence for all variables [source_path, p.12].

### 4. Moderation Design and Analysis

Key characteristics of a moderator: "an innate attribute, a relatively stable trait, or a relatively unchangeable background, environmental or contextual variable" [source_path, p.13]. A moderator does not change with the independent variable, nor should it correlate with the IV [source_path, p.14]. Moderators must be baseline or pre-treatment characteristics [source_path, p.14].

The moderation regression model: Y = i + aX + bMo + c(X*Mo), where c is the moderation effect representing "the unique synergistic effect of the two variables working together, over and above their separate effects" [source_path, p.14].

Centering continuous moderators is "highly recommended" to produce meaningful interpretations and eliminate non-essential multicollinearity, though centering does not alter the significance of the moderation test or the value of c [source_path, p.15].

Power for moderation: "the typical power of t-test for detecting a moderation effect ranges from .20 to .34, which is much lower than the recommended level of .80" [source_path, p.15].

### 5. Distinction Summary (Table 2)

The paper provides a comprehensive comparison table [source_path, pp.16-17]:

| Dimension | Mediator | Moderator |
|-----------|----------|-----------|
| Nature | State (temporary condition, transitory arousal) | Trait (stable characteristic, innate attribute) |
| Function | Links a cause and an effect | Modifies a causal effect |
| Question type | How and why | For whom and when |
| When to model | When causal effect is found | When causal effect is found or not found |
| Role | Dual (DV for X, IV for Y) | Single (auxiliary IV for Y) |
| Sequence | Follows IV, precedes DV | Precedes both IV and DV |
| Relation to IV | Correlated with IV | Uncorrelated with IV |
| Design control | Manipulated or observed | Typically observed |

Critical warning: "it is non-sensical to test an operationalized variable for both mediation and moderation effects" [source_path, p.23]. The appropriate role is determined by the researcher's substantive theory and operationalization [source_path, p.3].

### 6. Moderated Mediation

"The moderated mediation model hypothesizes that the mediation effect... depends on the value or level of the moderator" [source_path, p.18]. This model is "primarily mediational at its foundation" with the moderator having a secondary role [source_path, p.18]. A mediation effect must have been shown to occur first [source_path, p.18].

Alternative specifications vary by: which path(s) the moderator affects (a, b, or both), and how many moderators are invoked [source_path, p.19]. Data analytic strategies available in Preacher et al. (in press) [source_path, p.19].

### 7. Mediated Moderation

"A mediated moderation model hypothesized that a moderation effect is mediated by the fourth variable" [source_path, p.19]. This model is "primarily moderational at its foundation" with the mediator having a secondary role [source_path, p.19]. A moderated treatment effect must have been shown to occur first [source_path, p.19].

The mediated moderation effect is indicated by the product de (path d from X*Mo to Me, path e from Me to Y) [source_path, pp.19-20].

### 8. SEM for Mediation and Moderation

All regression approaches "assume that there is no measurement error in the scores of measured variables; that is, they are all measured with perfect reliability" [source_path, p.20]. Measurement errors attenuate association strength, overestimate IV→DV effect, and underestimate mediator→DV effect [source_path, p.20].

SEM advantages: (1) latent variables correct for measurement error, (2) flexibility to incorporate multiple causes/mediators/moderators in one model, (3) goodness-of-fit indices to assess model viability [source_path, pp.20-21].

SEM limitations: requires larger sample sizes, underlying data is covariance structure (correlational), and "drawing directional arrows from one construct to another does not render the power to make causal claims" [source_path, p.21].

Three criteria for causal inference via SEM (Bollen 1989; Kenny 1979): (1) true population association, (2) association is not spurious, (3) cause precedes effect in time [source_path, p.21].

### 9. Model Misspecification

Sources of misspecification [source_path, pp.22-23]:
- Incorrect functional form (linear assumed; non-linear relationships possible but "hardly discussed in the literature") [source_path, p.22]
- Alternative models: "there are alternative models, with different patterns of relationships among the variables, that fit the data equally well as the chosen model" [source_path, p.22]
- Incorrect hypothesized causal direction ("cause-and-effect types of language frequently slip into the research reports in which the data are correlational in nature") [source_path, p.22]
- Omitted variables: "could bias estimates of the mediation and moderation effects and result in incorrect conclusions" [source_path, pp.22-23]
- Violation of conditional independence when data is hierarchical or longitudinal [source_path, p.23]

### 10. Statistical Testing of Mediation Effect

The Sobel test (1982, 1988) directly tests the significance of ab against a normal Z distribution with SE approximately equal to √(b²SE²_a + a²SE²_b) [source_path, p.9]. However, the Sobel test "has been shown to have low statistical power because the distribution of ab often departs from a normal distribution" [source_path, p.9].

Alternatives when sample size is small [source_path, p.9]:
- MacKinnon's Z' statistic (empirical sampling distribution; critical values at http://www.public.asu.edu/~davidpm/ripl/methods.htm)
- Bootstrapping the standard error of ab (procedures in Mallinckrodt et al. 2006; Shrout and Bolger 2002)

## Methodology

Conceptual review and methodological synthesis. No empirical data collected. The paper reviews, compares, and integrates multiple frameworks for mediation and moderation using hypothetical examples (test difficulty → test anxiety, drug abuse prevention → resistance → refusal, instructional method → learning outcomes) [source_path, pp.1-2].

## Key Findings

This is a methodological review paper; "findings" are recommendations:

1. Mediation and moderation are "theoretical formulations for causal relationships rather than mere data analytic techniques" [source_path, p.23]
2. Mediators are states/processes occurring after the cause; moderators are traits/characteristics occurring before the cause [source_path, p.23]
3. "Empirical testing of causal models such as mediation and moderation effects require causal design and arguments to rule out alternative hypotheses" [source_path, p.23]
4. "It is non-sensical to test an operationalized variable for both mediation and moderation effects" [source_path, p.23]

## Relevance to Current Research

For the DBA thesis on organizational restructuring and GenAI, this paper provides:
- Rigorous grounding for any mediator/moderator variables proposed in the quantitative phase
- The integrated research design argument supports the sequential mixed-methods approach (qualitative constructs first, then quantitative testing)
- The four levels of design control help evaluate what causal inferences the thesis design can legitimately support
- Moderated mediation / mediated moderation frameworks apply if the thesis proposes complex multi-variable models
- The model misspecification warnings apply directly: cross-sectional survey data limits causal claims regardless of statistical technique

## Limitations

- Purely conceptual review; no empirical demonstration of the recommended approaches
- Does not cover more recent developments in causal mediation (e.g., counterfactual-based approaches, potential outcomes framework)
- Limited coverage of multilevel mediation (acknowledged as emerging at time of writing) [source_path, p.23]
- Software guidance is dated (2007 URLs for SPSS macros)

---

<!-- OBSIDIAN-LINKS:START (auto-generated by scripts/obsidian-graph-linker.py, do not edit by hand) -->
## Related
- **Related**: [[data/wiki/shared/methods/baron-kenny-moderation-mediation|baron-kenny-moderation-mediation]]
<!-- OBSIDIAN-LINKS:END -->
