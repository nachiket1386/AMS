# 🗄️ Database Entity Relationship Diagram

## Complete ER Diagram - Attendance Management System

```mermaid
erDiagram
    COMPANY ||--o{ USER : "employs"
    COMPANY ||--o{ ATTENDANCE_RECORD : "has"
    COMPANY ||--o{ MANDAY_SUMMARY : "has"
    COMPANY ||--o{ EMPLOYEE_ASSIGNMENT : "has"
    COMPANY ||--o{ ACCESS_REQUEST : "has"
    
    USER ||--o{ UPLOAD_LOG : "creates"
    USER ||--o{ MANDAY_UPLOAD_LOG : "creates"
    USER ||--o{ BACKUP_LOG : "creates"
    USER ||--o{ EMPLOYEE_ASSIGNMENT : "supervises"
    USER ||--o{ EMPLOYEE_ASSIGNMENT : "assigned_by"
    USER ||--o{ ACCESS_REQUEST : "requests"
    USER ||--o{ ACCESS_REQUEST : "reviews"
    USER ||--o{ AUDIT_LOG : "performs"
    USER ||--o{ AUDIT_LOG : "target_of"
    
    ACCESS_REQUEST ||--o{ AUDIT_LOG : "generates"
    EMPLOYEE_ASSIGNMENT ||--o{ AUDIT_LOG : "generates"

    COMPANY {
        int id PK
        string name UK
        datetime created_at
    }
    
    USER {
        int id PK
        string username UK
        string password
        string email
        string role "root/admin/user1"
        int company_id FK
        date assigned_date_from
        date assigned_date_to
        bool is_staff
        bool is_active
        bool is_superuser
        datetime last_login
        datetime date_joined
    }
    
    ATTENDANCE_RECORD {
        int id PK
        string ep_no
        string ep_name
        int company_id FK
        date date
        string shift
        string overstay
        string status "P/A/PH/WO/-0.5/-1"
        time in_time
        time out_time
        time in_time_2
        time out_time_2
        time in_time_3
        time out_time_3
        time overtime
        time overtime_to_mandays
        datetime created_at
        datetime updated_at
    }
    
    MANDAY_SUMMARY {
        int id PK
        string ep_no
        int company_id FK
        date punch_date
        decimal mandays
        decimal ot
        time regular_manday_hr
        string trade
        string contract
        string plant
        string plant_desc
        datetime created_at
        datetime updated_at
    }
    
    EMPLOYEE_ASSIGNMENT {
        int id PK
        int user_id FK "User1 supervisor"
        string ep_no
        string ep_name
        int company_id FK
        date access_from
        date access_to
        int assigned_by_id FK
        datetime assigned_at
        string source "request/admin"
        bool is_active
    }
    
    ACCESS_REQUEST {
        int id PK
        int requester_id FK
        string ep_no
        int company_id FK
        string access_type "date_range/permanent"
        date access_from
        date access_to
        text justification
        string status "pending/approved/rejected/cancelled"
        int reviewed_by_id FK
        datetime reviewed_at
        text rejection_reason
        datetime created_at
        datetime updated_at
    }
    
    AUDIT_LOG {
        int id PK
        datetime timestamp
        int actor_id FK
        string action
        int target_user_id FK
        string target_ep_no
        json details
    }
    
    UPLOAD_LOG {
        int id PK
        int user_id FK
        datetime uploaded_at
        string filename
        int success_count
        int updated_count
        int error_count
        text error_messages
    }
    
    MANDAY_UPLOAD_LOG {
        int id PK
        int user_id FK
        datetime uploaded_at
        string filename
        int success_count
        int updated_count
        int error_count
        text error_messages
    }
    
    BACKUP_LOG {
        int id PK
        int user_id FK
        string operation "backup_full/backup_incremental/restore"
        string filename
        datetime created_at
        int companies_count
        int records_count
        int records_added
        int records_updated
        int records_skipped
        bool success
        text error_message
    }
```

---

## Simplified View - Core Relationships

