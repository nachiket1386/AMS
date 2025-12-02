# Design System Specification

## Overview

The Django Attendance Management System follows a strict, minimalist 4-color design system that ensures consistency, professionalism, and accessibility across all interfaces.

---

## Color Palette

### Primary Colors

#### Cream (#EFECE3)
- **Usage**: Background, base layer
- **Purpose**: Creates a calm, professional atmosphere
- **Psychology**: Warmth, approachability, reduces eye strain
- **Applications**:
  - Page backgrounds
  - Card backgrounds (secondary)
  - Input field backgrounds
  - Neutral spaces

#### Light Blue (#8FABD4)
- **Usage**: Secondary elements, accents
- **Purpose**: Soft visual hierarchy, non-critical actions
- **Psychology**: Trust, calmness, professionalism
- **Applications**:
  - Secondary buttons
  - Table headers
  - Borders
  - Hover states
  - Badge backgrounds (late/partial status)

#### Dark Blue (#4A70A9)
- **Usage**: Primary actions, emphasis
- **Purpose**: Draw attention to important actions
- **Psychology**: Authority, trust, stability
- **Applications**:
  - Primary buttons
  - Active navigation items
  - Status badges (present)
  - Icons (active state)
  - Links

#### Black (#000000)
- **Usage**: Text, borders, critical actions
- **Purpose**: Maximum contrast and readability
- **Psychology**: Clarity, seriousness, professionalism
- **Applications**:
  - Body text
  - Headings
  - Borders (strong emphasis)
  - Delete/critical buttons
  - Icons

### Color Usage Rules

**DO:**
- Use Cream for all backgrounds
- Use Dark Blue for primary CTAs
- Use Black for all text (with opacity variations)
- Use Light Blue for secondary elements

**DON'T:**
- Introduce new colors
- Use gradients (except subtle ones for avatars)
- Use color for decoration only
- Rely solely on color to convey information

---

## Typography

### Font Family
**Primary**: Inter (Google Fonts)
- **Weights Used**: 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold), 800 (Extra-Bold), 900 (Black)
- **Fallback**: sans-serif

### Type Scale

#### Display Text
```css
font-size: 3rem (48px)
font-weight: 800
letter-spacing: -0.025em
```
**Usage**: Hero sections, major headings

#### Title (Desktop)
```css
font-size: 2.25rem (36px)
font-weight: 800
```
**Usage**: Page titles on desktop

#### Title (Mobile)
```css
font-size: 1.125rem (18px)
font-weight: 700
```
**Usage**: Page titles on mobile

#### Card Number
```css
font-size: 1.875rem (30px)
font-weight: 700
```
**Usage**: Statistics, large numbers

#### Label
```css
font-size: 0.75rem (12px)
font-weight: 600
text-transform: uppercase
letter-spacing: 0.05em
```
**Usage**: Form labels, section headers

#### Body Text
```css
font-size: 0.875rem (14px) - 1rem (16px)
font-weight: 400-600
```
**Usage**: General content

### Typography Rules

**DO:**
- Use proper weight hierarchy
- Maintain consistent line heights
- Use uppercase sparingly (labels only)
- Ensure minimum 14px for body text

**DON'T:**
- Mix multiple font families
- Use italic (except for emphasis)
- Use underline (except for links)
- Use all caps for long text

---

## Spacing System

### Base Unit: 0.25rem (4px)

### Scale
- **0.5rem (8px)**: Tight spacing, icon gaps
- **0.75rem (12px)**: Small gaps
- **1rem (16px)**: Standard spacing
- **1.5rem (24px)**: Section spacing
- **2rem (32px)**: Large spacing
- **3rem (48px)**: Major section breaks

### Padding Standards
- **Buttons**: 0.75rem 1.5rem (12px 24px)
- **Cards**: 1.5rem (24px)
- **Inputs**: 0.75rem 1rem (12px 16px)
- **Mobile Cards**: 1.25rem (20px)

### Margin Standards
- **Between sections**: 2rem (32px)
- **Between cards**: 1rem (16px)
- **Between form fields**: 1.5rem (24px)

---

## Border Radius

### Standard Sizes
- **Buttons/Inputs**: 0.5rem (8px) - `rounded-standard`
- **Cards**: 1rem (16px) - `rounded-card`
- **Mobile Dock**: 2rem (32px) - `rounded-dock`
- **Badges**: 9999px (full round) - `rounded-full`

### Usage
- Consistent radius creates visual harmony
- Larger radius for larger elements
- Full round for pills and badges

---

## Components

### Buttons

#### Primary Button
```css
background: #4A70A9 (Dark Blue)
color: #EFECE3 (Cream)
padding: 0.75rem 1.5rem
border-radius: 0.5rem
font-weight: 600
transition: all 0.2s ease
```
**Hover**: Background → #000000 (Black)  
**Active**: Scale 0.95

#### Secondary Button
```css
background: #8FABD4 (Light Blue)
color: #000000 (Black)
padding: 0.75rem 1.5rem
border-radius: 0.5rem
font-weight: 600
transition: all 0.2s ease
```
**Hover**: Background → rgba(143, 171, 212, 0.8)  
**Active**: Scale 0.95

### Status Badges

#### Present (P)
```css
background: #4A70A9 (Dark Blue)
color: #EFECE3 (Cream)
padding: 0.25rem 0.75rem
border-radius: 9999px
font-size: 0.75rem
font-weight: 600
```

