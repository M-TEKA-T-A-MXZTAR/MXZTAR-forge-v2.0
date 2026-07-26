# MXZTAR Forge v2.0 — Asset Generation and Construct Architecture

## 1. Authority

**Status:** founder-authorised active Stage One–Two sequencing addendum.  
**Effective date:** 27 July 2026.  
**Runtime capability:** planning and architecture only unless a capability is separately recorded as implemented and verified.

This document brings forward the work that creates the richest reusable asset foundation:

```text
editable path authority
→ manual and deterministic extraction
→ shipped starter source assets
→ reviewed reusable shapes
→ reversible shape-to-component generation
→ selectable objects, surfaces, and areas
→ pivot, anchor, and surface-assisted placement
→ groups and recoverable assemblies
→ reversible surface-effect stacks
→ explicit contact, stitch, weld, join, boolean, separate, or bake operations
```

For active engineering order, this document supersedes older immediate-sequence lists that delay shipped starter assets, selectable surface areas, modular placement, and effect-stack authority until late in Stage Two. It does not claim those capabilities already exist.

The Master Build Plan remains the finished-product boundary. This addendum controls the nearer implementation sequence until its rules are integrated into the next full Master Build Plan reconciliation.

---

## 2. Product decision

Forge must begin producing and accumulating useful editable assets earlier.

The asset-producing workflows are not secondary polish. They are the engine that creates compounding product value:

```text
one source image or blank document
→ several editable shapes
→ several reviewed variants
→ several reversible 3D components
→ modules, groups, and assemblies
→ reusable construction families
```

The software will ship with a founder-controlled starter source-asset set. Later releases may add more source files, reviewed shapes, construction recipes, modules, examples, and effect profiles without making bundled content the authority over a user project.

---

## 3. Non-negotiable authority boundaries

1. **Source evidence is not editable geometry.** A source image, model description, or detected region remains evidence until coordinates are created and accepted.
2. **A shape is not a component.** A reviewed 2D path may become one or more reversible 3D components through a declared construction recipe.
3. **Visual contact is not a stitch.** Moving objects together does not silently group, assemble, weld, join, boolean, or bake them.
4. **A surface effect is not an engineering material claim.** Metallic, rough, bent, distorted, luminous, or worn appearances remain visual design properties unless specialist validation says otherwise.
5. **An object group is not a mesh merge.** Groups and assemblies preserve member identity.
6. **AI remains optional and advisory.** Ollama may assess, rank, label, or propose candidates, but user-correctable coordinates and explicit acceptance establish project truth.
7. **No dead interface controls.** Context-menu entries appear only when their handler, artifact authority, Undo/Redo rule, error path, persistence contract, and verifier exist.
8. **All consequential operations are visible.** Extraction, approval, effect application, grouping, assembly, stitching, welding, joining, booleans, separation, and baking remain explicit user actions.

---

## 4. Shipped starter source-asset contract

### 4.1 Purpose

The installed Forge package will include a bounded starter collection that lets a new user create, edit, generate, and assemble useful assets without first sourcing external artwork.

### 4.2 Bundled asset classes

The starter collection may contain:

- original founder-owned source images;
- primitive and freeform 2D shape documents;
- reviewed shape variants;
- declared shape-to-component recipes;
- editable example components;
- anchor and socket examples;
- object-group and assembly examples;
- surface-area examples;
- effect-profile examples;
- tutorial projects and deterministic verification fixtures.

### 4.3 Installation and ownership rules

Bundled assets must be:

- stored under a dedicated read-only application asset root;
- listed through a versioned manifest;
- assigned stable asset IDs and content hashes;
- accompanied by provenance, licence, version, and compatibility metadata;
- copied into a user project before the user edits them;
- never silently modified in place;
- replaceable or extensible through future signed/versioned asset-pack updates;
- separable from private user-created assets.

The repository already defines an application `assets` root. The implementation must add explicit subdirectories and manifests rather than scattering starter files through runtime code.

### 4.4 Proposed installed layout

```text
assets/
  starter_pack/
    manifest.json
    sources/
    shapes/
    recipes/
    components/
    groups/
    assemblies/
    effects/
    tutorials/
    licences/
```

### 4.5 Starter-pack manifest minimum fields

```text
pack_id
pack_version
schema_version
publisher
licence_id
created_at
compatible_forge_versions
assets[]
  asset_id
  asset_type
  relative_path
  sha256
  display_name
  tags
  provenance
  editable_copy_required
  dependencies
  compatibility_version
```

