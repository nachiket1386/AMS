import React from 'react';
import Card from '../components/Card';
import Badge from '../components/Badge';
import { MOCK_UPLOAD_LOGS } from '../constants';
import { LogsIcon, FileIcon, UserIcon, BuildingIcon, CalendarIcon, CheckIcon, SyncIcon, WarningIcon } from '../constants';

const UploadLogsPage: React.FC = () => {
    return (
    <div className="space-y-8">
        <div>
            <h1 className="text-2xl md:text-4xl font-extrabold text-black flex items-center gap-3">
                <LogsIcon className="w-8 h-8"/>
                Upload Logs
            </h1>
            <p className="text-black/70 mt-1 hidden md:block">Track all CSV upload activities and results.</p>
        </div>
        <Card padding="p-0">
            <div className="overflow-x-auto">
                <table className="w-full text-sm text-left text-black mobile-card-view">
                    <thead className="text-xs text-black uppercase bg-light-blue">
                        <tr>
                            <th scope="col" className="px-6 py-4"><FileIcon className="w-5 h-5 inline-block mr-2"/>File Name</th>
                            <th scope="col" className="px-6 py-4"><UserIcon className="w-5 h-5 inline-block mr-2"/>Uploaded By</th>
                            <th scope="col" className="px-6 py-4"><BuildingIcon className="w-5 h-5 inline-block mr-2"/>Company</th>
                            <th scope="col" className="px-6 py-4"><CalendarIcon className="w-5 h-5 inline-block mr-2"/>Date</th>
                            <th scope="col" className="px-6 py-4 text-center">Metrics</th>
                        </tr>
                    </thead>
                    <tbody>
                        {MOCK_UPLOAD_LOGS.map((log) => (
                            <tr key={log.id} className="bg-cream border-b border-light-blue hover:bg-light-blue/40 transition-colors">
                                <td data-label="File Name" className="px-6 py-4 font-semibold text-black flex items-center gap-2">
                                    <FileIcon className="w-5 h-5 text-dark-blue"/> {log.fileName}
                                </td>
                                <td data-label="Uploaded By" className="px-6 py-4">{log.uploadedBy}</td>
                                <td data-label="Company" className="px-6 py-4">
                                     <Badge className="bg-light-blue text-black">{log.company}</Badge>
                                </td>
                                <td data-label="Date" className="px-6 py-4">{log.date}</td>
                                <td data-label="Metrics" className="px-6 py-4">
                                    <div className="flex items-center justify-end md:justify-center gap-2 flex-wrap">
                                        <Badge className="bg-light-blue text-black">Total: {log.total}</Badge>
                                        <Badge className="bg-dark-blue text-cream"><CheckIcon className="w-4 h-4"/> Success: {log.success}</Badge>
                                        <Badge className="bg-light-blue text-black"><SyncIcon className="w-4 h-4"/> Updated: {log.updated}</Badge>
                                        {log.errors > 0 ? (
                                            <Badge className="bg-cream text-black border border-black"><WarningIcon className="w-4 h-4"/> Errors: {log.errors}</Badge>
                                        ) : null }
                                    </div>
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

export default UploadLogsPage;