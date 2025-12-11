# Smart University Assistant - Frontend (Next.js + Tailwind)

This is a minimal, production-oriented frontend skeleton for the Smart University Assistant.

## Setup

1. Install deps:
```bash
cd sua-frontend
npm install
```

2. Set environment variable:
Create a `.env.local` in the root of this frontend folder:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

3. Run dev server:
```bash
npm run dev
```

4. Connect to the backend:
- Upload endpoint: POST {NEXT_PUBLIC_API_BASE_URL}/upload/file
- Chat endpoint: POST {NEXT_PUBLIC_API_BASE_URL}/chat/query

The UI is intentionally simple but polished with Tailwind. Use this as a starting point and replace components with your preferred UI library (shadcn/ui, Chakra, etc.).