---

## 5. Core asset vocabulary and records

### 5.1 Source asset

An unchanged project-owned or application-bundled input with identity, hash, provenance, licence, preview, and processing history.

### 5.2 Editable shape

A versioned 2D contour, path, mask, profile, or composition with nodes, handles, transforms, command history, provenance, and approval state.

### 5.3 Component

A project-owned editable 3D object generated through a declared recipe or created directly from a supported primitive. A component retains its source shape IDs, recipe, parameters, origin, pivot, and history.

### 5.4 Module

A reusable component that declares compatibility rules, anchors, sockets, dimensions, permitted orientations, and variation boundaries.

### 5.5 Area or surface subset

A stable selectable subset of an object or component used as a target for focus, anchors, effects, visual seams, connections, or later geometry operations.

An area record must include:

```text
area_id
owner_object_id
selection_kind
selection_definition
local_coordinate_frame
surface_normal_or_orientation
label
provenance
created_by_command_id
version
```

Initial selection kinds may include:

- whole object;
- declared face;
- bounded panel or inset;
- path-defined surface region;
- edge set;
- attachment area;
- generated effect region.

### 5.6 Anchor or socket

A named local coordinate frame used for placement and compatibility. It may define position, orientation, normal, permitted rotation, compatible types, clearance, and snap tolerance.

### 5.7 Object group

A named selection set used for shared selection, visibility, movement, organisation, and effect targeting. Members remain independent objects.

### 5.8 Assembly

A recoverable hierarchy of components, modules, groups, anchors, contact relationships, and constraints. Members retain identity and can be edited or replaced.

### 5.9 Effect stack

An ordered, reversible list of visual or geometric design effects targeting an object, area, surface subset, group, or assembly.

### 5.10 Connection or stitch record

An explicit relationship between named endpoints. It identifies whether the relationship is visual, organizational, assembly-level, mesh-level, or baked.

---

## 6. Central construct point and placement model

Every Construct scene must expose a stable project-owned construct origin and optional focus pivot.

The user must be able to:

- move components around the central construct point;
- orbit and zoom around the current focus target;
- set an object, group, assembly, anchor, area, or surface as the focus target;
- align an object pivot to the construct origin;
- align one anchor or surface normal to another;
- place modules through explicit snapping without silently joining them;
- return to the global construct origin at any time.

Placement sequence:

```text
select component
→ choose global origin, focus pivot, anchor, or surface target
→ move / rotate / scale
→ preview alignment, clearance, and intersection
→ accept placement
→ optionally declare group, assembly, contact, or stitch relationship
```

The current guide system may later be extended from scene-centre and object-edge guidance to pivot, anchor, surface-normal, socket, and contact guidance. Those extensions require separate verified commands.

---

## 7. Navigation, perspective, and focus framework

### 7.1 Empty-space context menu

Right-clicking empty 3D space may eventually expose implemented commands such as:

- Frame Entire Construct;
- Focus Construct Origin;
- Perspective View;
- Orthographic Front;
- Orthographic Right;
- Orthographic Top;
- Isometric View;
- Save Current View;
- Restore Named View.

The view framework must permit additional named perspectives without duplicating camera logic.

### 7.2 Object context menu

Right-clicking a valid object may eventually expose:

- Select Object;
- Set as Primary Focus Object;
- Frame Selected Object;
- Focus Object Pivot;
- Add to Group;
- Create Group from Selection;
- Create Area or Surface Subset;
- Create Anchor or Socket;
- Add Effect;
- Connect or Stitch;
- Inspect Provenance;
- Open Numeric Inspector.

### 7.3 Surface or area context menu

Right-clicking a valid selected area may eventually expose:

- Set as Primary Focus Surface;
- View Along Surface Normal;
- Frame Area;
- Rename Area;
- Create Anchor from Area;
- Add Effect to Area;
- Copy Effect Stack;
- Connect Area to Anchor or Area;
- Add Visual Seam;
- Inspect Area Definition.

Context menus are command routes only. They must invoke the same command engines used by menus, inspectors, shortcuts, and tests.

---

## 8. Surface-effect tree

### 8.1 Effect-stack authority

Each effect entry requires:

```text
effect_id
effect_type
target_type
target_id
enabled
order
parameters
seed
blend_or_combine_mode
created_by_command_id
parent_effect_id
provenance
schema_version
```

Effect application must be:

