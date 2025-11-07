'use client';

import { Document } from '@/lib/api';
import { useState } from 'react';
import { FileText, Clock, Layers, Trash2, Loader2 } from 'lucide-react';
import Modal from './Modal';

interface DocumentListProps {
  documents: Document[];
  onDelete: (documentId: string) => Promise<void>;
  onSelectDocument: (document: Document) => void;
  selectedDocumentId?: string;
}

export default function DocumentList({
  documents,
  onDelete,
  onSelectDocument,
  selectedDocumentId,
}: DocumentListProps) {
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [documentToDelete, setDocumentToDelete] = useState<string | null>(null);

  const handleDelete = async (e: React.MouseEvent, documentId: string) => {
    e.stopPropagation();
    setDocumentToDelete(documentId);
    setShowDeleteModal(true);
  };

  const confirmDelete = async () => {
    if (!documentToDelete) return;

    setDeletingId(documentToDelete);
    try {
      await onDelete(documentToDelete);
    } catch (error) {
      setShowErrorModal(true);
    } finally {
      setDeletingId(null);
      setDocumentToDelete(null);
    }
  };

  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateString;
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return 'Unknown size';
    const mb = bytes / 1024 / 1024;
    if (mb < 1) {
      return `${(bytes / 1024).toFixed(2)} KB`;
    }
    return `${mb.toFixed(2)} MB`;
  };

  if (documents.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-gray-200 mb-3">
          <FileText className="h-6 w-6 text-gray-400" />
        </div>
        <h3 className="text-lg font-semibold text-gray-900">No documents yet</h3>
        <p className="mt-2 text-base text-gray-600 max-w-sm mx-auto">
          Upload your first document to start asking questions and getting AI-powered answers.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {documents.map((doc) => (
        <div
          key={doc.id}
          onClick={() => onSelectDocument(doc)}
          className={`group p-4 rounded-xl cursor-pointer transition-all duration-200 bg-white shadow-sm ${
            selectedDocumentId === doc.id
              ? 'ring-2 ring-blue-500'
              : 'hover:shadow-md'
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1 min-w-0">
              <div className="flex items-center space-x-3">
                <div className={`flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center ${
                  selectedDocumentId === doc.id ? 'bg-blue-100' : 'bg-gray-100 group-hover:bg-blue-50'
                }`}>
                  <FileText className={`h-5 w-5 ${selectedDocumentId === doc.id ? 'text-blue-600' : 'text-gray-500'}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-semibold text-gray-900 truncate">
                    {doc.filename}
                  </h3>
                  <div className="mt-1.5 flex items-center space-x-4 text-sm text-gray-500">
                    <span className="flex items-center">
                      <Clock className="h-3.5 w-3.5 mr-1.5" />
                      {formatDate(doc.upload_time)}
                    </span>
                    <span className="flex items-center">
                      <Layers className="h-3.5 w-3.5 mr-1.5" />
                      {doc.chunk_count} chunks
                    </span>
                    <span className="flex items-center">
                      <FileText className="h-3.5 w-3.5 mr-1.5" />
                      {formatFileSize(doc.file_size)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            
            <button
              onClick={(e) => handleDelete(e, doc.id)}
              disabled={deletingId === doc.id}
              className="ml-4 p-2 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 focus:outline-none disabled:opacity-50 transition-colors"
              title="Delete document"
            >
              {deletingId === doc.id ? (
                <Loader2 className="animate-spin h-4 w-4" />
              ) : (
                <Trash2 className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>
      ))}

      {/* Delete Confirmation Modal */}
      <Modal
        isOpen={showDeleteModal}
        onClose={() => setShowDeleteModal(false)}
        title="Delete Document"
        message="Are you sure you want to delete this document? This action cannot be undone."
        type="confirm"
        onConfirm={confirmDelete}
        confirmText="Delete"
        cancelText="Cancel"
      />

      {/* Error Modal */}
      <Modal
        isOpen={showErrorModal}
        onClose={() => setShowErrorModal(false)}
        title="Error"
        message="Failed to delete document. Please try again."
        type="alert"
      />
    </div>
  );
}
