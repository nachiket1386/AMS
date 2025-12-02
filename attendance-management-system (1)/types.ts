
export enum Page {
  Dashboard = 'Dashboard',
  Upload = 'Upload',
  Data = 'Data',
  Export = 'Export',
  Logs = 'Logs',
  Users = 'Users',
}

export enum UserRole {
  Root = 'Root',
  Admin = 'Admin',
  User = 'User1',
}

export interface User {
  username: string;
  role: UserRole;
  company: string;
}

export enum AttendanceStatus {
    Present = 'Present',
    Absent = 'Absent',
    Holiday = 'Holiday',
    HalfDay = 'Half Day',
}

export interface AttendanceRecord {
    id: string;
    name: string;
    company: string;
    date: string;
    shift: string;
    status: AttendanceStatus;
    inTime: string;
    outTime: string;
    overstay: string;
}

export interface UploadLog {
    id: number;
    fileName: string;
    uploadedBy: string;
    company: string;
    date: string;
    total: number;
    success: number;
    updated: number;
    errors: number;
}

export interface ExistingUser {
    id: number;
    username: string;
    role: UserRole;
    company: string;
    status: 'Active' | 'Inactive';
}
