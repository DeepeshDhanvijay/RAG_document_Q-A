'use client';

import { useState, useEffect } from 'react';
import FileUpload from '@/components/FileUpload';
import DocumentList from '@/components/DocumentList';
import QAInterface from '@/components/QAInterface';
import { useDocuments } from '@/hooks/useDocuments';
import { Document } from '@/lib/api';

export default function Home() {
  const { documents, loading, refreshDocuments, deleteDocument } = useDocuments();
  const [selectedDocument, setSelectedDocument] = useState<Document | null>(null);

  useEffect(() => {
    refreshDocuments();
  }, [refreshDocuments]);

  const handleUploadSuccess = () => {
    refreshDocuments();
  };

  const handleSelectDocument = (doc: Document) => {
    setSelectedDocument(doc);
  };

  const handleDeleteDocument = async (documentId: string) => {
    await deleteDocument(documentId);
    if (selectedDocument?.id === documentId) {
      setSelectedDocument(null);
    }
  };

  const handleRemoveDocument = () => {
    setSelectedDocument(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-indigo-500 via-purple-500 to-fuchsia-500 text-white">
      {/* Header */}
      <header className="bg-white/10 backdrop-blur-md border-b border-white/20 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-white" style={{ fontFamily: 'Poppins, sans-serif' }}>Smart Document Q&A</h1>
            <p className="text-base text-purple-100" style={{ fontFamily: 'Poppins, sans-serif' }}>
              Upload documents and ask questions using AI
            </p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        {/* Top Row - Upload & Documents Side by Side */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Upload Section */}
          <section className="p-4">
            <h2 className="text-lg font-semibold text-white mb-4">
              Upload Document
            </h2>
            <FileUpload onUploadSuccess={handleUploadSuccess} />
          </section>

          {/* Documents Section */}
          <section className="p-4">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-white">
                My Documents
              </h2>
              {!loading && documents.length > 0 && (
                <span className="text-sm text-gray-600">
                  {documents.length} document{documents.length !== 1 ? 's' : ''}
                </span>
              )}
            </div>

            {loading && documents.length === 0 ? (
              <div className="flex justify-center items-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
              </div>
            ) : (
              <DocumentList
                documents={documents}
                onDelete={handleDeleteDocument}
                onSelectDocument={handleSelectDocument}
                selectedDocumentId={selectedDocument?.id}
              />
            )}
          </section>
        </div>

        {/* Bottom Row - Q&A Interface */}
        <section className="p-4 mb-8">
          <h2 className="text-lg font-semibold text-white mb-4">
            Ask Questions
          </h2>
          <QAInterface 
            selectedDocument={selectedDocument} 
            onRemoveDocument={handleRemoveDocument}
          />
        </section>

        {/* Instructions Section */}
        <div className="mt-8 p-4">
          <h3 className="text-lg font-semibold text-black mb-4">How to use this tool</h3>
          <ol className="list-decimal list-inside space-y-2 text-base text-black">
            <li>Upload a PDF or TXT document using the upload area above</li>
            <li>Wait for the document to be processed (usually takes a few seconds)</li>
            <li>Select a document from your list</li>
            <li>Type your question in the Q&A interface</li>
            <li>Get AI-powered answers based on your document content</li>
          </ol>
          <div className="mt-4 pt-4">
            <p className="text-base text-black">
              <strong>Example questions:</strong> "What is the main conclusion?", 
              "What are the key recommendations?", "What percentage increase was reported?"
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-base text-gray-600">
            Powered by RAG (Retrieval-Augmented Generation) • FastAPI + Next.js + Groq + FAISS
          </p>
        </div>
      </footer>
    </div>
  );
}
