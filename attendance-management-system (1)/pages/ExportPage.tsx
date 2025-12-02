import React, { useState } from 'react';
import Card from '../components/Card';
import SolidButton from '../components/GradientButton';
import { ExportIcon, BuildingIcon, CalendarIcon, FileIcon, ClockIcon } from '../constants';

const ExportPage: React.FC = () => {
    const [isGenerating, setIsGenerating] = useState(false);

    const handleGenerate = () => {
        setIsGenerating(true);
        setTimeout(() => {
            setIsGenerating(false);
            // In a real app, this would trigger a download.
            alert('Report generated and download started!');
        }, 2000);
    };

    const recentExports = [
        { id: 1, name: 'Monthly_Summary_Oct_2023.csv', date: '2023-11-01 10:15 AM' },
        { id: 2, name: 'Daily_Attendance_2023-10-31.pdf', date: '2023-10-31 05:00 PM' },
        { id: 3, name: 'Innovate_Inc_Report.csv', date: '2023-10-30 09:30 AM' },
    ];

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl md:text-4xl font-extrabold text-black flex items-center gap-3">
                    <ExportIcon className="w-8 h-8"/>
                    Export Data
                </h1>
                <p className="text-black/70 mt-1 hidden md:block">Generate and download attendance reports.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
                <div className="lg:col-span-2">
                    <Card>
                        <h2 className="text-xl font-bold text-black mb-6">Report Options</h2>
                        <div className="space-y-6">
                            {/* Report Type */}
                            <div>
                                <label className="text-sm font-semibold text-black/80">Report Type</label>
                                <div className="relative mt-2">
                                     <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/50">
                                        <FileIcon className="w-5 h-5"/>
                                     </span>
                                     <select className="w-full pl-10 pr-4 py-3 border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition bg-cream text-black appearance-none">
                                        <option>Daily Attendance Report</option>
                                        <option>Monthly Summary</option>
                                        <option>Employee Performance</option>
                                     </select>
                                </div>
                            </div>

                            {/* Company */}
                            <div>
                                <label className="text-sm font-semibold text-black/80">Company</label>
                                <div className="relative mt-2">
                                     <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/50">
                                        <BuildingIcon className="w-5 h-5"/>
                                     </span>
                                     <select className="w-full pl-10 pr-4 py-3 border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition bg-cream text-black appearance-none">
                                        <option>All Companies</option>
                                        <option>Innovate Inc.</option>
                                        <option>Tech Solutions</option>
                                        <option>Future Corp</option>
                                     </select>
                                </div>
                            </div>

                            {/* Date Range */}
                            <div>
                                <label className="text-sm font-semibold text-black/80">Date Range</label>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
                                    <div className="relative">
                                        <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/50"><CalendarIcon className="w-5 h-5"/></span>
                                        <input type="date" defaultValue="2023-10-01" className="w-full pl-10 pr-4 py-3 border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition bg-cream text-black"/>
                                    </div>
                                    <div className="relative">
                                        <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/50"><CalendarIcon className="w-5 h-5"/></span>
                                        <input type="date" defaultValue="2023-10-31" className="w-full pl-10 pr-4 py-3 border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition bg-cream text-black"/>
                                    </div>
                                </div>
                            </div>

                            {/* File Format */}
                             <div>
                                <label className="text-sm font-semibold text-black/80 mb-2 block">File Format</label>
                                <div className="flex gap-4">
                                    <button className="flex-1 text-center py-3 rounded-xl border-2 border-dark-blue bg-dark-blue text-cream font-semibold">CSV</button>
                                    <button className="flex-1 text-center py-3 rounded-xl border-2 border-light-blue text-black font-semibold hover:border-dark-blue transition">PDF</button>
                                </div>
                            </div>
                            
                            <SolidButton onClick={handleGenerate} disabled={isGenerating} className="w-full !py-4 text-base">
                                {isGenerating ? 'Generating...' : 'Generate & Download'}
                            </SolidButton>
                        </div>
                    </Card>
                </div>
                
                {/* Recent Exports */}
                <div>
                    <Card>
                        <div className="flex items-center gap-3 mb-4">
                            <ClockIcon className="w-6 h-6 text-dark-blue" />
                            <h3 className="text-lg font-bold text-black">Recent Exports</h3>
                        </div>
                        <ul className="space-y-3">
                           {recentExports.map(exp => (
                                <li key={exp.id} className="p-3 bg-light-blue/50 rounded-lg">
                                    <p className="font-semibold text-black text-sm truncate">{exp.name}</p>
                                    <p className="text-xs text-black/70 mt-1">{exp.date}</p>
                                </li>
                           ))}
                        </ul>
                    </Card>
                </div>
            </div>
        </div>
    );
};

export default ExportPage;