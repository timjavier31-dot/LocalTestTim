# Full Stack Next.js Project

This project includes:

- Frontend built with Next.js App Router
- Welcome login page at `/`
- Backend SQL Server login API route at `src/app/api/login/route.ts`
- Tailwind CSS styling
- TypeScript and ESLint support

## SQL Server connection

The app is configured to connect to Microsoft SQL Server Express at `DESKTOP-5IK0H2G\\SQLEXPRESS` using Windows authentication.

When the login form is used, the backend will ensure a database named `TestApp` exists and a table named `Users` exists for user lookup.

The login API checks whether the submitted domain and username exist in `TestApp.Users` and verifies the password before returning a success or failure message.

## Available commands

- `npm install`
- `npm run dev`
- `npm run build`
- `npm start`
- `npm run lint`