- explicit;
- previewable;
- ordered;
- reversible;
- seed-stable when procedural;
- target-bounded;
- saved in project authority;
- recoverable after restart;
- removable without damaging the source object or area.

### 8.2 Initial effect families

#### A. Greebling

Adds bounded procedural panels, ribs, vents, recesses, fastener-like marks, channels, or repeated geometric detail.

Minimum parameters:

- density;
- scale range;
- depth or relief;
- spacing;
- orientation mode;
- symmetry mode;
- random seed;
- exclusion margin;
- raised, recessed, or mixed profile.

Greebling must initially remain a reversible detail recipe or instance field, not an uncontrolled destructive mesh operation.

#### B. Roughness

Controls visual micro-surface response.

Minimum parameters:

- roughness amount from `0.0` to `1.0`;
- uniform, noise, directional, or masked distribution;
- scale;
- seed;
- edge influence;
- area mask.

#### C. Distortion

Applies bounded visual or geometric variation.

Minimum parameters:

- amplitude;
- frequency;
- axis influence;
- noise type;
- seed;
- falloff;
- preserve-boundary option;
- preview quality.

#### D. Bend

Applies a declared reversible bend recipe.

Minimum parameters:

- bend intensity;
- bend axis;
- pivot or anchor;
- direction;
- start and end limits;
- falloff;
- preserve-thickness option;
- clamp range.

The bend-intensity selector must use bounded numeric authority rather than an unrecorded visual-only slider state.

#### E. Logic wiring

Adds conceptual visual routing across a target surface or object group. It is design intent, not verified electronics.

Initial routing modes:

1. **Randomized** — seeded non-repeating routes within declared bounds;
2. **Symbiotic** — routes follow nearby features, anchors, panels, or component relationships;
3. **Aligned** — routes follow selected axes, grids, edges, or normals;
4. **Radial** — routes grow from a declared focus point or hub;
5. **Parallel** — evenly spaced routes follow one direction.

Minimum parameters:

- route mode;
- density;
- line or conduit thickness;
- clearance;
- start and end anchors;
- branching;
- symmetry;
- seed;
- raised, recessed, emissive, or neutral visual profile.

#### F. Metallic hue profiles

The initial visual metallic profiles are:

1. **Brushed Titanium** — cool grey, directional brushing, medium roughness;
2. **Polished Chrome** — neutral bright reflection, low roughness;
3. **Anodized Aluminium** — coloured metallic tint with fine grain;
4. **Oxidized Copper** — copper base with bounded patina variation;
5. **Iridescent Nickel** — dark metallic base with angle-dependent hue shift.

Each profile must remain editable through explicit parameters rather than being stored only as a name. Minimum parameters include base hue, metallic response, roughness, anisotropy or grain direction, oxidation/patina amount where applicable, iridescence amount where applicable, reflectivity, and intensity.

These profiles are visual design effects, not declarations of real material composition, strength, conductivity, corrosion behaviour, or manufacturing suitability.

---

## 9. Areas, groups, and effect targeting

Effects must target named records rather than anonymous screen coordinates.

Valid target levels:

```text
object
→ area or surface subset
→ object group
→ assembly
```

Rules:

1. An effect targeting an area follows that area's local coordinate frame.
2. An effect targeting a group applies through explicit member rules and records per-member results.
3. An assembly-level effect cannot silently flatten member identity.
4. Removing a group or assembly relationship must not delete underlying components or effects unless the user explicitly chooses cascading deletion.
5. Area definitions must detect stale parent geometry and enter a repair/review state instead of silently targeting the wrong surface.

---

## 10. Connection and stitching model

Forge must expose separate named operations:

### A. Placement only

Objects are moved into contact or proximity. No relationship is created.

### B. Snap or align

A transform command aligns pivots, anchors, sockets, edges, centres, or surface normals. Objects remain independent.

### C. Group

Objects share selection and organisation but have no structural relationship.

### D. Assembly connection

Named anchors or areas are related through a recoverable contact, mate, parent, or compatibility record.

### E. Visual seam

A reversible seam, gasket, rim, trim, conduit, or bridging detail is generated between named areas. This changes appearance or adds a derived component but does not imply mesh welding or physical strength.

### F. Mesh stitch or weld

A future explicit geometry operation attempts to connect compatible open boundaries under declared tolerances. Failure must leave originals unchanged.

### G. Join mesh

Several mesh objects become one mesh object while source records and rollback or derivative provenance remain available.

