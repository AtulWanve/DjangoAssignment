# Project Context

## Problem Being Solved
Warehouse teams need to know which shipping box to use when a customer places an order. The system must take a list of products (with dimensions/weight) and select the cheapest box that physically fits all items and supports their total weight.

## Current Architectural Decisions
- **Framework**: Standard Django, minimal dependencies.
- **Database**: SQLite (stateless for orders, stateful for Boxes/Products).
- **Interface**: Django Admin (for Box/Product management) + 1 REST-like JSON endpoint (`/api/recommend-box/`).
- **Algorithm**: Greedy 3D Space Partitioning (Guillotine Split), tracking only dimensions (not explicit X/Y/Z coordinates).

## Known Limitations
- **Space Fragmentation**: Because the algorithm only tracks the dimensions of remaining empty spaces (not coordinates), it cannot merge adjacent empty spaces. This may cause occasional "False Negatives" (saying a box doesn't fit when a human could make it fit).
- **No Packing Instructions**: The system outputs a box recommendation, but cannot tell the warehouse worker *how* to arrange the items.

## Current Implementation Status
- **Phase 0 (Planning)**: Completed. Architecture and algorithm selected. Documentation files initialized.
- **Phase 1 (Models/Setup)**: Pending approval.
- **Phase 2 (Algorithm)**: Pending.
- **Phase 3 (API)**: Pending.
- **Phase 4 (Docs/Tests)**: Pending.

## Important Assumptions
- Products are rigid rectangular prisms.
- Products can be rotated in any of 6 3D orientations.
- Weight is distributed evenly enough that we only need to check total weight vs. max weight.