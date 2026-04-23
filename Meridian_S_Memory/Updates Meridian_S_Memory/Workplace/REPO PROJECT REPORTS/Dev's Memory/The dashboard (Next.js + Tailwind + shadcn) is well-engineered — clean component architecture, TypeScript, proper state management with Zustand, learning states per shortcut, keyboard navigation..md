---
modified: 2026-04-13T05:05:57+03:00
---
**The shortcut dashboard is technically stronger. Dev's Memory is stylistically stronger.**

The dashboard (Next.js + Tailwind + shadcn) is well-engineered — clean component architecture, TypeScript, proper state management with Zustand, learning states per shortcut, keyboard navigation. The keycap component is genuinely excellent. But the design language is generic — it's the standard Linear/Raycast dark theme that every developer tool uses right now. Nothing wrong with it, but nothing memorable either.

Dev's Memory has a real identity. The warm paper aesthetic, Caveat handwriting, ruled lines, the Game Boy widget — it feels like something someone actually made for themselves. That's rare and worth protecting.

**The verdict: Dev's Memory's aesthetic wins. The dashboard's architecture wins.**

For homogenisation I'd go in this direction — bring the dashboard's strengths into Dev's Memory's world, not the other way around:

- Adopt the keycap component for displaying keyboard shortcuts in Dev's Memory (it's genuinely better than plain text)
- Bring the learning state concept (new / learning / known / mastered) as an optional tag on commands
- Keep the paper aesthetic as the unified visual language across both
- The dashboard's dark mode could adopt Dev's Memory's warm dark ink palette instead of the cold blue-grey it currently uses

The shortcut dashboard would benefit from a "paper mode" option that brings it visually in line — warm background, Caveat for headings, the same ruled-line texture. The keycaps would look great on aged paper.

Want me to start the homogenisation work?