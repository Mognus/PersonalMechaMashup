'use client';

import { useEffect } from 'react';
import { useFormState, useFormStatus } from 'react-dom'; // Import hooks for Server Actions
import { useRouter } from 'next/navigation';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { login } from '@/actions/auth';

// Button component aware of the form's pending state
function SubmitButton() {
  const { pending } = useFormStatus(); // Hook to check if the parent form is submitting
  return (
    <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700 text-white" disabled={pending}>
      {pending ? 'Authenticating...' : 'Engage'}
    </Button>
  );
}

// Main Login Form component
const LoginForm = () => {
  const router = useRouter();
  // Initial state for the form action's return value
  const initialState = { success: false, message: "", errors: undefined };
  // `useFormState` manages state based on the Server Action's return value
  // `state` holds the last returned value from the `login` action
  // `formAction` is passed to the form's `action` prop to trigger the server action
  const [state, formAction] = useFormState(login, initialState);

  // Effect hook to handle redirection upon successful login
  useEffect(() => {
    if (state.success) {
      console.log("Login form detected success from server action, redirecting...");
      // Redirect to the home page or dashboard
      router.push('/');
    }
    // No 'else' needed here; error messages are displayed based on the 'state' below
  }, [state, router]); // Re-run the effect if the state or router changes

  return (
    // The form's `action` prop is now connected to our server action handler
    <form action={formAction} className="space-y-4">
      {/* Username Input Section */}
      <div className="grid w-full items-center gap-1.5">
        <Label htmlFor="username" className="text-slate-300">Username / Callsign</Label>
        <Input
          type="text"
          id="username"
          name="username" // `name` attribute is crucial for FormData used by server actions
          placeholder="Enter your callsign"
          required
          className="bg-slate-700/50 border-slate-600 text-slate-200 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500"
          // Input is implicitly disabled when form is pending via SubmitButton's disabled state
        />
         {/* Display field-specific validation errors if returned by the server action */}
        {state.errors?.username && <p className="text-xs text-red-400">{state.errors.username.join(', ')}</p>}
      </div>

      {/* Password Input Section */}
      <div className="grid w-full items-center gap-1.5">
        <Label htmlFor="password" className="text-slate-300">Password</Label>
        <Input
          type="password"
          id="password"
          name="password" // `name` attribute is crucial for FormData
          placeholder="Enter secure password"
          required
          className="bg-slate-700/50 border-slate-600 text-slate-200 placeholder:text-slate-400 focus:border-blue-500 focus:ring-blue-500"
        />
        {/* Display field-specific validation errors */}
        {state.errors?.password && <p className="text-xs text-red-400">{state.errors.password.join(', ')}</p>}
      </div>

      {/* Display general error message from the server action state */}
      {/* Show this only if login failed overall and there are no specific field errors */}
      {!state.success && state.message && !state.errors && (
         <p className="text-sm text-red-400">{state.message}</p>
      )}

      {/* Submit Button Component (uses useFormStatus) */}
      <SubmitButton />
    </form>
  );
};

export default LoginForm;