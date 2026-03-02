# SVG Animation Best Practices

## The Core Problem

CSS `transform-origin` uses **bounding-box relative values** like "center", "top center", "bottom center". These are calculated from the element's bounding box, NOT from a fixed coordinate point.

When SVG elements are drawn at arbitrary coordinates (like `cx="-10" cy="-18"`), the "center" of their bounding box is NOT where you visually expect it to be.

## The Golden Rule

**Every animated element needs its pivot point at local origin (0,0), positioned by a parent wrapper.**

## Wrong vs Right

### WRONG: Relying on bounding-box transform-origin

```svg
<!-- The eyes are at cy="-18", so "center" is NOT at the eye center -->
<g class="boy-eyes" style="transform-origin: center;">
  <ellipse cx="-10" cy="-18" rx="6" ry="5" fill="white"/>
  <ellipse cx="10" cy="-18" rx="6" ry="5" fill="white"/>
</g>
```

```css
.boy-eyes {
  animation: blink 4s ease-in-out infinite;
  transform-origin: center; /* Calculated from bounding box - WRONG */
}
```

**Result:** Eyes scale from the bounding box center, causing them to jump around.

### RIGHT: Pivot at origin with position wrapper

```svg
<!-- Position wrapper places eyes at correct location -->
<g transform="translate(0, -18)">
  <!-- Animation wrapper has eyes centered at origin -->
  <g class="boy-eyes">
    <ellipse cx="-10" cy="0" rx="6" ry="5" fill="white"/>
    <ellipse cx="10" cy="0" rx="6" ry="5" fill="white"/>
  </g>
</g>
```

```css
.boy-eyes {
  animation: blink 4s ease-in-out infinite;
  transform-origin: 0 0; /* Rotates/scales around local origin */
}
```

**Result:** Eyes scale around their actual center.

## The Three-Wrapper Pattern (For Elements with Base Rotation)

**CRITICAL**: CSS animations REPLACE transforms, they don't ADD to them!

This applies to **ALL transform types** - rotations, translations, and scales. If your CSS animation includes ANY `transform` property (even just `translateY(0)` in a fade-in animation), it will **REPLACE** any SVG `transform` attribute on the same element, causing the element to lose its position!

If your element needs a base rotation (like a raised arm), you need THREE wrappers:

```svg
<!-- 1. POSITION WRAPPER: Translates pivot point to world position -->
<g transform="translate(PIVOT_X, PIVOT_Y)">

  <!-- 2. BASE ROTATION: Static rotation for the element's resting position -->
  <g transform="rotate(BASE_ANGLE)">

    <!-- 3. ANIMATION WRAPPER: Has the animation class, oscillates around base -->
    <g class="animated-element">

      <!-- 4. GEOMETRY: Drawn with pivot at origin (0,0) -->

    </g>
  </g>
</g>
```

### Why Three Wrappers?

If you put `transform="rotate(-60)"` on the animation wrapper:
```svg
<g class="arm-wave" transform="rotate(-60)">  <!-- WRONG! -->
```

The CSS animation will REPLACE that transform:
```css
@keyframes wave {
  0% { transform: rotate(-20deg); }  /* Replaces -60 with -20! */
  50% { transform: rotate(20deg); }   /* Replaces -60 with 20! */
}
```

Result: Arm drops from raised (-60) to animation values (-20 to 20).

### Correct: Separate Base and Animation

```svg
<g transform="rotate(-60)">         <!-- Base: arm raised -->
  <g class="arm-wave">              <!-- Animation adds oscillation -->
```

Now the animation's -20 to 20 degrees is ADDED to the parent's -60:
- Effective range: -80 to -40 degrees (arm stays raised, just waves)

## The Two-Wrapper Pattern (For Elements without Base Rotation)

For simple animations where the resting position is neutral:

```svg
<!-- 1. POSITION WRAPPER: Translates pivot point to correct world position -->
<g transform="translate(PIVOT_X, PIVOT_Y)">

  <!-- 2. ANIMATION WRAPPER: Has the animation class, pivot at (0,0) -->
  <g class="animated-element">

    <!-- 3. GEOMETRY: Drawn relative to origin as pivot -->
    <rect x="-width/2" y="0" .../>  <!-- centered on pivot -->

  </g>
</g>
```

