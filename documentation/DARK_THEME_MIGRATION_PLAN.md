# Dark Theme Migration Plan

## Overview
Applying the dark theme design system across all pages requires systematic updates to colors, backgrounds, and text throughout the application.

## Completed
✅ Base template - Added dark theme CSS variables
✅ Body background - Changed to dark-bg
✅ Attendance list - Converted to dark theme grid cards
✅ Mobile/Desktop headers - Updated to dark backgrounds

## Pages to Update

### High Priority
1. **Dashboard** (`dashboard.html`) - Main landing page
2. **Mandays List** (`mandays_list.html`) - Similar to attendance
3. **Login** (`login.html`) - Entry point

### Medium Priority
4. **Upload pages** (`upload.html`, `upload_mandays.html`)
5. **Request pages** (`request_access.html`, `my_requests.html`, `approve_requests.html`)
6. **User management** (`user_list.html`, `user_create.html`, `user_edit.html`)
7. **Manage assignments** (`manage_assignments.html`)

### Low Priority
8. **Error pages** (`403.html`, `404.html`, `500.html`)

## Global Changes Needed

### 1. Navigation (base.html)
- [x] Header backgrounds → `var(--dark-card)`
- [x] Header borders → `var(--dark-border)`
- [ ] Nav link text → white
- [ ] Nav link hover → `var(--dark-primary)`
- [ ] Active nav → `var(--dark-primary)` background
- [ ] User avatar background → `var(--dark-secondary)`
- [ ] Logout button → `var(--dark-primary)` border

### 2. Forms & Inputs
Replace:
- `bg-cream` → `style="background-color: var(--dark-secondary);"`
- `border-light-blue` → `style="border-color: var(--dark-border);"`
- `text-black` → `text-white`
- `text-black/60` → `dark-muted`

### 3. Cards & Containers
Replace:
- `bg-white` → `dark-card`
- `border-light-blue` → `style="border-color: var(--dark-border);"`
- Card shadows → subtle dark shadows

### 4. Buttons
- Primary: `var(--dark-primary)` background
- Secondary: `var(--dark-secondary)` background
- Danger: Keep red but darker shade

### 5. Tables
- Header: `var(--dark-secondary)` background
- Rows: `var(--dark-card)` background
- Hover: `var(--dark-muted)` background
- Text: white

### 6. Status Badges
- Success: `var(--dark-success)`
- Warning: `var(--dark-warning)`
- Info: `var(--dark-primary)`

## Color Mapping

| Old Color | New Color | CSS Variable |
|-----------|-----------|--------------|
| `#EFECE3` (cream) | `hsl(220, 30%, 5%)` | `var(--dark-bg)` |
| `#FFFFFF` (white) | `hsl(220, 25%, 8%)` | `var(--dark-card)` |
| `#8FABD4` (light-blue) | `hsl(220, 20%, 18%)` | `var(--dark-border)` |
| `#4A70A9` (dark-blue) | `hsl(166, 100%, 48%)` | `var(--dark-primary)` |
| `#000000` (black) | `#FFFFFF` (white) | - |
| Text muted | `hsl(220, 10%, 55%)` | `var(--dark-muted-fg)` |

## Implementation Strategy

### Option 1: Manual (Current Approach)
Update each template file individually
- Pros: Full control, can test each page
- Cons: Time-consuming, many files

### Option 2: CSS Override
Create a dark theme CSS class and apply globally
- Pros: Faster, centralized
- Cons: May conflict with existing styles

### Option 3: Hybrid (Recommended)
1. Update base.html with global dark styles
2. Update high-priority pages manually
3. Use CSS overrides for remaining pages

## Next Steps

1. Test current changes (attendance list)
2. If approved, proceed with dashboard
3. Then mandays list
4. Continue with remaining pages

## Rollback Plan

If dark theme isn't working:
```bash
git checkout ddfcd71  # Previous commit
```

Or create a theme toggle to switch between light/dark modes.
