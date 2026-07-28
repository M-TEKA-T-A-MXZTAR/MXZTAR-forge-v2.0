# Visible Deletion and Editor Entry Correction

## Live acceptance findings

T1700 acceptance after PR #68 showed three presentation failures:

1. deleting one document immediately opened another same-title document, making the completed deletion appear ineffective;
2. Start Here project deletion was crowded into the Purpose row and its result was reported away from the project controls;
3. entering Editor automatically scrolled the page beneath the fixed command strip, leaving clipped text visible below the strip.

## Corrected runtime contract

- Every document selector entry includes a short stable document-ID suffix so same-title documents remain distinguishable.
- Successful Delete Document leaves the 2D/3D workspace empty and the selector unselected.
- Remaining documents stay listed but reopen only after deliberate selection.
- The deletion result is stated beside the Editor workspace and includes the deleted document identity and remaining count.
- Start Here exposes Delete Selected Project and New Project + Document in a dedicated Project management row.
- Project Trash success, cancellation, and failure feedback appears beside Project Authority rather than only at the bottom of the page.
- Entering Editor positions the scroll area at its top so introductory and document text is not clipped beneath the fixed strip.
- Explicit 2D/3D output reveal aligns to the output boundary without leaving a partial line of preceding text.

## Authority boundary

This correction does not weaken or replace the existing document-deletion or Project Trash transactions. Canonical files, manifest registration, history events, exclusive project leases, rollback, and writable-authority revocation remain governed by their existing core modules.

No new AI capability, geometry operation, export path, approval authority, or permanent project erasure is introduced.