## Common Animation Types and Their Pivots

### Rotating Limbs (arms, legs)
- **Pivot:** Joint (shoulder, hip, elbow, knee)
- **Draw from:** Origin extends outward
- **Example:** Arm from shoulder: `rect x="-7" y="0"` (centered horizontally, extends down)

### Scaling Elements (eyes blinking, mouth opening)
- **Pivot:** Visual center of the element
- **Draw from:** Centered on origin
- **Example:** Eyes: `ellipse cx="0" cy="0"` per eye, or group centered

### Rotating Head (looking around, nodding)
- **Pivot:** Neck base (where head connects to body)
- **Draw from:** Head extends upward from origin
- **Example:** Head group with neck at y=0, head at negative y

### Breathing/Pulsing (torso, whole body)
- **Pivot:** Base (feet for body, bottom for torso)
- **Draw from:** Element extends upward from origin
- **Example:** Torso with bottom at y=0

## Checklist Before Animating

1. [ ] Identify the pivot point for this animation
2. [ ] Create position wrapper with `transform="translate(pivot_x, pivot_y)"`
3. [ ] Create animation wrapper inside with the CSS class
4. [ ] Redraw geometry so pivot point is at local (0, 0)
5. [ ] Set CSS `transform-origin: 0 0`

## Common Mistakes

### Mistake 1: Using "center" or "top center" transform-origin
These are bounding-box relative and will calculate wrong pivot points.

**Fix:** Always use `transform-origin: 0 0` with properly positioned geometry.

### Mistake 2: Drawing geometry at world coordinates inside animated groups
If your arm rect is at `x="-45" y="-20"`, the origin (0,0) is nowhere near the shoulder.

**Fix:** Redraw so the joint is at origin: `x="-7" y="0"` for a centered arm extending down.

### Mistake 3: Animating nested elements without considering parent transforms
When the head rotates, eyes/mouth inside should stay attached because they're children.
But if eyes/mouth have their OWN animations, those animations compound.

**Fix:** Ensure child animations also use proper pivot structure, or make them relative to parent.

### Mistake 4: Forgetting the position wrapper
Just changing geometry to be at origin without a position wrapper moves everything to (0,0).

**Fix:** Always pair the geometry restructure with a position wrapper.

### Mistake 5: Fade-in animations with translateY on positioned elements
This is a very common bug! If you have:
```svg
<g id="my-box" class="fade-in" transform="translate(300, 200)">
```
```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeIn 0.5s ease-out forwards; }
```

The CSS `transform: translateY(0)` will **REPLACE** the SVG `transform="translate(300, 200)"`, causing the element to end up at (0, 0) instead of (300, 200)!

**Fix:** Use separate position wrapper and animation wrapper:
```svg
<g transform="translate(300, 200)">       <!-- Position: NOT animated -->
  <g id="my-box" class="fade-in">         <!-- Animation: NO position transform -->
    <!-- content -->
  </g>
</g>
```

**Alternative fix:** Use opacity-only animations if you don't need the slide effect:
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Testing Animations

1. Open the SVG in a browser
2. Watch for elements that "jump" at animation start
3. Watch for elements that orbit/swing around wrong points
4. If something jumps: the pivot isn't where you think it is
5. If something detaches: the geometry isn't properly nested

## Example: Complete Character Arm

```svg
<!-- Character positioned in scene -->
<g transform="translate(480, 300)">

  <!-- Body (static or breathing animation) -->
  <rect x="-22" y="20" width="44" height="55" fill="orange"/>

  <!-- LEFT ARM: shoulder at (-22, 25) relative to character -->
  <g transform="translate(-22, 25)">
    <!-- Animation wrapper - arm waves from shoulder -->
    <g class="arm-wave">
      <!-- Arm geometry: shoulder at origin, extends down -->
      <rect x="-7" y="0" width="15" height="45" fill="peachpuff"/>
      <!-- Hand at end of arm -->
      <circle cx="0" cy="50" r="8" fill="peachpuff"/>
    </g>
  </g>

</g>
```

```css
.arm-wave {
  animation: wave 1s ease-in-out infinite;
  transform-origin: 0 0; /* Shoulder is at origin */
}

@keyframes wave {
  0%, 100% { transform: rotate(-10deg); }
  50% { transform: rotate(10deg); }
}
```
