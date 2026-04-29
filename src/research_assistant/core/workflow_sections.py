"""
Workflow Section Templates — defines the section-by-section structure
for each workflow type. Used by IterativeProcessor.write_sections().

Each workflow type has a list of sections with name + instructions.
These are generic enough to work across any persona/space.
"""

from typing import List, Dict


def get_sections_for_workflow(workflow_name: str, query: str = "") -> List[Dict[str, str]]:
    """Get section templates for a workflow type. Returns empty list for simple workflows."""
    
    query_lower = query.lower()
    
    if workflow_name == "guide":
        # Detect sub-type from query
        if any(kw in query_lower for kw in ["case study", "case writing", "teaching case"]):
            return CASE_STUDY_SECTIONS
        elif any(kw in query_lower for kw in ["thesis", "dissertation", "chapter"]):
            return _detect_thesis_chapter(query_lower)
        elif any(kw in query_lower for kw in ["research paper", "journal paper", "manuscript"]):
            return RESEARCH_PAPER_SECTIONS
        elif any(kw in query_lower for kw in ["literature", "lit review", "survey", "systematic review"]):
            return LIT_REVIEW_SECTIONS
        return []  # Simple guide — single call is fine
    
    elif workflow_name == "research":
        return RESEARCH_WORKFLOW_SECTIONS
    
    elif workflow_name == "quant":
        return QUANT_WORKFLOW_SECTIONS
    
    elif workflow_name == "review":
        return []  # Reviews are evaluative, not generative — single call
    
    elif workflow_name == "explain":
        return []  # Explanations are usually short enough for single call
    
    return []


def get_extraction_prompt(workflow_name: str, query: str = "") -> str:
    """Get the extraction prompt for iterative document analysis."""
    query_lower = query.lower()
    
    if any(kw in query_lower for kw in ["case study", "case writing", "benchmark"]):
        return CASE_STUDY_EXTRACTION
    elif any(kw in query_lower for kw in ["literature", "lit review", "survey"]):
        return LIT_REVIEW_EXTRACTION
    elif any(kw in query_lower for kw in ["thesis", "dissertation"]):
        return THESIS_EXTRACTION
    
    # Generic extraction
    return """Extract from this document:
- Main argument or thesis
- Key findings or contributions
- Methodology used
- Strengths and limitations
- How it relates to the research question"""


def get_synthesis_prompt(workflow_name: str, query: str = "") -> str:
    """Get the synthesis prompt for combining document analyses."""
    query_lower = query.lower()
    
    if any(kw in query_lower for kw in ["case study", "benchmark"]):
        return ("Synthesize into a 'Publication Playbook': structural patterns, "
                "opening hook conventions, section structure, exhibit patterns, "
                "voice rules, tension levers, and a publication readiness checklist.")
    elif any(kw in query_lower for kw in ["literature", "lit review"]):
        return ("Synthesize into a literature landscape: key themes, theoretical frameworks, "
                "methodological approaches, research gaps, and a conceptual framework "
                "showing how the studies relate to each other.")
    elif any(kw in query_lower for kw in ["thesis", "dissertation"]):
        return ("Synthesize into structural guidance: chapter organization patterns, "
                "argumentation flow, evidence presentation, and quality benchmarks.")
    
    return ("Synthesize all analyses into a comprehensive framework: "
            "common patterns, key insights, gaps identified, and actionable recommendations.")


# =============================================================================
# SECTION TEMPLATES
# =============================================================================

CASE_STUDY_SECTIONS = [
    {"name": "Opening Vignette",
     "instructions": "Write a vivid, tension-filled opening scene. Specific date, protagonist full name, physical scene with sensory details, immediate tension signal. 500-800 words."},
    {"name": "Company Background",
     "instructions": "Build the protagonist and company history. Founding story, growth trajectory, current state with key numbers. Establish character depth naturally. 600-900 words."},
    {"name": "Industry Context",
     "instructions": "Present the industry ecosystem with enough depth for unfamiliar readers. History, business model, labor dynamics, market forces. 600-900 words."},
    {"name": "The Crisis",
     "instructions": "Present the crisis with hard numbers. Break down each dimension of the problem with actual data from source materials. Frame the central strategic metaphor. 800-1000 words."},
    {"name": "Strategic Options",
     "instructions": "Lay out each strategic option with honest pros, cons, and risks. Use ONLY data from source materials. No fabrication. Equal treatment per option. 800-1200 words."},
    {"name": "Decision Point",
     "instructions": "Return to the opening tension. Present the unresolved dilemma with explicit questions. NO resolution, NO recommendation. End with tension. 300-500 words."},
    {"name": "Exhibits",
     "instructions": "Create all data exhibits as markdown tables. Use ONLY numbers from source materials. Use [PLACEHOLDER: ...] for missing data."},
]

