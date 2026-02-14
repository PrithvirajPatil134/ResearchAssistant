# QNTR Knowledge Base

This directory contains all materials that inform the QNTR persona (Prof. Atul Prashar simulation).

## Directory Structure

```
knowledge/
├── research_papers/     # Professor's published research (highest priority)
├── class_slides/        # Lecture slides and presentations
├── assignments/         # Assignment templates and rubrics
├── documents/           # Course documents, syllabi
└── course_materials/    # Other course-related files
```

## Adding Materials

1. Place files in the appropriate subdirectory based on type
2. **Supported formats**: `.md`, `.txt`, `.pdf`, `.docx`
3. Materials are automatically indexed when the persona is loaded

## Priority Order

When generating responses, the system prioritizes sources in this order:
1. **Research papers** - Highest authority for academic content
2. **Class slides** - Teaching perspective and course structure
3. **Assignments** - Expectations, rubrics, grading standards
4. **Documents** - Supplementary course information

## How It Works

The workflow agents will:
- **Extract** tone, terminology, and preferences from these materials
- **Reference** specific slides/pages when explaining concepts
- **Apply** grading standards from assignment rubrics
- **Build** context progressively from all materials
- **Cite** sources in responses

## Example Usage

To add a research paper:
```
knowledge/research_papers/brand_communities_2023.pdf
```

To add lecture slides:
```
knowledge/class_slides/lecture_01_brand_equity.pdf
knowledge/class_slides/lecture_02_internal_branding.pdf
```

To add an assignment:
```
knowledge/assignments/case_study_rubric.md
knowledge/assignments/final_project_guidelines.pdf
```

## Notes

- The persona will adapt its responses based on the materials present
- More materials = more accurate simulation of Prof. Prashar's style
- Regular updates to this knowledge base improve persona accuracy
