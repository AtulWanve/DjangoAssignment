# Local Context: Boxes App

## Purpose
This Django app contains the core domain logic for the Box Selection System. It manages the database models for Boxes and Products, the mathematical packing algorithm, and the JSON API endpoint for recommendations.

## Packing Algorithm Notes
The algorithm lives in `packing.py` (to be created) and uses a **Greedy Space Partitioning (Guillotine Split)** approach.
- It relies on `Space` and `Item` dataclasses.
- It places an `Item` into a `Space` and splits the remaining area into 3 new `Spaces` (Top, Right, Front).
- Rotation is handled by sorting item dimensions and testing all valid orientations against a space.
- It fails fast: if an item cannot fit into *any* remaining space, the box is rejected.