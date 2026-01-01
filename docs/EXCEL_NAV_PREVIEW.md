# Excel File Upload Navigation - Visual Preview

## Desktop Navigation Bar

```
┌─────────────────────────────────────────────────────────────────────────┐
│ AMS    [🏠 Dashboard] [📤 Upload] [📋 Data] [📊 Excel File Upload] ... │
└─────────────────────────────────────────────────────────────────────────┘
```

### Navigation Link Details

**Label:** 📊 Excel File Upload

**Tooltip (on hover):**
> Upload attendance data files (Punchrecord, ARC Summary, Overtime, Partial Day, Regularization)

**Visibility:** Only for Root and Admin users

**Active State:** Highlights in dark blue when on the Excel upload page

---

## Mobile Navigation (Admin Bottom Sheet)

When you tap the "Admin" button in the mobile dock, you'll see:

```
┌─────────────────────────────────────────────┐
│         Admin Functions              [×]    │
├─────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐                │
│  │    ✓     │  │   📋     │                │
│  │ Approve  │  │ Manage   │                │
│  │ Requests │  │Assignments│               │
│  └──────────┘  └──────────┘                │
│                                             │
│  ┌──────────┐  ┌──────────┐                │
│  │   👥     │  │ 📊 📄    │                │
│  │  Users   │  │  Excel   │                │
│  │          │  │File Upload│               │
│  └──────────┘  └──────────┘                │
│                                             │
│  ┌──────────┐  ┌──────────┐                │
│  │   📚     │  │   💾     │                │
│  │  Upload  │  │  Backup  │                │
│  │   Logs   │  │   Data   │                │
│  └──────────┘  └──────────┘                │
│                                             │
│  ┌──────────┐                               │
│  │   ⬆️     │                               │
│  │ Restore  │                               │
│  │   Data   │                               │
│  └──────────┘                               │
└─────────────────────────────────────────────┘
```

---

## What Happens When You Click

1. **Desktop:** Clicking "📊 Excel File Upload" takes you directly to `/excel/upload/`
2. **Mobile:** Tapping the card takes you directly to `/excel/upload/`

## Supported File Types

The upload page supports these Excel file types:
- ✅ Punchrecord files
- ✅ ARC Summary files
- ✅ Overtime files
- ✅ Partial Day files
- ✅ Regularization files

## File Formats Supported

- `.xls` (HTML-based Excel)
- `.xls` (Binary Excel)
- `.xlsx` (Modern Excel)

---

## Quick Access Path

**For Root/Admin Users:**

1. Login → See "📊 Excel File Upload" in navbar
2. Click → Upload page opens
3. Drag & drop or select files
4. Upload and process

**Simple and direct!** 🎯
