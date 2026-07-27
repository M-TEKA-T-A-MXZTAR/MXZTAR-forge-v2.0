# Editor Command Strip Correction

PR #66 failed T1700 live acceptance because its always-open command tree reduced the usable Editor workspace.

The accepted replacement is one fixed row containing Document, Shape, Edit, Object, View, and the mouse-wheel selector. Each category opens a temporary dropdown that closes after selection. No permanent command tree or expanded list is allowed. The original in-page category buttons must be hidden so the interface exposes only one command row while retaining the current-document selector.

At a 980 x 760 window, the row must be no more than 48 pixels high. At the supported 760-pixel minimum window width, all five categories and the shortened wheel selector must remain visible without clipping or forcing a wider window.

Wheel routing, output reveal, Project Trash, project authority, and shutdown behaviour remain unchanged. Project Trash verification must retain writer-lock, recovery-receipt, receipt-failure rollback, active-detachment, and safe background-thread shutdown coverage.

This correction must pass focused automated verification and T1700 live acceptance before editable-path or tracing runtime work begins.
