# Attendance Management System - UI/UX Design Guide

This document outlines the design system, user interface (UI) principles, and user experience (UX) goals for the Attendance Management System application.

## 1. Design Philosophy

The application's design is guided by three core principles:

1.  **Professional & Data-Focused**: The UI prioritizes clarity and efficient data presentation, adopting an enterprise-grade aesthetic suitable for a business environment.
2.  **Clean & Minimalist**: A limited color palette and generous use of whitespace create a calm, uncluttered interface that reduces cognitive load and helps users focus on their tasks.
3.  **Responsive & Accessible**: The system is designed to be fully functional and visually consistent across desktop, tablet, and mobile devices, with a focus on readability and intuitive interactions.

---

## 2. Color Palette

The color scheme is intentionally constrained to create a cohesive and professional look.

| Color      | Hex Code                                                            | Usage                                                                                             |
| :--------- | :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------ |
| **Cream**  | `bg-cream` <br/> `#EFECE3`                                          | The primary background color for the entire application, providing a soft, easy-on-the-eyes canvas. |
| **Light Blue** | `bg-light-blue` <br/> `#8FABD4`                                     | Secondary backgrounds, navigation bars, table headers, info boxes, and decorative borders.          |
| **Dark Blue**  | `bg-dark-blue` <br/> `#4A70A9`                                       | Primary action color for buttons, active navigation links, icons, and important status badges.    |
| **Black**      | `text-black` <br/> `#000000`                                        | The primary color for all text and icons, ensuring high contrast and readability.                 |

---

## 3. Typography

The entire application uses the **Inter** font family, chosen for its excellent readability on screens at various sizes and weights.

-   **Font Family**: `Inter`, sans-serif
-   **Font Smoothing**: Enabled for a smoother, more refined text appearance.

### Type Scale

| Element             | Font Weight | Font Size (Tailwind) | Example Usage                               |
| :------------------ | :---------- | :------------------- | :------------------------------------------ |
| **Display**         | Extrabold   | `text-5xl`           | Login screen main heading.                  |
| **Heading 1 (H1)**  | Extrabold   | `text-4xl`           | Page titles on desktop.                     |
| **Heading 2 (H2)**  | Bold        | `text-xl`            | Card titles, section headers.               |
| **Heading 3 (H3)**  | Bold        | `text-lg`            | Sub-section headers (e.g., "Recent Exports"). |
| **Body (Default)**  | Regular     | `text-sm`, `text-base` | Paragraphs, table content, general text.    |
| **Label / Input**   | Semibold    | `text-sm`            | Form labels, button text.                   |
| **Small / Meta**    | Regular     | `text-xs`            | Helper text, meta-information (e.g., dates). |

---

## 4. Layout & Spacing

The layout is structured for intuitive navigation and a clear content hierarchy.

-   **Main Structure**:
    -   **Desktop**: A fixed top navigation bar (`h-20`) with a main content area below.
    -   **Mobile**: A main content area with a fixed bottom navigation bar (`h-20`) for easy thumb access.
-   **Content Container**: The main content is constrained to a `max-w-7xl` container with horizontal padding (`px-4 sm:px-6 lg:px-8`) to maintain optimal line length and visual balance.
-   **Spacing**: The design uses Tailwind's default spacing scale (based on a `4px` unit) for consistent padding, margins, and gaps between elements. Common paddings for cards are `p-6` or `p-8`.
-   **Responsiveness**: The UI uses `md` (768px) as its primary breakpoint to switch between mobile and desktop layouts. Specific components, like tables, have a custom mobile-first design that transforms into a card view on smaller screens.

---

## 5. Component Library

Core components are designed to be reusable, consistent, and accessible.

### Cards

-   **Base Card**: The primary content container.
    -   `bg-cream` background.
    -   `1px` `border-light-blue` border.
    -   `rounded-2xl` for soft, modern corners.
    -   Default padding of `p-6 md:p-8`.
-   **Stat Card**: Used on the dashboard for key metrics.
    -   `bg-light-blue` background to stand out.
    -   Features a prominent icon, large numeric value, and descriptive label.

### Buttons

-   **Solid Button (Primary)**:
    -   **Style**: `bg-dark-blue` with `text-cream` font.
    -   **Interaction**: Transitions to `bg-black` on hover for clear feedback.
    -   **Focus State**: A `ring-4` with `ring-dark-blue/50` ensures accessibility.
-   **Secondary/Filter Buttons**:
    -   Use simpler styles, such as `bg-black` or `bg-light-blue/50`, to de-emphasize them relative to primary actions.

### Forms & Inputs

-   **Text Inputs & Selects**:
    -   **Style**: `bg-cream` with a `border-light-blue`. Placeholder text is `text-black/50`.
    -   **Interaction**: On focus, a `ring-2 ring-dark-blue` appears, providing a clear visual cue that the field is active.
    -   **Icons**: Inputs often include a decorative icon on the left for better context and visual appeal.

### Tables

-   **Desktop View**: A standard tabular layout with a `bg-light-blue` header. Rows have a bottom border and a subtle hover effect (`hover:bg-light-blue/40`).
-   **Mobile Card View**: Below the `md` breakpoint, the table transforms:
    -   `thead` is hidden.
    -   Each `<tr>` becomes a self-contained card with padding and a border.
    -   Each `<td>` becomes a flex row, with a label generated from a `data-label` attribute using the `::before` pseudo-element. This creates a readable key-value pair format.

### Badges

-   Small, rounded tags used to display status, roles, or categories.
-   Colors are contextual:
    -   **Dark Blue**: For positive or active states (e.g., "Present", "Active").
    -   **Light Blue**: For neutral, informational states (e.g., "Holiday", "User").
    -   **Black/Cream Border**: For negative or inactive states (e.g., "Absent", "Inactive").
    -   **Black**: For the highest-level role ("Root").

---

## 6. Iconography

-   **Style**: The application uses a consistent set of custom SVG icons inspired by the Heroicons "outline" style.
-   **Implementation**: Icons are stateless React components with a consistent `strokeWidth={1.5}`.
-   **Sizing**: Standard icon size is `w-5 h-5`. Larger icons (`w-8 h-8`) are used for page titles to create visual hierarchy.
-   **Color**: Icons inherit their color via `stroke="currentColor"`, making them easy to style with Tailwind's text color utilities (e.g., `text-black`, `text-dark-blue`).
