import React from 'react';
import Card from '../components/Card';
import Badge from '../components/Badge';
import { MOCK_ATTENDANCE_DATA } from '../constants';
import { AttendanceStatus } from '../types';
import { DataIcon, SearchIcon, CalendarIcon, ClockIcon, CheckIcon, SignInIcon, SignOutIcon, HourglassIcon, CogIcon, UserIcon, BuildingIcon, TrashIcon } from '../constants';

const statusStyles: { [key in AttendanceStatus]: string } = {
  [AttendanceStatus.Present]: 'bg-dark-blue text-cream',
  [AttendanceStatus.Absent]: 'bg-cream text-black border border-black',
  [AttendanceStatus.Holiday]: 'bg-light-blue text-black',
  [AttendanceStatus.HalfDay]: 'bg-light-blue text-black',
};

const ViewDataPage: React.FC = () => {
    return (
    <div className="space-y-8">
        <div>
            <h1 className="text-2xl md:text-4xl font-extrabold text-black flex items-center gap-3">
                <DataIcon className="w-8 h-8"/>
                Attendance Data
            </h1>
            <p className="text-black/70 mt-1 hidden md:block">View and manage attendance records.</p>
        </div>

        <Card padding="p-4 md:p-6">
            <div className="flex flex-col md:flex-row gap-4 items-center">
                <div className="relative w-full md:flex-grow">
                    <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/40">
                        <SearchIcon className="w-5 h-5"/>
                    </span>
                    <input type="text" placeholder="Search by name or EP NO..." className="w-full pl-10 pr-4 py-2.5 bg-cream border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black placeholder:text-black/50" />
                </div>
                 <input type="date" className="w-full md:w-auto px-4 py-2.5 bg-cream border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black" />
                 <input type="date" className="w-full md:w-auto px-4 py-2.5 bg-cream border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition text-black" />
                 <button className="w-full md:w-auto bg-black text-cream px-6 py-2.5 rounded-xl font-semibold hover:bg-black/80 transition">Filter</button>
            </div>
        </Card>

        <div className="md:hidden">
             {MOCK_ATTENDANCE_DATA.map((record) => (
                <Card key={record.id} className="mb-4 !p-4">
                    <div className="flex justify-between items-start">
                        <div>
                             <p className="font-bold text-black">{record.name}</p>
                             <p className="text-sm text-black/60">{record.id}</p>
                        </div>
                         <Badge className={statusStyles[record.status]}>
                            {record.status}
                        </Badge>
                    </div>
                    <div className="mt-4 space-y-2 text-sm text-black">
                        <div className="flex justify-between"><span className="font-semibold text-black/70">Company:</span> <Badge className="bg-light-blue text-black">{record.company}</Badge></div>
                        <div className="flex justify-between"><span className="font-semibold text-black/70">Date:</span> <span>{record.date}</span></div>
                        <div className="flex justify-between"><span className="font-semibold text-black/70">Shift:</span> <span>{record.shift}</span></div>
                        <div className="flex justify-between"><span className="font-semibold text-black/70">In:</span> <span>{record.inTime}</span></div>
                        <div className="flex justify-between"><span className="font-semibold text-black/70">Out:</span> <span>{record.outTime}</span></div>
                        <div className="flex justify-between"><span className="font-semibold text-black/70">Overstay:</span> <span>{record.overstay}</span></div>
                    </div>
                    <div className="mt-4 text-right">
                         <button className="p-2 rounded-lg text-cream bg-black hover:opacity-80 transition">
                            <TrashIcon className="w-4 h-4" />
                        </button>
                    </div>
                </Card>
             ))}
        </div>

        <Card padding="p-0" className="hidden md:block">
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-black">
                    <thead className="text-xs text-black uppercase bg-light-blue">
                        <tr>
                            <th scope="col" className="px-6 py-4"><UserIcon className="w-5 h-5 inline-block mr-2"/>Name</th>
                            <th scope="col" className="px-6 py-4"><BuildingIcon className="w-5 h-5 inline-block mr-2"/>Company</th>
                            <th scope="col" className="px-6 py-4"><CalendarIcon className="w-5 h-5 inline-block mr-2"/>Date</th>
                            <th scope="col" className="px-6 py-4"><ClockIcon className="w-5 h-5 inline-block mr-2"/>Shift</th>
                            <th scope="col" className="px-6 py-4"><CheckIcon className="w-5 h-5 inline-block mr-2"/>Status</th>
                            <th scope="col" className="px-6 py-4"><SignInIcon className="w-5 h-5 inline-block mr-2"/>In</th>
                            <th scope="col" className="px-6 py-4"><SignOutIcon className="w-5 h-5 inline-block mr-2"/>Out</th>
                            <th scope="col" className="px-6 py-4"><HourglassIcon className="w-5 h-5 inline-block mr-2"/>Overstay</th>
                            <th scope="col" className="px-6 py-4"><CogIcon className="w-5 h-5 inline-block mr-2"/>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {MOCK_ATTENDANCE_DATA.map((record) => (
                            <tr key={record.id} className="bg-cream border-b border-light-blue hover:bg-light-blue/40 transition-colors duration-200">
                                <td className="px-6 py-4 font-semibold text-black">
                                    {record.name}
                                    <span className="block font-normal text-black/60">{record.id}</span>
                                </td>
                                <td className="px-6 py-4">
                                    <Badge className="bg-light-blue text-black">{record.company}</Badge>
                                </td>
                                <td className="px-6 py-4">{record.date}</td>
                                <td className="px-6 py-4">{record.shift}</td>
                                <td className="px-6 py-4">
                                    <Badge className={statusStyles[record.status]}>
                                        {record.status}
                                    </Badge>
                                </td>
                                <td className="px-6 py-4">{record.inTime}</td>
                                <td className="px-6 py-4">{record.outTime}</td>
                                <td className="px-6 py-4">{record.overstay}</td>
                                <td className="px-6 py-4">
                                    <button className="p-2 rounded-lg text-cream bg-black hover:opacity-80 transition">
                                        <TrashIcon className="w-4 h-4" />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </Card>
    </div>
    );
};

export default ViewDataPage;