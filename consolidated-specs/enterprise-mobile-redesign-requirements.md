# Requirements Document: Enterprise-Mobile Responsive Redesign

## Introduction

This document specifies requirements for a comprehensive visual redesign of the Django Attendance Management System. The redesign transforms the application from its current state to a professional Enterprise Dashboard on desktop that seamlessly transitions to a modern, native-feeling Mobile App on smaller screens, following a strict 4-color design system.

## Glossary

- **AMS**: Attendance Management System
- **Enterprise Dashboard**: Professional desktop interface with top navigation and grid layouts
- **Mobile Native App**: Mobile interface with floating dock navigation and card-based layouts
- **Floating Dock**: Bottom navigation bar with rounded container floating above the screen edge
- **Bottom Sheet**: Slide-up modal menu for mobile admin functions
- **Cream**: Background color #EFECE3
- **Light Blue**: Accent color #8FABD4
- **Dark Blue**: Primary action color #4A70A9
- **Black**: Text and contrast color #000000
- **Breakpoint**: 768px width - below is mobile, above is desktop
- **Card Stack**: Mobile layout where table rows become individual vertical cards
- **Grid Cards**: Dashboard stat cards arranged in a 2x2 grid on mobile

## Requirements

### Requirement 1: Visual Identity System

**User Story:** As a user, I want a consistent, professional visual identity across all pages, so that the application feels cohesive and branded.

#### Acceptance Criteria

