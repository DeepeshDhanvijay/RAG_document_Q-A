# Screenshots

This folder contains screenshots of the RAG Document Q&A application.

## Required Screenshots

To complete the documentation, please add the following screenshots:

1. **home.png** - Home page with upload interface
2. **documents.png** - Document list showing uploaded files
3. **qa-interface.png** - Q&A interface with question input
4. **sources.png** - Answer with expanded source references
5. **upload-progress.png** - File upload progress bar
6. **error-modal.png** - Custom error modal
7. **mobile-view.png** - Responsive mobile layout
8. **api-docs.png** - FastAPI Swagger UI at http://localhost:8000/docs

## How to Take Screenshots

1. **Start the application**:
   - Backend: `cd backend && python main.py`
   - Frontend: `cd frontend && npm run dev`

2. **Navigate to http://localhost:3000**

3. **Capture screenshots**:
   - **Home Page**: Take screenshot of initial landing page
   - **Upload Document**: Drag a PDF/TXT file and capture the upload area
   - **Document List**: After uploading, capture the "My Documents" section
   - **Q&A Interface**: Select a document and capture the question input area
   - **Answer with Sources**: Ask a question, wait for response, expand source references
   - **Progress**: Capture during file upload (progress bar visible)
   - **Error**: Try uploading an invalid file to trigger error modal
   - **Mobile**: Use browser dev tools to simulate mobile device

4. **API Documentation**:
   - Navigate to http://localhost:8000/docs
   - Capture the FastAPI automatic documentation page

## Screenshot Specifications

- **Format**: PNG (preferred) or JPG
- **Dimensions**: 1920x1080 recommended (or actual browser window size)
- **Quality**: High quality, clear text
- **File Size**: Optimize images (use tools like TinyPNG)

## Naming Convention

Use descriptive names matching the list above:
- `home.png`
- `documents.png`
- `qa-interface.png`
- `sources.png`
- `upload-progress.png`
- `error-modal.png`
- `mobile-view.png`
- `api-docs.png`

## Usage in README

Once screenshots are added, update the main README.md to include them:

```markdown
![Home Page](screenshots/home.png)
![Document List](screenshots/documents.png)
![Q&A Interface](screenshots/qa-interface.png)
![Source References](screenshots/sources.png)
```
