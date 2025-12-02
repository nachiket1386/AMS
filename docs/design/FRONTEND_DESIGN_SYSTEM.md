# Frontend Design System Documentation
# Attendance Management System

## Table of Contents
1. [Color Palette](#color-palette)
2. [Typography](#typography)
3. [Spacing & Layout](#spacing--layout)
4. [Responsive Breakpoints](#responsive-breakpoints)
5. [Component Library](#component-library)
6. [Navigation Patterns](#navigation-patterns)
7. [Form Elements](#form-elements)
8. [Tables & Data Display](#tables--data-display)
9. [Cards & Containers](#cards--containers)
10. [Buttons & Actions](#buttons--actions)
11. [Icons & SVG](#icons--svg)
12. [Animation & Transitions](#animation--transitions)
13. [Accessibility](#accessibility)

---

## Color Palette

### Primary Colors
```css
Cream (Background):    #EFECE3
Light Blue (Secondary): #8FABD4
Dark Blue (Primary):    #4A70A9
Black (Text):          #000000
```

### Color Usage Guidelines

**Cream (#EFECE3)**
- Main background color for entire application
- Card backgrounds
- Input field backgrounds
- Creates warm, soft aesthetic

**Light Blue (#8FABD4)**
- Navigation bars (desktop header, mobile bottom nav)
- Table headers
- Secondary buttons
- Borders and dividers
- Hover states with opacity variations (e.g., bg-light-blue/40)

**Dark Blue (#4A70A9)**
- Primary action buttons
- Active navigation states
- Icons in headers
- Focus rings
- Status badges (Present status)
- Links and interactive elements

**Black (#000000)**
- Primary text color
- Secondary action buttons (delete, critical actions)
- Borders for emphasis
- Status badges (Absent status)

### Opacity Variations
- `text-black/70` - Secondary text (70% opacity)
- `text-black/60` - Tertiary text (60% opacity)
- `text-black/80` - Labels (80% opacity)
- `bg-light-blue/40` - Hover states (40% opacity)
- `bg-light-blue/30` - Subtle backgrounds (30% opacity)
- `bg-cream/50` - Semi-transparent overlays (50% opacity)

---

## Typography

### Font Family
**Inter** - Google Fonts
- Weights: 400 (Regular), 500 (Medium), 600 (Semi-Bold), 700 (Bold), 800 (Extra-Bold)
- Applied globally via Tailwind config
- Font smoothing: antialiased (webkit), grayscale (moz)

### Font Sizes & Hierarchy

**Headings**
- H1 (Page Titles): `text-2xl md:text-4xl` (24px mobile, 36px desktop)
- H2 (Section Titles): `text-xl` (20px)
- H3 (Card Titles): `text-lg` (18px)

**Body Text**
- Regular: `text-sm` (14px)
- Small: `text-xs` (12px)
- Tiny: `text-xs` (11px for dense tables)

**Font Weights**
- Extra Bold: `font-extrabold` (800) - Page titles
- Bold: `font-bold` (700) - Section headers, important data
- Semi-Bold: `font-semibold` (600) - Labels, buttons
- Medium: `font-medium` (500) - Secondary text
- Regular: `font-normal` (400) - Body text

---

## Spacing & Layout

### Container Widths
- Max width: `max-w-7xl` (1280px)
- Centered: `mx-auto`
- Horizontal padding: `px-4 sm:px-6 lg:px-8`

### Spacing Scale (Tailwind)
- `gap-2` - 8px (tight spacing)
- `gap-3` - 12px (compact spacing)
- `gap-4` - 16px (default spacing)
- `gap-6` - 24px (comfortable spacing)
- `gap-8` - 32px (section spacing)

### Padding
- Cards: `p-4 md:p-6` (16px mobile, 24px desktop)
- Large cards: `p-6 md:p-8` (24px mobile, 32px desktop)
- Buttons: `px-4 py-2` (horizontal 16px, vertical 8px)
- Large buttons: `px-6 py-3` (horizontal 24px, vertical 12px)
- Table cells: `px-2 py-2` (8px all sides)

### Margins
- Section spacing: `space-y-8` (32px vertical)
- Card spacing: `space-y-4` (16px vertical)
- Element spacing: `mt-1`, `mt-2`, `mt-4` (4px, 8px, 16px)

---

## Responsive Breakpoints

### Tailwind Breakpoints
```css
sm:  640px  (Small tablets)
md:  768px  (Tablets)
lg:  1024px (Desktops)
xl:  1280px (Large desktops)
2xl: 1536px (Extra large)
```

### Mobile-First Approach
Base styles target mobile (<768px), then enhanced for larger screens

### Key Responsive Patterns

**Navigation**
- Mobile (<768px): Bottom navigation bar (fixed)
- Desktop (≥768px): Top navigation bar (fixed)

**Layout**
- Mobile: Single column, stacked elements
- Tablet (≥768px): 2-column grids
- Desktop (≥1024px): 3-column grids

**Typography**
- Mobile: `text-2xl` (24px) for H1
- Desktop: `text-4xl` (36px) for H1

**Spacing**
- Mobile: `p-4` (16px padding)
- Desktop: `p-6` or `p-8` (24px or 32px padding)

**Data Display**
- Mobile: Card-based layout
- Desktop: Table layout

---

## Component Library

### 1. Navigation Components

#### Desktop Header
```html
Position: Fixed top
Height: 80px (h-20)
Background: Light Blue (#8FABD4)
Border: Bottom border (Dark Blue)
Z-index: 50
Display: Hidden on mobile (hidden md:block)

Components:
- Logo icon (Dark Blue background, Cream text)
- App title (text-xl font-bold)
- Navigation links (horizontal)
- User avatar (circular, Dark Blue background)
- Logout button (circular hover effect)
```

#### Mobile Bottom Navigation
```html
Position: Fixed bottom
Height: 64px (h-16)
Background: Light Blue (#8FABD4)
Border: Top border (Dark Blue)
Z-index: 50
Display: Visible on mobile only (md:hidden)

Layout: Flex, evenly distributed (justify-around)
Items: Icon + Label (vertical stack)
Active state: Dark Blue color
Inactive state: Black color
```

#### Navigation Link States
- Default: `text-black hover:bg-black/10`
- Active: `text-dark-blue font-bold`
- Transition: `transition-colors duration-200`
- Padding: `padding: 0.5rem 1rem`
- Border radius: `rounded-lg`

### 2. Card Components

#### Standard Card
```html
Background: Cream (#EFECE3)
Border: 1px solid Light Blue
Border radius: rounded-2xl (16px)
Padding: p-4 md:p-6 (16px mobile, 24px desktop)
Shadow: None (flat design)
```

#### Large Card
```html
Background: Cream (#EFECE3)
Border: 1px solid Light Blue
Border radius: rounded-2xl (16px)
Padding: p-6 md:p-8 (24px mobile, 32px desktop)
```

#### Info Card (Sidebar)
```html
Background: Light Blue (#8FABD4)
Border: 1px solid Dark Blue (50% opacity)
Border radius: rounded-2xl (16px)
Padding: p-6 (24px)
Text color: Black
```

#### Mobile Data Card
```html
Background: Cream (#EFECE3)
Border: 1px solid Light Blue
Border radius: rounded-2xl (16px)
Padding: p-4 (16px)

Structure:
- Header: Name + Status badge (flex justify-between)
- Body: Key-value pairs (space-y-3)
- Time grid: 2x3 grid with Light Blue background
- Actions: Full-width buttons (flex gap-2)
```

### 3. Button Components

#### Primary Button
```html
Background: Dark Blue (#4A70A9)
Text: Cream (#EFECE3)
Padding: px-4 py-2 (small) or px-6 py-3 (large)
Border radius: rounded-xl (12px)
Font: font-semibold
Hover: bg-black
Transition: transition-all duration-300
Focus: focus:ring-4 focus:ring-dark-blue/50
```

#### Secondary Button
```html
Background: Light Blue (#8FABD4)
Text: Black (#000000)
Padding: px-4 py-2
Border radius: rounded-xl (12px)
Font: font-semibold
Hover: bg-light-blue/70 (70% opacity)
Transition: transition
```

#### Danger Button
```html
Background: Black (#000000)
Text: Cream (#EFECE3)
Padding: px-4 py-2
Border radius: rounded-xl (12px) or rounded-lg (8px)
Font: font-semibold
Hover: opacity-80
Transition: transition
```

#### Icon Button (Small)
```html
Size: p-1 (4px padding)
Background: Dark Blue or Black
Text: Cream
Border radius: rounded (4px)
Icon size: w-3 h-3 (12px)
Hover: bg-black (for Dark Blue) or opacity-80 (for Black)
```

#### Icon Button (Large - Mobile Touch)
```html
Size: p-2 (8px padding)
Min size: 44x44px (touch target)
Background: Dark Blue or Black
Text: Cream
Border radius: rounded
Icon size: w-4 h-4 (16px)
Display: flex items-center justify-center
```

### 4. Form Elements

#### Text Input
```html
Background: Cream (#EFECE3)
Border: 1px solid Light Blue
Border radius: rounded-xl (12px)
Padding: px-3 py-2 (12px horizontal, 8px vertical)
Font size: text-sm (14px)
Text color: Black
Placeholder: text-black/50 (50% opacity)
Focus: ring-2 ring-dark-blue border-transparent
Transition: transition
```

#### Select Dropdown
```html
Same styling as Text Input
Additional: Dropdown arrow (browser default)
```

#### Date Input
```html
Same styling as Text Input
Type: date
Browser native date picker
```

#### File Upload (Drag & Drop)
```html
Border: 2px dashed Light Blue
Border radius: rounded-2xl (16px)
Padding: px-6 pt-5 pb-6
Hover: border-dark-blue
Transition: transition-colors
Center aligned content
Icon: Upload cloud (h-12 w-12, text-black/40)
```

#### Label
```html
Font size: text-sm (14px)
Font weight: font-semibold
Color: text-black/80 (80% opacity)
Margin: mb-1 (4px bottom)
Display: block
```

### 5. Status Badges

#### Present (P)
```html
Background: Dark Blue (#4A70A9)
Text: Cream (#EFECE3)
Padding: px-3 py-1 (small) or px-2 py-1 (table)
Border radius: rounded-lg (8px) or rounded (4px)
Font: font-semibold text-xs or text-sm
```

#### Absent (A)
```html
Background: Cream (#EFECE3)
Text: Black (#000000)
Border: 1px solid Black
Padding: px-3 py-1 (small) or px-2 py-1 (table)
Border radius: rounded-lg (8px) or rounded (4px)
Font: font-semibold text-xs or text-sm
```

#### Other Status (PH, -0.5, -1)
```html
Background: Light Blue (#8FABD4)
Text: Black (#000000)
Padding: px-3 py-1 (small) or px-2 py-1 (table)
Border radius: rounded-lg (8px) or rounded (4px)
Font: font-semibold text-xs or text-sm
```

### 6. Upload Log Badges

#### Success Count
```html
Background: Dark Blue/10 (10% opacity)
Text: Dark Blue
Padding: px-2 py-1
Border radius: rounded-lg (8px)
Font: font-semibold text-sm
Icon: ✓
```

#### Updated Count
```html
Background: Light Blue/30 (30% opacity)
Text: Black
Padding: px-2 py-1
Border radius: rounded-lg (8px)
Font: font-semibold text-sm
Icon: ↻
```

#### Error Count
```html
Background: Black/10 (10% opacity)
Text: Black
Padding: px-2 py-1
Border radius: rounded-lg (8px)
Font: font-semibold text-sm
Icon: ✗
```

---

## Tables & Data Display

### Desktop Table

#### Table Container
```html
Background: Cream (#EFECE3)
Border: 1px solid Light Blue
Border radius: rounded-2xl (16px)
Padding: p-0 (no padding, table fills container)
Overflow: overflow-hidden
Display: hidden md:block (desktop only)
```

#### Table Element
```html
Width: w-full
Text size: text-xs (12px)
Text align: text-left
Text color: text-black
Layout: table-fixed (fixed column widths)
```

#### Table Header (thead)
```html
Background: Light Blue (#8FABD4)
Text: Black, uppercase
Font size: text-xs (12px)
```

#### Table Header Cell (th)
```html
Padding: px-2 py-2 (8px all sides)
Width: Varies by column (w-16, w-20, w-24, w-32)
Scope: col (for accessibility)
```

#### Table Body Row (tr)
```html
Background: Cream (#EFECE3)
Border: Bottom border (Light Blue)
Hover: bg-light-blue/40 (40% opacity)
Transition: transition-colors duration-200
```

#### Table Data Cell (td)
```html
Padding: px-2 py-2 (8px all sides)
Font size: text-xs (12px)
Text truncate: truncate (for long text)
Font weight: font-semibold (for EP NO, EP NAME)
```

#### Column Widths
```
EP NO:          w-24 (96px)
EP NAME:        w-32 (128px)
DATE:           w-24 (96px)
SHIFT:          w-16 (64px)
IN/OUT:         w-16 (64px each)
IN(2)/OUT(2):   w-16 (64px each)
IN(3)/OUT(3):   w-16 (64px each)
HOURS:          w-16 (64px)
OVERSTAY:       w-20 (80px)
STATUS:         w-20 (80px)
OVERTIME:       w-20 (80px)
OT TO MANDAYS:  w-24 (96px)
ACTIONS:        w-24 (96px)
```

### Mobile Card Layout

#### Card Structure
```html
Display: md:hidden (mobile only)
Layout: space-y-4 (16px vertical spacing)
```

#### Card Header
```html
Layout: flex justify-between items-start
Gap: mb-4 (16px bottom margin)
Left: Name (font-bold) + EP NO (text-sm text-black/60)
Right: Status badge
```

#### Card Body
```html
Layout: space-y-3 (12px vertical spacing)
Font size: text-sm (14px)
Key-value pairs: flex justify-between
```

#### Time Grid Section
```html
Background: Light Blue/30 (30% opacity)
Border radius: rounded-lg (8px)
Padding: p-3 (12px)
Grid: grid-cols-2 gap-2 (2 columns, 8px gap)
Font size: text-xs (12px)
```

#### Action Buttons Section
```html
Margin: mt-4 (16px top)
Layout: flex gap-2 (8px gap)
Buttons: flex-1 (equal width)
```

---

## Pagination

### Pagination Container
```html
Layout: flex justify-center items-center gap-2
Spacing: 8px between elements
```

### Pagination Button
```html
Background: Cream (#EFECE3)
Border: 1px solid Light Blue
Text: Black
Padding: px-4 py-2 (16px horizontal, 8px vertical)
Border radius: rounded-lg (8px)
Hover: bg-light-blue
Transition: transition
```

### Current Page Indicator
```html
Background: Dark Blue (#4A70A9)
Text: Cream (#EFECE3)
Padding: px-4 py-2
Border radius: rounded-lg (8px)
Font: font-semibold
```

---

## Icons & SVG

### Icon Library
**Source**: Heroicons (inline SVG)
**Style**: Outline (stroke-based)

### Icon Sizes
- Small: `w-3 h-3` (12px) - Table actions
- Medium: `w-4 h-4` (16px) - Buttons, mobile actions
- Default: `w-5 h-5` (20px) - Navigation, standard buttons
- Large: `w-6 h-6` (24px) - Section headers, mobile nav
- Extra Large: `w-7 h-7` (28px) - Dashboard stat cards
- Huge: `w-8 h-8` (32px) - Page titles
- Upload: `w-12 h-12` (48px) - File upload area

### Icon Colors
- Primary: `text-dark-blue` or `text-cream` (on dark backgrounds)
- Secondary: `text-black` or `text-black/40` (subtle)
- Navigation active: `text-dark-blue`
- Navigation inactive: `text-black`

### Common Icons Used
- Dashboard: Home icon
- Upload: Cloud upload icon
- Data: Clipboard icon
- Logs: Book open icon
- Users: User group icon
- Calendar: Calendar icon
- Edit: Pencil icon
- Delete: Trash icon
- Download: Download icon
- Info: Information circle icon
- Logout: Logout arrow icon

### SVG Properties
```html
fill="none"
stroke="currentColor"
viewBox="0 0 24 24"
stroke-linecap="round"
stroke-linejoin="round"
stroke-width="2"
```

---

## Animation & Transitions

### Transition Classes
```css
transition                    /* All properties, 150ms */
transition-colors             /* Color properties only */
transition-all duration-300   /* All properties, 300ms */
transition-opacity duration-300 /* Opacity only, 300ms */
```

### Hover Effects

**Buttons**
- Primary: `hover:bg-black`
- Secondary: `hover:bg-light-blue/70`
- Danger: `hover:opacity-80`
- Icon: `hover:bg-black` or `hover:opacity-80`

**Navigation Links**
- Desktop: `hover:bg-black/10`
- Mobile: No hover (touch interface)

**Table Rows**
- `hover:bg-light-blue/40`

**Cards**
- No hover effect (static)

**Inputs**
- Border: `hover:border-dark-blue` (file upload)

### Focus States
```css
focus:outline-none
focus:ring-2 focus:ring-dark-blue
focus:border-transparent
focus:ring-4 focus:ring-dark-blue/50 (buttons)
```

### Loading States
```html
Button disabled: opacity-75 cursor-not-allowed
Spinner: animate-spin (Tailwind animation)
```

---

## Accessibility

### Touch Targets (Mobile)
- Minimum size: 44x44px
- Applied to: Action buttons in tables, mobile navigation
- Implementation: `min-width: 44px; min-height: 44px;`

### Semantic HTML
- `<header>` for navigation
- `<main>` for content
- `<nav>` for navigation menus
- `<table>` with proper `<thead>`, `<tbody>`, `<th>`, `<td>`
- `<form>` for all forms
- `<label>` for all inputs

### ARIA Attributes
- `scope="col"` on table headers
- `title` attribute on icon-only buttons
- `aria-label` where needed

### Keyboard Navigation
- All interactive elements focusable
- Tab order follows visual order
- Focus indicators visible (ring-2 ring-dark-blue)

### Color Contrast
- Text on Cream: Black (#000000) - High contrast
- Text on Light Blue: Black (#000000) - Good contrast
- Text on Dark Blue: Cream (#EFECE3) - High contrast
- All combinations meet WCAG AA standards (4.5:1 minimum)

### Screen Reader Support
- Proper heading hierarchy (H1 → H2 → H3)
- Descriptive link text
- Form labels associated with inputs
- Table headers properly scoped

---

## Message/Alert Components

### Success Message
```html
Background: Cream (#EFECE3)
Border: Left border (4px, Dark Blue)
Padding: p-4 (16px)
Border radius: rounded-lg (8px)
Text: Black
```

### Error Message
```html
Background: Cream (#EFECE3)
Border: Left border (4px, Black)
Padding: p-4 (16px)
Border radius: rounded-lg (8px)
Text: Black
```

### Info Message
```html
Background: Cream (#EFECE3)
Border: Left border (4px, Light Blue)
Padding: p-4 (16px)
Border radius: rounded-lg (8px)
Text: Black
```

---

## User Avatar Component

### Avatar Circle
```html
Size: w-8 h-8 (32px)
Background: Dark Blue (#4A70A9)
Shape: rounded-full
Text: Cream (#EFECE3)
Font: font-bold text-sm (14px)
Alignment: flex items-center justify-center
Content: First letter of username (uppercase)
```

### Avatar with Info (Desktop)
```html
Container: flex items-center gap-0.5rem
Background: Cream/50 (50% opacity)
Shape: rounded-full
Padding: 0.5rem (8px)

Components:
- Avatar circle (left)
- User info (right, hidden on small screens)
  - Username: text-sm font-semibold
  - Role: text-xs text-black/70
```

---

## Grid Layouts

### Dashboard Stats Grid
```html
Mobile: grid-cols-1 (single column)
Tablet: grid-cols-2 (2 columns)
Desktop: grid-cols-3 (3 columns)
Gap: gap-6 (24px)
```

### Quick Actions Grid
```html
Base: grid-cols-2 (2 columns)
Large: xl:grid-cols-3 (3 columns for root/admin)
Gap: gap-4 (16px)
```

### Filter Form Grid
```html
Mobile: grid-cols-2 (date inputs)
Desktop: Horizontal flex with wrapping
Gap: gap-3 (12px)
```

### Upload Page Grid
```html
Mobile: grid-cols-1 (single column)
Desktop: lg:grid-cols-3 (3 columns)
Gap: gap-8 (32px)
Main content: lg:col-span-2 (2/3 width)
Sidebar: 1 column (1/3 width)
```

---

## Border Radius Scale

```css
rounded       4px   (small elements, badges)
rounded-lg    8px   (buttons, small cards)
rounded-xl    12px  (inputs, medium buttons)
rounded-2xl   16px  (cards, containers)
rounded-full  50%   (circles, avatars)
```

---

## Z-Index Layers

```css
z-10   Scroll indicators
z-20   Sticky table columns (data cells)
z-30   Sticky table headers
z-31   Sticky table headers + columns intersection
z-50   Navigation (header, bottom nav)
```

---

## Page-Specific Patterns

### Login Page
- Centered layout
- Single card design
- Logo/branding at top
- Form in center
- Minimal distractions

### Dashboard Page
- Stats cards at top (3-column grid)
- Quick actions section
- Company info sidebar
- Recent activity feed
- Mobile: Stacked layout with greeting header

### Upload Page
- Two-column layout (2/3 main, 1/3 sidebar)
- Drag-and-drop file upload
- Format requirements sidebar (Light Blue background)
- Recent uploads list below
- Mobile: Stacked layout

### Data List Page (Attendance)
- Filters at top (collapsible on mobile)
- Record count display
- Mobile: Card-based layout
- Desktop: Table layout
- Pagination at bottom
- Export button in filters section

### User Management Page
- List of users with role badges
- Action buttons (Edit, Delete)
- Create new user button
- Role-based visibility

---

## Responsive Design Patterns

### Mobile (<768px)
- Bottom navigation (fixed)
- Stacked layouts (single column)
- Card-based data display
- Full-width buttons
- Larger touch targets (44x44px)
- Reduced padding (p-4 instead of p-6)
- Smaller font sizes
- Hidden secondary text
- Collapsible filters

### Tablet (768px - 1024px)
- Top navigation (fixed)
- 2-column grids
- Table layout for data
- Medium padding (p-6)
- Standard font sizes
- Visible secondary text

### Desktop (≥1024px)
- Top navigation (fixed)
- 3-column grids
- Table layout for data
- Larger padding (p-8)
- Larger font sizes
- Full feature visibility
- Hover effects enabled

---

## Performance Optimizations

### Font Loading
- Preconnect to Google Fonts
- Font-display: swap
- Limited font weights (400, 500, 600, 700, 800)

### CSS
- Tailwind CDN for development
- Purged CSS for production
- Minimal custom CSS
- Utility-first approach

### Images
- SVG icons (inline, no HTTP requests)
- No raster images in UI
- Icon reuse across components

### JavaScript
- Minimal JavaScript usage
- Vanilla JS (no frameworks for simple interactions)
- Event delegation where possible
- No heavy libraries

---

## Design Principles

### 1. Consistency
- Uniform spacing scale
- Consistent color usage
- Predictable component behavior
- Standardized border radius
- Unified typography

### 2. Clarity
- High contrast text
- Clear visual hierarchy
- Obvious interactive elements
- Descriptive labels
- Meaningful icons

### 3. Simplicity
- Minimal design elements
- Flat design (no shadows)
- Clean borders
- Ample whitespace
- Focused content

### 4. Responsiveness
- Mobile-first approach
- Fluid layouts
- Adaptive components
- Touch-friendly on mobile
- Optimized for all screen sizes

### 5. Accessibility
- WCAG AA compliant
- Keyboard navigable
- Screen reader friendly
- Sufficient touch targets
- Clear focus indicators

---

## Component States

### Button States
1. **Default**: Base styling
2. **Hover**: Color change (desktop only)
3. **Focus**: Ring indicator
4. **Active**: Pressed state
5. **Disabled**: Reduced opacity, no pointer events
6. **Loading**: Spinner, disabled interaction

### Input States
1. **Default**: Base styling
2. **Focus**: Ring indicator, border change
3. **Error**: Red border (if implemented)
4. **Disabled**: Reduced opacity
5. **Filled**: Contains value

### Navigation States
1. **Default**: Base styling
2. **Hover**: Background change (desktop)
3. **Active**: Bold text, Dark Blue color
4. **Focus**: Ring indicator

### Table Row States
1. **Default**: Cream background
2. **Hover**: Light Blue background (40% opacity)
3. **Selected**: Not implemented

---

## Browser Support

### Supported Browsers
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile Safari (iOS 14+)
- Chrome Android (latest)

### CSS Features Used
- Flexbox
- Grid
- Custom properties (via Tailwind)
- Transitions
- Transforms
- Border radius
- Opacity

### Fallbacks
- System fonts if Inter fails to load
- Graceful degradation for older browsers
- Progressive enhancement approach

---

## Code Examples

### Example: Primary Button
```html
<button class="px-6 py-3 text-sm font-semibold text-cream bg-dark-blue rounded-xl hover:bg-black transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-dark-blue/50">
    Upload File
</button>
```

### Example: Card Component
```html
<div class="bg-cream border border-light-blue rounded-2xl p-6 md:p-8">
    <h2 class="text-xl font-bold text-black mb-4">Card Title</h2>
    <p class="text-sm text-black/70">Card content goes here.</p>
</div>
```

### Example: Input Field
```html
<div>
    <label class="text-sm font-semibold text-black/80 mb-1 block">
        Email Address
    </label>
    <input 
        type="email" 
        class="w-full px-3 py-2 bg-cream border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black placeholder:text-black/50 text-sm"
        placeholder="Enter your email"
    >
</div>
```

### Example: Status Badge
```html
<!-- Present -->
<span class="px-3 py-1 rounded-lg text-sm font-semibold bg-dark-blue text-cream">
    P
</span>

<!-- Absent -->
<span class="px-3 py-1 rounded-lg text-sm font-semibold bg-cream text-black border border-black">
    A
</span>

<!-- Other -->
<span class="px-3 py-1 rounded-lg text-sm font-semibold bg-light-blue text-black">
    PH
</span>
```

### Example: Mobile Card
```html
<div class="bg-cream border border-light-blue rounded-2xl p-4">
    <div class="flex justify-between items-start mb-4">
        <div>
            <p class="font-bold text-black">John Doe</p>
            <p class="text-sm text-black/60">EMP001</p>
        </div>
        <span class="px-3 py-1 rounded-lg text-sm font-semibold bg-dark-blue text-cream">
            P
        </span>
    </div>
    <div class="space-y-3 text-sm text-black">
        <div class="flex justify-between">
            <span class="font-semibold text-black/70">Date:</span>
            <span>01-01-2024</span>
        </div>
    </div>
</div>
```

### Example: Navigation Link
```html
<a href="/dashboard" class="flex items-center rounded-lg text-sm font-semibold transition-colors duration-200 text-dark-blue font-bold" style="gap: 0.5rem; padding: 0.5rem 1rem;">
    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
    </svg>
    <span>Dashboard</span>
</a>
```

---

## Maintenance Guidelines

### Adding New Colors
1. Add to Tailwind config in base.html
2. Add CSS override in style block
3. Document in this file
4. Test contrast ratios

### Adding New Components
1. Follow existing patterns
2. Use established spacing scale
3. Maintain responsive behavior
4. Test on all breakpoints
5. Document in this file

### Modifying Existing Components
1. Check all usages first
2. Maintain backward compatibility
3. Test thoroughly
4. Update documentation

---

## Quick Reference

### Most Used Classes
```
Spacing:     gap-3, gap-4, p-4, p-6, px-3, py-2, space-y-4
Colors:      bg-cream, bg-light-blue, bg-dark-blue, text-black
Borders:     border, border-light-blue, rounded-xl, rounded-2xl
Typography:  text-sm, text-xs, font-semibold, font-bold
Layout:      flex, grid, items-center, justify-between
Responsive:  md:hidden, md:block, md:flex, lg:grid-cols-3
```

### Color Hex Codes
```
#EFECE3  Cream
#8FABD4  Light Blue
#4A70A9  Dark Blue
#000000  Black
```

---

**Last Updated**: November 2024
**Version**: 1.0
**Framework**: Tailwind CSS 3.4.1
**Font**: Inter (Google Fonts)
