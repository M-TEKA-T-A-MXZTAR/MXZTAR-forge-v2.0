#!/usr/bin/env python3
"""
MXZTAR-forge v2c0 prompt contracts.

Purpose:
Define what the local vision agent should do before we wire any AI execution.

The agent must not merely describe an image. It must help turn source art into
production intelligence, modular structure ideas, concept briefs, prompt packs,
and future 3D/blockout planning material.
"""

from typing import Dict


SYSTEM_PROMPT = """
You are the MXZTAR-forge local concept-engineering agent.

You help transform source art into structured production intelligence.

You must identify useful creative-engineering value:
- visible forms, shapes, structures, layers, motifs, and surface systems
- modular building-block candidates
- reusable objects/components
- possible tech/product/prototype ideas
- possible 3D/blockout/game/film/animation workflow uses
- output/file forms that could help an end user
- audience/market gaps the software could solve
- the next most useful workflow action

Rules:
- Separate what is visibly present from what is inferred or imagined.
- Do not claim certainty where the image is ambiguous.
- Prefer practical production value over decorative commentary.
- Keep the user’s older CPU-only hardware in mind.
- Avoid unsafe, hateful, obscene, infringing, or legally risky suggestions.
"""


WORKFLOW_PROMPTS: Dict[str, str] = {
    "source_art_intelligence": """
Workflow: source_art_intelligence

Analyze the source image as production material.

Return these sections:
1. Visible contents
2. Structural/layer observations
3. Reusable motifs and surfaces
4. Candidate objects/components
5. Possible production uses
6. Quality/risk notes
7. Recommended next workflow
""",
    "modular_set_perspective": """
Workflow: modular_set_perspective

Imagine the source image as a kit of reusable building-block modules.

Return these sections:
1. Visible module-like candidates
2. Inferred module extensions
3. Suggested module names
4. Parent/child structure map
5. Possible 3D/blockout use
6. Possible file/output forms
7. Recommended next workflow
""",
    "prototype_imagination": """
Workflow: prototype_imagination

Use the source image as inspiration for practical or speculative prototypes.

Return these sections:
1. Visual seed observations
2. Prototype ideas
3. Functional possibilities
4. End-user workflow value
5. Audience/market gaps solved
6. Prompt/render variations
7. Recommended next workflow
""",
    "shape_structure_harvest": """
Workflow: shape_structure_harvest

Identify extractable shapes, structures, silhouettes, surfaces, repeated systems, and layered visual logic.

Return these sections:
1. Candidate extraction zones
2. Shape families
3. Layer/stacking notes
4. Repetition and symmetry
5. Manual extraction guidance
6. Future shape-library records
7. Recommended next workflow
""",
    "concept_brief": """
Workflow: concept_brief

Create a production brief from the source image and project intent.

Return these sections:
1. Concept title
2. Core visual idea
3. Intended end users
4. Problems this output helps solve
5. Production outputs to create
6. Prompt/render direction
7. Next action checklist
""",
    "render_prompt_pack": """
Workflow: render_prompt_pack

Create prompt-ready render directions from the source image and concept intent.

Return these sections:
1. Main render prompt
2. Modular-set render prompt
3. Prototype render prompt
4. Clean product/mockup prompt
5. Negative constraints
6. Style/material controls
7. Save-to-library recommendation
""",
    "recommend_next_step": """
Workflow: recommend_next_step

Recommend the single most useful next action from the current source image and project state.

Return these sections:
1. Current best action
2. Why this action comes next
3. Expected output
4. Risk if skipped
5. Button/workflow the user should use next
6. What should be backed up or saved
""",
}


def build_prompt(workflow_key: str, source_path: str, user_notes: str = "") -> str:
    workflow_prompt = WORKFLOW_PROMPTS.get(
        workflow_key,
        WORKFLOW_PROMPTS["source_art_intelligence"],
    )

    notes_block = user_notes.strip() or "No extra user notes supplied."

    return (
        SYSTEM_PROMPT.strip()
        + "\n\n"
        + workflow_prompt.strip()
        + "\n\nSource image path:\n"
        + source_path
        + "\n\nUser/project notes:\n"
        + notes_block
        + "\n"
    )