```mermaid
graph TB
    subgraph "Multi-Tenancy Layer"
        COMPANY[🏢 COMPANY<br/>104 records]
    end
    
    subgraph "User Management"
        USER[👤 USER<br/>3 records<br/>Roles: root/admin/user1]
    end
    
    subgraph "Attendance Data"
        ATTENDANCE[📋 ATTENDANCE_RECORD<br/>96,315 records<br/>Daily attendance tracking]
        MANDAYS[⏰ MANDAY_SUMMARY<br/>37,086 records<br/>Mandays & OT summary]
    end
    
    subgraph "Access Control"
        ASSIGNMENT[🔐 EMPLOYEE_ASSIGNMENT<br/>1 record<br/>User1 → Employee access]
        REQUEST[📝 ACCESS_REQUEST<br/>1 record<br/>Request workflow]
        AUDIT[📊 AUDIT_LOG<br/>6 records<br/>Audit trail]
    end
    
    subgraph "Upload Logs"
        UPLOAD[📤 UPLOAD_LOG<br/>21 records]
        MANDAY_UPLOAD[📤 MANDAY_UPLOAD_LOG<br/>4 records]
        BACKUP[💾 BACKUP_LOG<br/>1 record]
    end
    
    COMPANY -->|owns| ATTENDANCE
    COMPANY -->|owns| MANDAYS
    COMPANY -->|employs| USER
    COMPANY -->|has| ASSIGNMENT
    COMPANY -->|has| REQUEST
    
    USER -->|creates| UPLOAD
    USER -->|creates| MANDAY_UPLOAD
    USER -->|creates| BACKUP
    USER -->|supervises| ASSIGNMENT
    USER -->|requests| REQUEST
    USER -->|reviews| REQUEST
    USER -->|performs| AUDIT
    
    REQUEST -->|approved| ASSIGNMENT
    REQUEST -->|logs| AUDIT
    ASSIGNMENT -->|logs| AUDIT
    
    style COMPANY fill:#4A70A9,stroke:#000,stroke-width:2px,color:#fff
    style USER fill:#8FABD4,stroke:#000,stroke-width:2px,color:#000
    style ATTENDANCE fill:#EFECE3,stroke:#4A70A9,stroke-width:2px,color:#000
    style MANDAYS fill:#EFECE3,stroke:#4A70A9,stroke-width:2px,color:#000
    style ASSIGNMENT fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style REQUEST fill:#FFD700,stroke:#000,stroke-width:2px,color:#000
    style AUDIT fill:#FFA07A,stroke:#000,stroke-width:2px,color:#000
```

---

## Access Control Flow Diagram

```mermaid
flowchart TD
    START([User1 needs employee access])
    
    START --> CHECK{Has existing<br/>assignment?}
    
    CHECK -->|Yes| ACCESS[✅ Access Granted<br/>View employee data]
    CHECK -->|No| CREATE_REQUEST[📝 Create Access Request]
    
    CREATE_REQUEST --> PENDING[⏳ Status: PENDING]
    PENDING --> ADMIN_REVIEW{Admin Reviews}
    
    ADMIN_REVIEW -->|Approve| APPROVED[✅ Status: APPROVED]
    ADMIN_REVIEW -->|Reject| REJECTED[❌ Status: REJECTED]
    PENDING -->|User cancels| CANCELLED[🚫 Status: CANCELLED]
    
    APPROVED --> CREATE_ASSIGNMENT[🔐 Create Employee Assignment]
    CREATE_ASSIGNMENT --> LOG_AUDIT[📊 Log to Audit Trail]
    LOG_AUDIT --> ACCESS
    
    REJECTED --> LOG_REJECT[📊 Log Rejection]
    CANCELLED --> LOG_CANCEL[📊 Log Cancellation]
    
    ACCESS --> CHECK_DATE{Within date<br/>range?}
    CHECK_DATE -->|Yes| ALLOW[✅ Allow Data Access]
    CHECK_DATE -->|No| DENY[❌ Deny Access]
    
    style START fill:#4A70A9,stroke:#000,stroke-width:2px,color:#fff
    style ACCESS fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style APPROVED fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style REJECTED fill:#FF6B6B,stroke:#000,stroke-width:2px,color:#fff
    style CANCELLED fill:#FFA500,stroke:#000,stroke-width:2px,color:#000
    style ALLOW fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style DENY fill:#FF6B6B,stroke:#000,stroke-width:2px,color:#fff
```

---

## Data Upload Flow

```mermaid
flowchart LR
    subgraph "Attendance Upload"
        A1[📄 CSV File] --> A2[🔄 Process Upload]
        A2 --> A3{Validation}
        A3 -->|Valid| A4[💾 Save to<br/>ATTENDANCE_RECORD]
        A3 -->|Invalid| A5[❌ Log Errors]
        A4 --> A6[📝 Create UPLOAD_LOG]
        A5 --> A6
    end
    
    subgraph "Mandays Upload"
        M1[📄 CSV File] --> M2[🔄 Process Upload]
        M2 --> M3{Validation}
        M3 -->|Valid| M4[💾 Save to<br/>MANDAY_SUMMARY]
        M3 -->|Invalid| M5[❌ Log Errors]
        M4 --> M6[📝 Create MANDAY_UPLOAD_LOG]
        M5 --> M6
    end
    
    style A4 fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style M4 fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style A5 fill:#FF6B6B,stroke:#000,stroke-width:2px,color:#fff
    style M5 fill:#FF6B6B,stroke:#000,stroke-width:2px,color:#fff
```

---

## Role-Based Access Matrix