RESEARCH_PAPER_SECTIONS = [
    {"name": "Abstract",
     "instructions": "Write a structured abstract: background, purpose, methodology, key findings, implications. 200-300 words."},
    {"name": "Introduction",
     "instructions": "Establish the research problem, its significance, the gap in literature, and the research questions/objectives. End with paper structure overview. 800-1200 words."},
    {"name": "Literature Review",
     "instructions": "Review relevant literature organized thematically. Identify theoretical frameworks, key findings from prior work, and the specific gap this research addresses. 1500-2500 words."},
    {"name": "Methodology",
     "instructions": "Describe research design, sample, data collection, variables/constructs, measurement instruments, and analysis techniques. Justify each choice. 1000-1500 words."},
    {"name": "Results",
     "instructions": "Present findings systematically. Descriptive statistics first, then hypothesis tests. Use tables for key statistics. Report effect sizes and confidence intervals. 1000-1500 words."},
    {"name": "Discussion",
     "instructions": "Interpret findings in context of literature. Address each research question. Discuss theoretical and practical implications. Acknowledge limitations. 1000-1500 words."},
    {"name": "Conclusion",
     "instructions": "Summarize key contributions, implications for practice and theory, limitations, and future research directions. 400-600 words."},
]

LIT_REVIEW_SECTIONS = [
    {"name": "Search Strategy",
     "instructions": "Document the systematic search: databases, keywords, inclusion/exclusion criteria, date range, PRISMA flow data. 300-500 words."},
    {"name": "Thematic Analysis",
     "instructions": "Organize literature by themes. For each theme: key studies, findings, methodologies, and how they relate. 1500-2500 words."},
    {"name": "Theoretical Framework Mapping",
     "instructions": "Map the theoretical landscape: which frameworks are used, how they relate, which are dominant vs emerging. 600-1000 words."},
    {"name": "Methodological Assessment",
     "instructions": "Assess methodological approaches across studies: designs used, sample sizes, analysis techniques, quality indicators. 600-800 words."},
    {"name": "Research Gaps",
     "instructions": "Identify specific gaps: what hasn't been studied, what needs replication, what methodological improvements are needed. 400-600 words."},
    {"name": "Conceptual Framework",
     "instructions": "Propose a conceptual framework showing how the reviewed literature connects. Identify variables, relationships, and boundaries. 400-600 words."},
]

RESEARCH_WORKFLOW_SECTIONS = [
    {"name": "Research Framing",
     "instructions": "Clarify the research objective, theoretical lens, scope and boundaries. What exactly are we investigating and why? 500-800 words."},
    {"name": "Literature Landscape",
     "instructions": "Map relevant sources from KB. Identify theoretical frameworks, key findings, and gaps. Suggest search terms for additional sources. 800-1200 words."},
    {"name": "Methodology Design",
     "instructions": "Recommend research design, data collection methods, variables, validity/reliability considerations, and ethical implications. Justify each choice. 800-1200 words."},
    {"name": "Research Roadmap",
     "instructions": "Provide phased timeline with milestones, risks and mitigation, resource requirements, and concrete next steps. 500-800 words."},
]

QUANT_WORKFLOW_SECTIONS = [
    {"name": "Data Understanding",
     "instructions": "Identify variables (types, scales), sample structure, research hypotheses, and data quality considerations. 400-600 words."},
    {"name": "Method Selection",
     "instructions": "Recommend statistical tests with justification. Explain WHY each method is appropriate. List assumptions to check. Reference KB materials. 600-1000 words."},
    {"name": "Analysis Plan",
     "instructions": "Step-by-step procedure: assumption checks, descriptive stats, main analysis, post-hoc tests. Include software commands where applicable. 600-1000 words."},
    {"name": "Interpretation Guide",
     "instructions": "How to read output: which numbers matter, significance vs practical significance, effect size benchmarks, APA reporting format. 500-800 words."},
    {"name": "Reporting Template",
     "instructions": "Results section template with [PLACEHOLDER: ...] for actual values. Include table formats. 400-600 words."},
]


