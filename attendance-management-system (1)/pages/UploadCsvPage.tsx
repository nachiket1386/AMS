import React, { useState } from 'react';
import Card from '../components/Card';
import SolidButton from '../components/GradientButton';
import { UploadIcon, InfoIcon, BuildingIcon } from '../constants';

const UploadCsvPage: React.FC = () => {
    const [fileName, setFileName] = useState<string | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [uploadSuccess, setUploadSuccess] = useState(false);

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files.length > 0) {
            setFileName(event.target.files[0].name);
            setUploadSuccess(false);
        }
    };

    const handleUpload = () => {
        if (!fileName) return;
        setIsUploading(true);
        setUploadSuccess(false);
        setTimeout(() => {
            setIsUploading(false);
            setUploadSuccess(true);
            setFileName(null);
        }, 2000);
    };

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl md:text-4xl font-extrabold text-black flex items-center gap-3">
                    <UploadIcon className="w-8 h-8"/>
                    Upload CSV
                </h1>
                <p className="text-black/70 mt-1 hidden md:block">Upload your attendance data in CSV format.</p>
            </div>

            {uploadSuccess && (
                <div className="bg-dark-blue/20 border border-dark-blue text-black p-4 rounded-lg" role="alert">
                    <p className="font-bold">Success</p>
                    <p>File uploaded and processed successfully.</p>
                </div>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2">
                    <Card>
                        <div className="space-y-6">
                            <div>
                                <label className="text-sm font-semibold text-black/80">Company</label>
                                <div className="relative mt-2">
                                     <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-black/50">
                                        <BuildingIcon className="w-5 h-5"/>
                                     </span>
                                     <select className="w-full pl-10 pr-4 py-3 border border-light-blue rounded-xl focus:ring-2 focus:ring-dark-blue focus:border-transparent transition bg-cream text-black appearance-none">
                                        <option>Innovate Inc.</option>
                                        <option>Tech Solutions</option>
                                        <option>Future Corp</option>
                                     </select>
                                </div>
                            </div>
                            <div>
                                <label className="text-sm font-semibold text-black/80">CSV File</label>
                                <div className="mt-2 flex justify-center px-6 pt-5 pb-6 border-2 border-light-blue border-dashed rounded-2xl">
                                    <div className="space-y-1 text-center">
                                        <UploadIcon className="mx-auto h-12 w-12 text-black/40" />
                                        <div className="flex text-sm text-black/80">
                                            <label htmlFor="file-upload" className="relative cursor-pointer bg-transparent rounded-md font-medium text-dark-blue hover:text-black focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-dark-blue">
                                                <span>Upload a file</span>
                                                <input id="file-upload" name="file-upload" type="file" className="sr-only" accept=".csv" onChange={handleFileChange} />
                                            </label>
                                            <p className="pl-1">or drag and drop</p>
                                        </div>
                                        <p className="text-xs text-black/60">CSV up to 10MB</p>
                                    </div>
                                </div>
                                {fileName && <p className="mt-2 text-sm text-black/80">Selected file: <span className="font-semibold">{fileName}</span></p>}
                            </div>
                            <SolidButton onClick={handleUpload} disabled={!fileName || isUploading} className="w-full !py-4 text-base">
                                {isUploading ? 'Uploading...' : 'Upload File'}
                            </SolidButton>
                        </div>
                    </Card>
                </div>
                <div>
                     <div className="bg-light-blue border border-dark-blue/50 p-6 rounded-2xl space-y-4 h-full">
                        <div className="flex items-center gap-3">
                            <InfoIcon className="w-6 h-6 text-dark-blue" />
                            <h3 className="text-lg font-bold text-black">Format Requirements</h3>
                        </div>
                        <div className="space-y-4 text-sm text-black/90">
                           <div>
                                <h4 className="font-semibold mb-1">📋 Required Columns</h4>
                                <p><code>EP NO</code>, <code>Name</code>, <code>Date</code>, <code>Status</code>, <code>In</code>, <code>Out</code></p>
                           </div>
                           <div>
                                <h4 className="font-semibold mb-1">📝 Optional Columns</h4>
                                <p><code>Company</code>, <code>Shift</code>, <code>Overstay</code></p>
                           </div>
                           <div>
                                <h4 className="font-semibold mb-1">✅ Format Rules</h4>
                                <ul className="list-disc list-inside space-y-1">
                                    <li>Date format: YYYY-MM-DD</li>
                                    <li>Time format: HH:MM (24-hour)</li>
                                    <li>Status must be one of: Present, Absent, Holiday, Half Day</li>
                                </ul>
                           </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UploadCsvPage;