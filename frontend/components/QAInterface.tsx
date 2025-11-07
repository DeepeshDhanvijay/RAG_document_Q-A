'use client';

import { useState } from 'react';
import { apiService, QueryResponse, Document } from '@/lib/api';
import { HelpCircle, FileText, Loader2, ChevronDown, X } from 'lucide-react';

interface QAInterfaceProps {
  selectedDocument: Document | null;
  onRemoveDocument?: () => void;
}

export default function QAInterface({ selectedDocument, onRemoveDocument }: QAInterfaceProps) {
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [responses, setResponses] = useState<QueryResponse[]>([]);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedDocument || !question.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await apiService.queryDocument(
        selectedDocument.id,
        question.trim()
      );
      
      setResponses((prev) => [response, ...prev]);
      setQuestion('');
    } catch (err: any) {
      setError(err.response?.data?.error || err.message || 'Failed to get answer');
    } finally {
      setLoading(false);
    }
  };

  if (!selectedDocument) {
    return (
      <div className="text-center py-16">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-200 mb-3">
          <HelpCircle className="h-8 w-8 text-gray-400" />
        </div>
        <h3 className="mt-2 text-lg font-medium text-gray-900">No document selected</h3>
        <p className="mt-1 text-base text-gray-500">
          Select a document from the list to ask questions.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Document Info */}
      <div className="bg-blue-50 rounded-lg p-4 mb-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <FileText className="h-5 w-5 text-blue-600" />
            <div>
              <p className="text-base font-medium text-blue-900">
                Asking about: {selectedDocument.filename}
              </p>
              <p className="text-sm text-blue-700">
                {selectedDocument.chunk_count} chunks available
              </p>
            </div>
          </div>
          {onRemoveDocument && (
            <button
              onClick={onRemoveDocument}
              className="p-2 hover:bg-blue-100 rounded-full transition-colors"
              title="Remove document"
            >
              <X className="h-5 w-5 text-blue-600" />
            </button>
          )}
        </div>
      </div>

      {/* Question Form */}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="question" className="block text-base font-medium text-gray-700 mb-2">
            Ask a question
          </label>
          <textarea
            id="question"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="e.g., What is the main conclusion of this document?"
            rows={3}
            className="w-full px-4 py-3 text-base text-gray-900 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={!question.trim() || loading}
          className="w-full bg-gradient-to-r from-purple-500 to-indigo-500 text-white px-6 py-3 text-base font-semibold rounded-lg shadow-md hover:shadow-[0_0_15px_rgba(139,92,246,0.6)] hover:opacity-90 transition focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-md disabled:hover:opacity-50"
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <Loader2 className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" />
              Processing...
            </span>
          ) : (
            'Get Answer'
          )}
        </button>
      </form>

      {error && (
        <div className="p-4 bg-red-50 rounded-md">
          <p className="text-base text-red-600">{error}</p>
        </div>
      )}

      {/* Responses */}
      {responses.length > 0 && (
        <div className="space-y-6">
          <h3 className="text-xl font-semibold text-gray-900">Q&A History</h3>
          {responses.map((response, index) => (
            <div key={index} className="rounded-lg overflow-hidden bg-white/50 backdrop-blur-sm">
              {/* Question */}
              <div className="bg-gray-50 px-4 py-3">
                <div className="flex items-start space-x-3">
                  <HelpCircle className="h-5 w-5 text-gray-600 mt-0.5 flex-shrink-0" />
                  <p className="text-base font-medium text-gray-900">{response.question}</p>
                </div>
              </div>

              {/* Answer */}
              <div className="px-4 py-4 bg-white/80">
                <div className="prose prose-sm max-w-none">
                  <p className="text-base text-gray-800 leading-relaxed whitespace-pre-wrap">{response.answer}</p>
                </div>

                <div className="mt-4 text-sm text-gray-500">
                  Processing time: {response.processing_time}s
                </div>
              </div>

              {/* Sources */}
              {response.sources && response.sources.length > 0 && (
                <div className="px-4 py-3 bg-gray-50">
                  <details className="group">
                    <summary className="cursor-pointer text-base font-medium text-gray-700 hover:text-gray-900 flex items-center justify-between">
                      <span>Source References ({response.sources.length})</span>
                      <ChevronDown className="h-5 w-5 text-gray-500 group-open:rotate-180 transition-transform" />
                    </summary>
                    <div className="mt-3 space-y-3">
                      {response.sources.map((source, sourceIndex) => (
                        <div
                          key={sourceIndex}
                          className="p-3 bg-white/80 rounded text-sm"
                        >
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-medium text-gray-700 text-sm">
                              Chunk {source.chunk_index + 1}
                            </span>
                            <span className="text-sm text-gray-500">
                              Relevance: {(source.relevance_score * 100).toFixed(1)}%
                            </span>
                          </div>
                          <p className="text-gray-600 text-sm leading-relaxed">
                            {source.chunk_text}
                          </p>
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
