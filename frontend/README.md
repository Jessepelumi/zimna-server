This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Zimna AI

Zimna AI is a personalized productivity application that helps users break down their goals into actionable objectives and tasks using AI-powered goal decomposition.

### Features

- **Goal Input**: Enter your goals in natural language
- **AI Decomposition**: Automatically break down goals into manageable objectives
- **Dashboard**: View and manage your goals and objectives
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: TanStack Query for server state
- **Icons**: Phosphor Icons and Lucide React
- **Backend**: REST API integration

## Getting Started

### Prerequisites

- Node.js 18+
- npm, yarn, pnpm, or bun

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd zimna-ai
```

2. Install dependencies:

```bash
npm install
# or
yarn install
# or
pnpm install
# or
bun install
```

3. Set up environment variables:
   Create a `.env.local` file in the root directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_ZIMNA_AUTH=<your-basic-auth-token>
```

### Running the Development Server

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

The page auto-updates as you edit the file.

### Building for Production

```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/
│   ├── (dashboard)/
│   │   ├── goals/page.tsx
│   │   ├── home/page.tsx
│   │   └── objectives/page.tsx
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── custom/
│   │   ├── examplePrompt.tsx
│   │   ├── sectionHeader.tsx
│   │   ├── sidebar.tsx
│   │   └── sidebarItem.tsx
│   ├── providers/
│   │   └── QueryProvider.tsx
│   └── ui/
│       ├── button.tsx
│       ├── input.tsx
│       └── sheet.tsx
├── lib/
│   ├── api.ts
│   └── utils.ts
└── static/
    └── examplePrompts.tsx
```

## API Integration

The app integrates with a backend API for goal decomposition. The API endpoint expects:

- **Endpoint**: `/decompose/`
- **Method**: POST
- **Body**: `{ "text": "your goal text" }`
- **Auth**: Basic Auth using `NEXT_PUBLIC_ZIMNA_AUTH`

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
