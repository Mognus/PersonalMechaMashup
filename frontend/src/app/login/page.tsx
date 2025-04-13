import LoginForm from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    // Page container styling
    <div className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-br from-slate-900 to-zinc-900 p-4">
      {/* Page Title */}
      <h1 className="mb-8 text-4xl font-bold text-slate-200 tracking-tighter">Mech Interface Login</h1>
      {/* Form container styling */}
      <div className="w-full max-w-md rounded-lg border border-slate-700 bg-slate-800/50 p-6 shadow-xl backdrop-blur-sm">
         {/* Render the actual login form component */}
         <LoginForm />
      </div>
      {/* Optional: Link for registration or help */}
      {/* <p className="mt-4 text-sm text-slate-400">Need access? Contact Administrator.</p> */}
    </div>
  );
}