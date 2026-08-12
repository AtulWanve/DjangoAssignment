# Reference Information

## Assignment Requirements
- Build a Django-based system to recommend the most suitable shipping box for an order.
- Document AI usage extensively (prompts, accepted/rejected output, mistakes, verification).
- Submit: GitHub link, README, AI_USAGE.md, chat transcript, reflection ("What did you learn?"), Test Cases, and Test Output.

## Key Domain Concepts & Terminology
- **Product**: An item to be shipped, defined by Length, Width, Height, and Weight.
- **Box**: A shipping container, defined by Internal Length, Internal Width, Internal Height, Max Weight Capacity, and Cost.
- **Order**: A collection of Products that need to be packed into a single Box.
- **Space**: A rectangular void of empty air inside a Box.
- **Guillotine Split**: An algorithmic concept where placing a Product into a Space slices the remaining empty air into up to 3 smaller, perfectly rectangular Spaces.

## Important Decisions Made
1. **No Order Persistence**: The API will be stateless for orders (accepting a payload of product IDs) to keep the architecture minimal, unless requested otherwise.
2. **Dimension-Only Tracking**: The packing algorithm checks if items fit by subdividing empty spaces based on dimensions, avoiding the complexity of 3D coordinate collision detection.
3. **Cost Optimization**: If multiple boxes fit the order, the system will always recommend the one with the lowest cost.

## Documentation Pointers
- Implementation Rules: `/CLAUDE.md`
- Current Status & State: `/CONTEXT.md`
- Algorithm specifics: `/boxes/CONTEXT.md`