# Extraction prompts for document analysis
CASE_STUDY_EXTRACTION = """Extract from this case study:
- Narrative structure (hook, build-up, decision point, conclusion)
- How the protagonist's dilemma is framed and sustained
- Use of exhibits and data (financial tables, industry data, timelines)
- Sectioning pattern and page depth per section
- Voice and tense choices (first-person vs third-person, past vs present)
- What makes it publishable — the tension, the stakes, the pedagogical utility"""

LIT_REVIEW_EXTRACTION = """Extract from this paper:
- Research question and objectives
- Theoretical framework used
- Methodology (design, sample, analysis)
- Key findings and contributions
- Limitations acknowledged
- How it relates to the broader research landscape"""

THESIS_EXTRACTION = """Extract from this chapter/document:
- Chapter structure and organization pattern
- Argumentation flow (how claims are built and supported)
- Evidence presentation style (data, citations, examples)
- Transitions between sections
- Quality indicators (depth, rigor, clarity)"""


def _detect_thesis_chapter(query_lower: str) -> List[Dict[str, str]]:
    """Detect which thesis chapter type and return appropriate sections."""
    if any(kw in query_lower for kw in ["introduction", "chapter 1", "intro"]):
        return [
            {"name": "Research Context", "instructions": "Establish the broad context and significance of the research area. 400-600 words."},
            {"name": "Problem Statement", "instructions": "Define the specific problem, its scope, and why it matters. 300-500 words."},
            {"name": "Research Questions", "instructions": "State research questions/objectives clearly. Link each to the problem. 200-400 words."},
            {"name": "Significance", "instructions": "Explain theoretical and practical contributions. 300-400 words."},
            {"name": "Chapter Overview", "instructions": "Brief overview of remaining chapters. 200-300 words."},
        ]
    elif any(kw in query_lower for kw in ["methodology", "method", "chapter 3"]):
        return [
            {"name": "Research Philosophy", "instructions": "State and justify the philosophical position (positivism, interpretivism, etc.). 300-500 words."},
            {"name": "Research Design", "instructions": "Describe and justify the overall design (experimental, survey, case study, etc.). 400-600 words."},
            {"name": "Data Collection", "instructions": "Detail sampling, instruments, procedures. Justify each choice. 500-800 words."},
            {"name": "Data Analysis", "instructions": "Describe analysis techniques, software, and quality criteria. 400-600 words."},
            {"name": "Ethical Considerations", "instructions": "Address ethics: consent, anonymity, IRB approval, data handling. 200-400 words."},
        ]
    elif any(kw in query_lower for kw in ["results", "findings", "chapter 4"]):
        return [
            {"name": "Descriptive Statistics", "instructions": "Present sample demographics, variable distributions, and preliminary analysis. 400-600 words."},
            {"name": "Assumption Testing", "instructions": "Report results of assumption checks (normality, multicollinearity, etc.). 300-500 words."},
            {"name": "Hypothesis Testing", "instructions": "Present main analysis results organized by research question/hypothesis. 800-1200 words."},
            {"name": "Summary of Findings", "instructions": "Tabular summary of all hypotheses and their outcomes. 200-400 words."},
        ]
    elif any(kw in query_lower for kw in ["discussion", "chapter 5"]):
        return [
            {"name": "Summary of Key Findings", "instructions": "Recap main findings concisely. 300-400 words."},
            {"name": "Discussion of Results", "instructions": "Interpret each finding in context of literature. Compare with prior studies. 800-1200 words."},
            {"name": "Theoretical Implications", "instructions": "How findings extend or challenge existing theory. 400-600 words."},
            {"name": "Practical Implications", "instructions": "Actionable recommendations for practitioners. 400-600 words."},
            {"name": "Limitations and Future Research", "instructions": "Honest limitations and specific future research directions. 400-600 words."},
        ]
    # Generic thesis chapter
    return RESEARCH_PAPER_SECTIONS
