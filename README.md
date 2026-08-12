# AI-Assisted Box Selection System

## Overview
This is a small Django-based system designed to recommend the most suitable shipping box for a given e-commerce order. It takes a list of products, calculates whether they physically fit into available boxes, respects weight limits, and recommends the cheapest box that successfully fits the order.

## Packing Approach
The core packing logic uses a **Greedy 3D Space Partitioning (Guillotine Split)** algorithm. 
- It tracks the dimensions of available "empty spaces" inside a box.
- When an item is packed into a space, the remaining empty air is sliced into up to 3 new smaller rectangular spaces (Top, Right, Front).
- The algorithm tests all 6 possible 3D rotations for every item.
- Boxes are sorted by cost (cheapest first). The algorithm returns the first box that successfully fits all items.

### Important Assumptions and Limitations
- **Greedy Heuristic:** This is a greedy heuristic, not a mathematically optimal 3D bin packing solver (which is NP-hard).
- **Dimension-Only Tracking:** The algorithm tracks the width, height, and length of empty spaces, but not their explicit X/Y/Z coordinates. Because it doesn't know where spaces are located relative to each other, it cannot merge adjacent empty spaces (Space Fragmentation). This can result in "False Negatives" (the algorithm claims a box cannot fit an order, even if a human might be able to perfectly arrange it). 
- **No Overlaps / False Positives:** While it may generate False Negatives, it mathematically guarantees zero False Positives. If it says an order fits, it physically fits.
- **No Instructions:** The API recommends a box but does not output a 3D coordinate diagram of *how* the warehouse worker should pack the items.
- **Rigidity:** Assumes all products are rigid rectangular prisms.

## Setup and Running

1. **Clone the repository.**
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```
5. **Create a Superuser (Optional, to manage Boxes/Products via Django Admin):**
   ```bash
   python manage.py createsuperuser
   ```
6. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

## API Usage

### `POST /api/recommend-box/`

Expects a JSON payload containing a list of `product_ids` that constitute the order.

**Request:**
```json
{
    "product_ids": [1, 2, 2, 5]
}
```

**Success Response (200 OK):**
```json
{
    "recommended_box_id": 3,
    "box_name": "Medium Box",
    "cost": "2.50",
    "status": "success"
}
```

**Failure Response (400 Bad Request):**
```json
{
    "error": "No available box can fit this order.",
    "status": "failed"
}
```

## Running Tests
The project includes a full test suite verifying various packing and API scenarios. The important scenarios covered by our tests include:
- **Exact fit:** Products that perfectly match the internal dimensions of a box.
- **Product rotation:** Testing all 3D rotations to ensure an item fits regardless of its initial orientation.
- **Weight limit:** Ensuring boxes are not recommended if the total order weight exceeds the box's maximum weight limit.
- **Dimension limit:** Validating that individual items strictly adhere to the physical dimensions of the box.
- **Multiple products:** Packing multiple distinct items into the same box using the 3D space partitioning algorithm.
- **No suitable box:** Correctly identifying when an order is too large or heavy for any available box.
- **API validation:** Ensuring the API handles missing payloads, invalid IDs, or non-JSON requests correctly.
- **Repeated product IDs:** Handling orders that contain multiple units of the same product.

Run the tests using:
```bash
python manage.py test
```
