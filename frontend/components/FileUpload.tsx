'use client';

import { useState, useRef, ChangeEvent } from 'react';
import { useDocumentUpload } from '@/hooks/useDocuments';
import { Upload, FileText, Loader2, AlertCircle } from 'lucide-react';

interface FileUploadProps {
  onUploadSuccess: () => void;
}

export default function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  const { uploading, progress, error, uploadDocument, resetError } = useDocumentUpload(onUploadSuccess);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      resetError();
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedFile(e.dataTransfer.files[0]);
      resetError();
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    
    const result = await uploadDocument(selectedFile);
    if (result) {
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        className={`rounded-xl p-10 text-center transition-all duration-200 ${
          dragActive
            ? 'bg-purple-50 scale-[1.02]'
            : ''
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.txt"
          onChange={handleFileChange}
          className="hidden"
        />
        
        <div className="space-y-4">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-blue-100 mb-3">
            <Upload className="h-8 w-8 text-blue-600" />
          </div>
          
          <div className="text-base text-gray-600">
            <button
              type="button"
              onClick={handleButtonClick}
              className="bg-white text-gray-900 px-5 py-2.5 rounded-lg shadow-md hover:shadow-lg transition font-semibold focus:outline-none border border-gray-200"
            >
              Click to upload
            </button>
            <span className="block mt-2">or drag and drop</span>
          </div>
          
          <p className="text-base text-gray-500">
            PDF or TXT files (up to 10MB)
          </p>
          
          {selectedFile && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-blue-600" />
                  <div className="text-left">
                    <p className="text-base font-semibold text-gray-900">
                      {selectedFile.name}
                    </p>
                    <p className="text-sm text-gray-500">
                      {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
          
          {uploading && (
            <div className="mt-4">
              <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-blue-500 to-blue-600 h-2 rounded-full transition-all duration-300 ease-out"
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
              <p className="text-base font-medium text-gray-700 mt-2 flex items-center justify-center">
                <Loader2 className="animate-spin h-4 w-4 mr-2 text-blue-600" />
                Uploading and processing... {progress}%
              </p>
            </div>
          )}
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 rounded-lg">
              <div className="flex items-start">
                <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-2" />
                <p className="text-base text-red-700 font-medium">{error}</p>
              </div>
            </div>
          )}
          
          {selectedFile && !uploading && (
            <button
              onClick={handleUpload}
              className="mt-4 bg-gradient-to-r from-purple-500 to-indigo-500 text-white px-8 py-3 text-base font-semibold rounded-lg shadow-md hover:shadow-[0_0_15px_rgba(139,92,246,0.6)] hover:opacity-90 transition focus:outline-none"
            >
              Upload Document
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