### H. Boolean union, difference, or intersection

A named derived geometry operation with preview, validation, and parent mapping.

### I. Separate

A joined or derived result is split according to recorded structure or selected regions.

### J. Bake

A user-confirmed irreversible or explicitly derivative consolidation step. Originals remain preserved unless the user separately chooses deletion.

Merely placing objects around a central point must never trigger F–J automatically.

---

## 11. Brought-forward delivery sequence

PR #63 live acceptance remains the final gate for the existing viewport interaction correction. Documentation planning may proceed, but runtime work starts only after that acceptance is recorded.

The active engineering order becomes:

1. **Freeform path authority** — durable path, node, handle, segment, selection, transform, Undo/Redo, autosave, reopen, and rendering contracts.
2. **Source-region and manual trace** — exact region selection, trace overlay, path correction, candidate save, provenance.
3. **Deterministic extraction candidates** — bounded contour, threshold, edge, mask, and silhouette proposals through the same editable path schema.
4. **Starter source-asset pack** — installed manifest, read-only bundled assets, copy-into-project command, integrity and licence checks.
5. **Optional AI proposal through editable authority** — Ollama assessment or candidate proposal with model evidence, editable coordinates, user correction, and rejection.
6. **Review and reusable Shape Library** — approval, rejection, correction, versioning, supersession, discovery, and reversible insertion.
7. **Shape-to-component recipe registry** — extrude first, then bounded declared recipes; parent shape and parameter history retained.
8. **Area, surface, pivot, and focus authority** — stable area IDs, primary focus object/surface, frame/focus commands, named perspectives, anchor creation.
9. **Modular placement and central construct point** — pivot/anchor/surface alignment, snapping, clearance and intersection preview without automatic joining.
10. **Object groups and recoverable assemblies** — group records, hierarchy, member identity, anchors, contact relationships, replacement and reopen.
11. **Effect-stack core** — targetable ordered effect records, preview, Undo/Redo, persistence, stale-target handling.
12. **Initial surface effects** — greebling, roughness, distortion, bend, logic wiring, and five metallic hue profiles.
13. **Visual seams and explicit connection operations** — area-to-area seams, then separately verified stitch/weld/join/boolean/separate/bake operations.
14. **Verified asset continuation** — SVG/PNG for 2D assets and GLB/glTF/OBJ for components and assemblies through named downstream tests.
15. **Release asset-pack engineering** — installer inclusion, updates, checksums, migration, backup, licence, and offline recovery.

Each implementation PR advances one coherent authority layer. No PR should combine extraction, component generation, assembly, effects, and mesh operations into one unreviewable change.

---

## 12. First implementation milestone after PR #63 acceptance

The next runtime milestone is **Freeform Path Authority**, not surface effects or mesh stitching.

Required minimum result:

```text
New Path
→ place nodes
→ create line and Bezier segments
→ select and move nodes
→ edit handles
→ close or open path
→ Undo/Redo
→ autosave
→ canonical save
→ close and reopen without drift
```

This creates the common editable geometry authority used by manual tracing, deterministic extraction, AI proposals, reviewed shapes, and later construction recipes.

---

## 13. Verification requirements

Every promoted capability requires proportionate evidence:

- pure schema and migration contracts;
- deterministic command and Undo/Redo tests;
- restart and copied-project recovery;
- stale-parent and missing-dependency handling;
- bounded CPU and memory behaviour on the T1700;
- offscreen Qt interaction contracts;
- manual T1700 acceptance for context menus, focus, navigation, selection, and effects;
- seed stability for procedural effects;
- nonmutation of unrelated objects, areas, groups, and assemblies;
- failure rollback for stitching, joining, booleans, and baking;
- downstream continuation tests before export claims.

---

## 14. Current non-claims

This architecture does not claim that Forge currently provides:

- freeform paths or tracing;
- automatic editable extraction;
- a bundled starter asset pack;
- approved Shape Library records;
- selectable persistent surface subsets;
- primary focus surfaces;
- anchors, sockets, groups, or recoverable assemblies;
- greebling, roughness, distortion, bend, wiring, or metallic effect stacks;
- visual seams or mesh stitching;
- welding, mesh joining, booleans, separation, or baking;
- engineering material properties;
- manufacturing-safe geometry;
- verified SVG, PNG, GLB/glTF, or OBJ continuation.

Those capabilities become current only through focused implementation, verification, merge, T1700 evidence, and truthful capability-document updates.
