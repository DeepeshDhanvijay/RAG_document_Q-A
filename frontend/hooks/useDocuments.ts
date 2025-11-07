'use client';

import { useState, useCallback } from 'react';
import { apiService, Document, UploadResponse } from '@/lib/api';

interface UseDocumentUploadReturn {
  uploading: boolean;
  progress: number;
  error: string | null;
  uploadDocument: (file: File) => Promise<UploadResponse | null>;
  resetError: () => void;
}

export function useDocumentUpload(onSuccess?: () => void): UseDocumentUploadReturn {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const uploadDocument = useCallback(async (file: File): Promise<UploadResponse | null> => {
    setUploading(true);
    setProgress(0);
    setError(null);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const response = await apiService.uploadDocument(file);
      
      clearInterval(progressInterval);
      setProgress(100);
      
      if (onSuccess) {
        onSuccess();
      }
      
      setTimeout(() => {
        setUploading(false);
        setProgress(0);
      }, 500);

      return response;
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'Upload failed');
      setUploading(false);
      setProgress(0);
      return null;
    }
  }, [onSuccess]);

  const resetError = useCallback(() => {
    setError(null);
  }, []);

  return { uploading, progress, error, uploadDocument, resetError };
}

interface UseDocumentsReturn {
  documents: Document[];
  loading: boolean;
  error: string | null;
  refreshDocuments: () => Promise<void>;
  deleteDocument: (documentId: string) => Promise<void>;
}

export function useDocuments(): UseDocumentsReturn {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const refreshDocuments = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const docs = await apiService.getDocuments();
      setDocuments(docs);
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'Failed to load documents');
    } finally {
      setLoading(false);
    }
  }, []);

  const deleteDocument = useCallback(async (documentId: string) => {
    try {
      await apiService.deleteDocument(documentId);
      setDocuments((prev) => prev.filter((doc) => doc.id !== documentId));
    } catch (err: any) {
      throw new Error(err.response?.data?.error || err.message || 'Failed to delete document');
    }
  }, []);

  return { documents, loading, error, refreshDocuments, deleteDocument };
}
