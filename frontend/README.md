# Soutenance Manager - Frontend

Student Dashboard for managing soutenance requests built with Next.js, React, and TypeScript.

## Features

- 📊 Student Dashboard with statistics
- 📝 Soutenance request form
- 📄 PDF report upload with drag-and-drop
- 🤖 AI module integration (summary, classification, similarity)
- 📋 Request history and status tracking
- 🎨 Modern UI with Tailwind CSS

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn

### Installation

1. Install dependencies:

```bash
npm install
# or
yarn install
```

2. Create a `.env.local` file (optional):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:

```bash
npm run dev
# or
yarn dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/              # Next.js app directory
│   ├── layout.tsx    # Root layout
│   ├── page.tsx      # Home page
│   └── globals.css   # Global styles
├── components/       # React components
│   ├── StudentDashboard.tsx
│   ├── SoutenanceRequestForm.tsx
│   ├── PDFUpload.tsx
│   └── RequestHistory.tsx
├── services/         # API services
│   └── api.ts
├── types/           # TypeScript types
│   └── soutenance.ts
└── public/          # Static assets
```

## Components

### StudentDashboard
Main dashboard component displaying statistics and request management.

### SoutenanceRequestForm
Form for submitting new soutenance requests with title, domain, and PDF upload.

### PDFUpload
Drag-and-drop PDF upload component with validation.

### RequestHistory
Displays all student requests with status, AI summary, and similarity scores.

## API Integration

The frontend expects the following backend endpoints:

- `POST /api/students/soutenance-requests` - Submit new request
- `GET /api/students/soutenance-requests` - Get all student requests
- `GET /api/students/dashboard` - Get dashboard statistics

## Build for Production

```bash
npm run build
npm start
```

## Technologies

- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **react-dropzone** - File upload
- **lucide-react** - Icons
- **date-fns** - Date formatting