#### Late/Partial (-0.5, PH, WO)
```css
background: #8FABD4 (Light Blue)
color: #000000 (Black)
padding: 0.25rem 0.75rem
border-radius: 9999px
font-size: 0.75rem
font-weight: 600
```

#### Absent (A, -1)
```css
background: transparent
border: 2px solid #000000 (Black)
color: #000000 (Black)
padding: 0.25rem 0.75rem
border-radius: 9999px
font-size: 0.75rem
font-weight: 600
```

### Cards

#### Standard Card
```css
background: white
border: 1px solid #8FABD4 (Light Blue)
border-radius: 1rem
padding: 1.5rem
transition: all 0.2s ease
```
**Hover**: box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1)

#### Mobile Card
```css
background: white
border: 1px solid #8FABD4 (Light Blue)
border-radius: 1rem
padding: 1.25rem
```
**Active**: scale(0.98)

### Form Inputs

```css
width: 100%
padding: 0.75rem 1rem
background: #EFECE3 (Cream)
border: 1px solid #8FABD4 (Light Blue)
border-radius: 0.5rem
color: #000000 (Black)
font-size: 0.875rem
transition: all 0.2s ease
```
**Focus**:
- border-color: #4A70A9 (Dark Blue)
- box-shadow: 0 0 0 3px rgba(74, 112, 169, 0.1)

### Navigation

#### Desktop Nav Link
```css
padding: 0.5rem 1rem
color: #000000 (Black)
font-weight: 600
font-size: 0.875rem
border-radius: 0.5rem
transition: all 0.2s ease
```
**Hover**: background: rgba(143, 171, 212, 0.2)  
**Active**: 
- color: #4A70A9 (Dark Blue)
- background: rgba(74, 112, 169, 0.1)

#### Mobile Dock Item
```css
display: flex
flex-direction: column
align-items: center
padding: 0.75rem
color: #000000 (Black)
transition: all 0.2s ease
```
**Active**: color: #4A70A9 (Dark Blue)  
**Press**: scale(0.95)

---

## Shadows

### Elevation Levels

#### Level 1 (Subtle)
```css
box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1)
```
**Usage**: Cards, inputs

#### Level 2 (Medium)
```css
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1)
```
**Usage**: Hover states, dropdowns

#### Level 3 (High)
```css
box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.15)
```
**Usage**: Modals, important dropdowns

#### Level 4 (Floating)
```css
box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25)
```
**Usage**: Mobile dock, floating elements

---

## Animations & Transitions

### Standard Transition
```css
transition: all 0.2s ease
```
**Usage**: Most interactive elements

### Smooth Transition
```css
transition: all 0.3s ease-in-out
```
**Usage**: Mobile header, modals

### Quick Transition
```css
transition: all 0.15s ease
```
**Usage**: Dropdown items, small interactions

### Animations

#### Slide Down (Dropdown)
```css
@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

#### Scale Press
```css
active:scale-[0.98]
```
**Usage**: Mobile cards, buttons

---

## Responsive Design

### Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: ≥ 1024px

### Mobile-First Approach
1. Design for mobile first
2. Add complexity for larger screens
3. Progressive enhancement

### Responsive Patterns

#### Navigation
- **Mobile**: Bottom dock (floating)
- **Tablet**: Bottom dock (floating)
- **Desktop**: Top navbar (fixed)

#### Data Display
- **Mobile**: Card view (vertical stack)
- **Tablet**: Card view (vertical stack)
- **Desktop**: Table view (horizontal)

#### Typography
- **Mobile**: Smaller sizes (text-xl)
- **Tablet**: Medium sizes (text-2xl)
- **Desktop**: Full sizes (text-4xl)

---

## Accessibility

### Color Contrast
- **Text on Cream**: Black (#000000) - WCAG AAA
- **Text on Dark Blue**: Cream (#EFECE3) - WCAG AA
- **Text on Light Blue**: Black (#000000) - WCAG AA

### Touch Targets
- **Minimum size**: 44x44px
- **Spacing**: 8px between targets
- **Mobile buttons**: Full width or large

### Focus States
- Visible focus rings
- Keyboard navigation support
- Skip links (if needed)

---

## Icons

### Source
- Heroicons (outline style)
- SVG format
- Inline in HTML

### Sizing
- **Small**: 1rem (16px) - w-4 h-4
- **Medium**: 1.25rem (20px) - w-5 h-5
- **Large**: 1.5rem (24px) - w-6 h-6
- **Extra Large**: 2rem (32px) - w-8 h-8

### Colors
- Match text color
- Use currentColor for flexibility

---

## Best Practices

### DO
✅ Follow the 4-color system strictly  
✅ Use consistent spacing  
✅ Maintain proper hierarchy  
✅ Test on all breakpoints  
✅ Ensure accessibility  
✅ Use semantic HTML  
✅ Optimize for touch  
✅ Keep animations subtle  

### DON'T
❌ Add new colors  
❌ Use inconsistent spacing  
❌ Mix design patterns  
❌ Ignore mobile users  
❌ Rely on color alone  
❌ Use complex animations  
❌ Forget hover states  
❌ Skip accessibility  

---

## Design Checklist

Before shipping any UI:
- [ ] Uses only 4 approved colors
- [ ] Follows spacing system
- [ ] Has proper typography hierarchy
- [ ] Works on mobile, tablet, desktop
- [ ] Has hover/active/focus states
- [ ] Meets accessibility standards
- [ ] Uses consistent border radius
- [ ] Has smooth transitions
- [ ] Follows component patterns
- [ ] Tested on real devices

---

**Last Updated:** November 28, 2025  
**Version:** 1.0.0
