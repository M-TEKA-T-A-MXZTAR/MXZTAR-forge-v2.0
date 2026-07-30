# Unified Project Menu and Editable Project Names

## Founder-directed correction

Project switching, project deletion, and **New Project + Document** must not remain scattered across separate buttons. Start Here and Editor each expose one compact **Project** dropdown containing:

1. `Switch Project…`
2. `New Project + Document…`
3. `Rename Selected Project…`
4. `Delete Selected Project…`

Refresh and project-close authority remain separate because they are not replacements for those selected-project operations.

## Editable display-name contract

The project selector is editable in Start Here and Editor. Clicking the displayed project name allows direct editing. While the user types, matching visible project values update immediately. The rename is committed on normal edit completion.

A project rename changes only the validated display value. It does **not** rename the canonical project directory and does not replace the immutable `project_id`. This preserves writer locks, Project Trash receipts, project paths, artifact references, and provenance.

The guarded rename transaction updates:

- `project.json -> project_name`;
- `updated_at_utc` and the last-opened application version;
- the first README heading;
- one appended `project_renamed` history event containing old and new names;
- the attached session manifest snapshot when the project is open;
- Start Here and Editor selector labels and attached-project presentation.

An inactive selected project may be renamed only after Forge acquires a temporary writable project lease. Locked and recovery-only projects remain protected.

Duplicate display names are allowed because identity remains project-ID based. Selectors append a short immutable project-ID suffix when duplicate names would otherwise be indistinguishable.

## Rollback and authority

Manifest, README, and history changes share one transaction marker and rollback boundary. If rollback cannot be confirmed, writable authority is revoked and explicit recovery is required.

No project directory migration, schema-version change, object transform change, AI work, or Project Trash behavior is included in this correction.

## Live acceptance

T1700 acceptance must confirm:

- Start Here and Editor each show one Project dropdown;
- the three former Switch/Delete/New controls are not separately visible;
- clicking the selected project name permits editing;
- matching visible values update while typing;
- committing a valid name persists after restart;
- the project directory and immutable ID remain unchanged;
- duplicate names remain distinguishable;
- active-work and lock protections still disable project mutations.
