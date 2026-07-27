# Editor Command Strip Correction

PR #66 failed T1700 live acceptance because its always-open command tree reduced the usable Editor workspace.

The accepted replacement is one fixed row containing Document, Shape, Edit, Object, View, and the mouse-wheel selector. Each category opens a temporary dropdown that closes after selection. No permanent command tree or expanded list is allowed. At a 980 x 760 window, the row must be no more than 48 pixels high.

Wheel routing, output reveal, Project Trash, project authority, and shutdown behaviour remain unchanged.

This correction must pass focused automated verification and T1700 live acceptance before editable-path or tracing runtime work begins.
