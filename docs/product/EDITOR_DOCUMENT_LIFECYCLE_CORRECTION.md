# Editor Document Lifecycle and Static Guidance Correction

T1700 live acceptance after PR #67 identified two remaining Editor usability requirements.

## Document menu authority

The fixed `Document` dropdown must expose:

- `Close Document` — detach the current document from the visible workspace without changing canonical project files;
- `Delete Document…` — after explicit confirmation, remove the current canonical shape document, its autosave, and its paired 3D object scene from project authority.

Document deletion is a guarded transaction. Shape, scene, manifest and project-history changes share one rollback boundary. A failed deletion must restore prior bytes or revoke writable authority and require recovery.

## Guidance behaviour

The `Next` action remains available as useful workflow guidance, but it must remain visually static. No pulsing, flashing, alternating border, or attention-grabbing timer is permitted.

## Scope boundary

This correction does not add tracing, extraction, freeform paths, export, Shape Library approval, permanent project erasure, or new AI capability. It must pass focused real-Qt verification and T1700 live acceptance before later Editor milestones proceed.