1. WHEN viewing any page THEN the system SHALL use only the 4-color palette: Cream (#EFECE3), Light Blue (#8FABD4), Dark Blue (#4A70A9), and Black (#000000)
2. WHEN viewing text THEN the system SHALL use Inter font family with appropriate weights (Regular, Medium, Semibold, Bold, Extrabold)
3. WHEN viewing buttons and inputs THEN the system SHALL use rounded-lg (8px) corner radius
4. WHEN viewing cards and containers THEN the system SHALL use rounded-2xl (16px) corner radius
5. WHEN viewing mobile dock elements THEN the system SHALL use rounded-[2rem] (32px) corner radius

### Requirement 2: Responsive Navigation System

**User Story:** As a user, I want navigation that adapts to my device, so that I have an optimal experience on both desktop and mobile.

#### Acceptance Criteria

1. WHEN viewing on desktop (width > 768px) THEN the system SHALL display a fixed top navigation bar with logo, text links, and user profile
2. WHEN viewing on mobile (width < 768px) THEN the system SHALL display a minimal top header and floating dock bottom navigation
3. WHEN hovering over Admin link on desktop THEN the system SHALL show a dropdown menu with admin options
4. WHEN tapping Admin on mobile THEN the system SHALL open a bottom sheet with admin options in a grid
5. WHEN navigating THEN the system SHALL show active state with Dark Blue color and appropriate visual feedback

### Requirement 3: Dashboard Grid Layout

**User Story:** As a user, I want to see key statistics in an organized layout, so that I can quickly understand system status.

#### Acceptance Criteria

1. WHEN viewing dashboard on desktop THEN the system SHALL display 4 horizontal stat cards with icons on the left
2. WHEN viewing dashboard on mobile THEN the system SHALL display a 2x2 grid of square stat cards
3. WHEN viewing mobile stat cards THEN the system SHALL use distinct background colors: Employees (Light Blue), Present (Dark Blue), On Leave (Cream with border), Late (Black)
4. WHEN viewing stat cards THEN the system SHALL show large central number, icon top-left, and label bottom-center
5. WHEN viewing dashboard THEN the system SHALL display page title "Dashboard" with current date

### Requirement 4: Data Table Responsive Transformation

**User Story:** As a user, I want attendance data displayed appropriately for my device, so that I can easily view and interact with records.

#### Acceptance Criteria

1. WHEN viewing attendance list on desktop THEN the system SHALL display a full-width table with Light Blue header row
2. WHEN viewing attendance list on mobile THEN the system SHALL transform table rows into individual vertical cards
3. WHEN viewing mobile cards THEN the system SHALL show name and date on top, status badge on top right, and times in a grid below
4. WHEN viewing status badges THEN the system SHALL use Present (Dark Blue), Late/Holiday (Light Blue), Absent (transparent with Black border)
5. WHEN viewing mobile cards THEN the system SHALL include a full-width "View Details" button at the bottom

### Requirement 5: Login Page Design

**User Story:** As a user, I want a clean, professional login page, so that I have a good first impression of the system.

#### Acceptance Criteria

1. WHEN viewing login page THEN the system SHALL display a centered card on Cream background
2. WHEN viewing login header THEN the system SHALL show "AMS" in 5xl Extrabold Dark Blue
3. WHEN viewing login form THEN the system SHALL display inputs with icons (Mail, Lock) inside the left edge
4. WHEN viewing login button THEN the system SHALL display full-width Dark Blue button that turns Black on hover
5. WHEN viewing login page THEN the system SHALL use vertical stack layout for form elements

### Requirement 6: User1 Request Pages Design

**User Story:** As a User1 supervisor, I want request pages that follow the design system, so that I have a consistent experience.

#### Acceptance Criteria

1. WHEN viewing Request Access page THEN the system SHALL use design system colors, typography, and spacing
2. WHEN viewing My Requests page THEN the system SHALL display requests as cards with status badges using system colors
3. WHEN viewing request forms THEN the system SHALL use rounded-lg inputs with Light Blue borders
4. WHEN viewing submit buttons THEN the system SHALL use Dark Blue primary buttons with hover effects
5. WHEN viewing on mobile THEN the system SHALL stack form elements vertically with appropriate spacing

### Requirement 7: Admin Pages Design

**User Story:** As an Admin, I want admin pages that follow the design system, so that I can efficiently manage the system.

#### Acceptance Criteria

1. WHEN viewing Approve Requests page THEN the system SHALL display pending requests as cards with action buttons
2. WHEN viewing Manage Assignments page THEN the system SHALL use table on desktop and card stack on mobile
3. WHEN viewing admin action buttons THEN the system SHALL use Dark Blue for approve and Light Blue for secondary actions
4. WHEN viewing admin pages on mobile THEN the system SHALL transform tables into card stacks
5. WHEN viewing admin navigation THEN the system SHALL show admin options in dropdown (desktop) or bottom sheet (mobile)

### Requirement 8: Interactive States and Animations

**User Story:** As a user, I want visual feedback for my interactions, so that I know the system is responding.

#### Acceptance Criteria

1. WHEN hovering over elements on desktop THEN the system SHALL shift background color to Light Blue/20
2. WHEN clicking buttons on mobile THEN the system SHALL apply active:scale-95 animation
3. WHEN opening mobile menus THEN the system SHALL slide in with animate-in slide-in-from-bottom transition
4. WHEN viewing active navigation items THEN the system SHALL show Dark Blue color and appropriate background
5. WHEN interacting with cards THEN the system SHALL provide subtle hover effects on desktop

### Requirement 9: Role-Based Visual Presentation

**User Story:** As a user with a specific role, I want to see only the navigation and features appropriate for my role, so that I'm not confused by irrelevant options.

#### Acceptance Criteria

1. WHEN logged in as ROOT THEN the system SHALL show all navigation items including Logs and Backup
2. WHEN logged in as ADMIN THEN the system SHALL show Dashboard, Upload, Data, and standard Admin functions
3. WHEN logged in as USER1 THEN the system SHALL show Dashboard, Data, and Request-related pages only
4. WHEN viewing navigation THEN the system SHALL hide items not available to current user role
5. WHEN viewing admin dropdown/sheet THEN the system SHALL show only functions available to current user role

### Requirement 10: Typography Hierarchy

**User Story:** As a user, I want clear visual hierarchy in text, so that I can quickly scan and understand content.

#### Acceptance Criteria

1. WHEN viewing page titles on desktop THEN the system SHALL use Extrabold 4xl
2. WHEN viewing page titles on mobile THEN the system SHALL use Bold lg
3. WHEN viewing card numbers THEN the system SHALL use Bold 3xl
4. WHEN viewing body text THEN the system SHALL use Regular or Medium sm/base
5. WHEN viewing labels THEN the system SHALL use Semibold xs/sm with uppercase where appropriate