```mermaid
graph TB
    subgraph "ROOT User"
        R1[✅ Full System Access]
        R2[✅ All Companies]
        R3[✅ User Management]
        R4[✅ Backup/Restore]
        R5[✅ Upload Logs]
    end
    
    subgraph "ADMIN User"
        A1[✅ Company Data Access]
        A2[✅ Approve Requests]
        A3[✅ Manage Assignments]
        A4[✅ Upload Data]
        A5[❌ Other Companies]
    end
    
    subgraph "USER1 Supervisor"
        U1[✅ Assigned Employees Only]
        U2[✅ Date-Range Limited]
        U3[✅ Request Access]
        U4[✅ View Own Requests]
        U5[❌ Upload Data]
    end
    
    style R1 fill:#4A70A9,stroke:#000,stroke-width:2px,color:#fff
    style R2 fill:#4A70A9,stroke:#000,stroke-width:2px,color:#fff
    style R3 fill:#4A70A9,stroke:#000,stroke-width:2px,color:#fff
    style R4 fill:#4A70A9,stroke:#000,stroke-width:2px,color:#fff
    style R5 fill:#4A70A9,stroke:#000,stroke-width:2px,color:#fff
    
    style A1 fill:#8FABD4,stroke:#000,stroke-width:2px,color:#000
    style A2 fill:#8FABD4,stroke:#000,stroke-width:2px,color:#000
    style A3 fill:#8FABD4,stroke:#000,stroke-width:2px,color:#000
    style A4 fill:#8FABD4,stroke:#000,stroke-width:2px,color:#000
    style A5 fill:#FF6B6B,stroke:#000,stroke-width:2px,color:#fff
    
    style U1 fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style U2 fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style U3 fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style U4 fill:#90EE90,stroke:#000,stroke-width:2px,color:#000
    style U5 fill:#FF6B6B,stroke:#000,stroke-width:2px,color:#fff
```

---

## Database Indexes Visualization

```mermaid
graph LR
    subgraph "ATTENDANCE_RECORD Indexes"
        AR1[📇 ep_no + date<br/>UNIQUE]
        AR2[📇 company_id + date]
        AR3[📇 date]
    end
    
    subgraph "MANDAY_SUMMARY Indexes"
        MS1[📇 ep_no + punch_date<br/>UNIQUE]
        MS2[📇 company_id + punch_date]
        MS3[📇 punch_date]
    end
    
    subgraph "ACCESS_REQUEST Indexes"
        AC1[📇 requester_id + status]
        AC2[📇 status + created_at]
        AC3[📇 ep_no + status]
    end
    
    subgraph "EMPLOYEE_ASSIGNMENT Indexes"
        EA1[📇 user_id + is_active]
        EA2[📇 ep_no + is_active]
        EA3[📇 company_id + is_active]
    end
    
    style AR1 fill:#FFD700,stroke:#000,stroke-width:2px,color:#000
    style MS1 fill:#FFD700,stroke:#000,stroke-width:2px,color:#000
```

---

## Key Relationships Summary

### 1️⃣ **Multi-Tenancy (Company-Based)**
- Every data record belongs to a company
- Users are assigned to companies
- Data isolation enforced at query level

### 2️⃣ **User Roles & Permissions**
- **Root**: System-wide access
- **Admin**: Company-level access
- **User1**: Employee-level access (via assignments)

### 3️⃣ **Access Control Workflow**
```
User1 → Access Request → Admin Review → Approval → Employee Assignment → Data Access
```

### 4️⃣ **Data Upload Pipeline**
```
CSV File → Validation → Database Insert/Update → Upload Log → Audit Trail
```

### 5️⃣ **Audit Trail**
- All access requests logged
- All assignments tracked
- All administrative actions recorded

---

## Cardinality Legend

| Symbol | Meaning |
|--------|---------|
| `||--o{` | One-to-Many |
| `||--||` | One-to-One |
| `}o--o{` | Many-to-Many |
| `PK` | Primary Key |
| `FK` | Foreign Key |
| `UK` | Unique Key |

---

## Table Size Summary

| Table | Records | Growth Rate |
|-------|---------|-------------|
| 📋 ATTENDANCE_RECORD | 96,315 | High (daily) |
| ⏰ MANDAY_SUMMARY | 37,086 | High (daily) |
| 🏢 COMPANY | 104 | Low (stable) |
| 📤 UPLOAD_LOG | 21 | Medium (per upload) |
| 📤 MANDAY_UPLOAD_LOG | 4 | Medium (per upload) |
| 📊 AUDIT_LOG | 6 | Medium (per action) |
| 👤 USER | 3 | Low (stable) |
| 🔐 EMPLOYEE_ASSIGNMENT | 1 | Low (as needed) |
| 📝 ACCESS_REQUEST | 1 | Low (as needed) |
| 💾 BACKUP_LOG | 1 | Low (per backup) |

---

## Performance Considerations

### ✅ Optimized Queries
- Indexed on frequently queried columns
- Composite indexes for multi-column filters
- Unique constraints prevent duplicates

### ⚠️ Watch For
- Attendance table growing rapidly (96K+ records)
- Mandays table growing rapidly (37K+ records)
- Consider archiving old data periodically

### 🚀 Recommendations
1. Archive attendance data older than 2 years
2. Partition large tables by date
3. Regular VACUUM operations on SQLite
4. Consider PostgreSQL for production scale
