'use client';

import { X } from 'lucide-react';
import { useEffect } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  message: string;
  type?: 'confirm' | 'alert';
  onConfirm?: () => void;
  confirmText?: string;
  cancelText?: string;
}

export default function Modal({
  isOpen,
  onClose,
  title,
  message,
  type = 'alert',
  onConfirm,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
}: ModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      ></div>

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white rounded-xl shadow-2xl max-w-md w-full p-6 transform transition-all">
          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 text-gray-400 hover:text-gray-600 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>

          {/* Title */}
          <h3 className="text-xl font-semibold text-gray-900 mb-3 pr-8">
            {title}
          </h3>

          {/* Message */}
          <p className="text-base text-gray-600 mb-6">
            {message}
          </p>

          {/* Buttons */}
          <div className="flex justify-end space-x-3">
            {type === 'confirm' && (
              <>
                <button
                  onClick={onClose}
                  className="px-4 py-2 text-base font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-300"
                >
                  {cancelText}
                </button>
                <button
                  onClick={() => {
                    onConfirm?.();
                    onClose();
                  }}
                  className="px-4 py-2 text-base font-medium text-white bg-gradient-to-r from-purple-500 to-indigo-500 rounded-lg hover:shadow-[0_0_15px_rgba(139,92,246,0.6)] hover:opacity-90 transition focus:outline-none"
                >
                  {confirmText}
                </button>
              </>
            )}
            {type === 'alert' && (
              <button
                onClick={onClose}
                className="px-4 py-2 text-base font-medium text-white bg-gradient-to-r from-purple-500 to-indigo-500 rounded-lg hover:shadow-[0_0_15px_rgba(139,92,246,0.6)] hover:opacity-90 transition focus:outline-none"
              >
                OK
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
