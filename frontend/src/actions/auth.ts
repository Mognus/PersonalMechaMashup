'use server'; // Marks functions in this file as Server Actions

import { cookies } from 'next/headers';
import { z } from 'zod'; // For optional input validation

// Optional: Schema for validating login data
const LoginSchema = z.object({
  username: z.string().min(1, "Username is required"),
  password: z.string().min(1, "Password is required"),
});

// --- Internal helper function for server-to-server calls to Django ---
// This function runs ONLY on the Next.js server.
async function callDjangoBackend(endpoint: string, method: string, body: any = null, baseUrlType: 'api' | 'auth' = 'api') {
    // Reads backend URLs from server environment variables (or uses default Docker names)
    // IMPORTANT: These variables (DJANGO_AUTH_URL etc.) must be set in the server environment,
    // do NOT use `NEXT_PUBLIC_...` as this is server-to-server.
    const djangoBaseUrl = baseUrlType === 'auth'
        ? process.env.DJANGO_AUTH_URL || 'http://backend:8000/auth' // Internal Docker hostname:port
        : process.env.DJANGO_API_URL || 'http://backend:8000/api';   // Internal Docker hostname:port

    if (!djangoBaseUrl) {
        throw new Error(`Server environment variable for ${baseUrlType === 'auth' ? 'DJANGO_AUTH_URL' : 'DJANGO_API_URL'} not configured.`);
    }
    if (!endpoint.startsWith('/')) {
        endpoint = '/' + endpoint;
    }
    const url = `${djangoBaseUrl}${endpoint.substring(1)}`;
    console.log(`[Server Action] Calling Django: ${method} ${url}`); // Server-side log

    try {
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
            body: body ? JSON.stringify(body) : null,
            cache: 'no-store', // Prevent caching of auth requests
        });

        const responseBody = await response.json().catch(() => null); // Attempt to parse body

        if (!response.ok) {
            console.error(`[Server Action] Django API Error (${response.status}):`, responseBody);
            // Ensure we throw an object with status and detail for consistency
            throw { status: response.status, detail: responseBody?.detail || `Request failed with status ${response.status}` };
        }

        console.log(`[Server Action] Django call ${method} ${url} successful.`);
        return responseBody; // Return parsed body

    } catch (error: any) {
        console.error(`[Server Action] Error calling Django ${method} ${url}:`, error);
        // Ensure we throw an object with 'detail' for consistency
        if (error.detail) {
             throw error;
        } else {
            // Wrap other errors
            throw { status: error.status || 500, detail: error.message || 'Unknown server error calling backend' };
        }
    }
}


// --- Login Server Action ---
// This function is called by the login form.
export async function login(prevState: any, formData: FormData) {
  console.log("[Server Action] 'login' action called.");
  // 1. Validate input (optional but recommended)
  const parseResult = LoginSchema.safeParse(Object.fromEntries(formData.entries()));
  if (!parseResult.success) {
    console.warn("[Server Action] Login input validation failed:", parseResult.error.flatten().fieldErrors);
    return { success: false, message: "Invalid input.", errors: parseResult.error.flatten().fieldErrors };
  }
  const { username, password } = parseResult.data;

  try {
    // 2. Call Django's token endpoint (server-to-server)
    const tokenData = await callDjangoBackend(
       '/token/', // Django endpoint (relative to the auth base URL)
       'POST',
       { username, password },
       'auth' // Use the 'auth' base URL helper
    );

    // 3. Check if tokens are present in the response
    if (!tokenData?.access || !tokenData?.refresh) {
      console.error("[Server Action] Django response missing required tokens:", tokenData);
      throw new Error("Authentication failed: Invalid response from authentication server.");
    }

    // 4. Set HttpOnly cookies using next/headers
    const cookieStore = await cookies();
    cookieStore.set('access_token', tokenData.access, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production', // Use secure flag in production (HTTPS)
      path: '/', // Make accessible across the entire site or specify a more restrictive path like '/api'
      sameSite: 'lax', // Or 'strict'. 'lax' is a good default.
      // maxAge: 60 * 60, // Optional: Set max age in seconds (e.g., 1 hour), align with SIMPLE_JWT settings if needed
    });
    cookieStore.set('refresh_token', tokenData.refresh, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      // Important: Path should ideally only be accessible by the refresh token endpoint
      path: '/api/auth/token/refresh/', // Adjust this path to match your backend's refresh token route!
      sameSite: 'lax',
      // maxAge: 60 * 60 * 24 * 7, // Optional: Longer max age for refresh token (e.g., 7 days)
    });

    console.log(`[Server Action] Set HttpOnly cookies for user: ${username}`);
    // 5. Return success status (can also return user data if Django provides it)
    return { success: true, message: "Login successful!" };

  } catch (error: any) {
    console.error("[Server Action] Login process failed:", error);
    // Extract a user-friendly error message
    const message = error.detail || error.message || "An unknown error occurred during login.";
    // Return error status and message to the client form
    return { success: false, message: message };
  }
}

// --- Logout Server Action ---
// This function is called by the logout button.
export async function logout() {
    console.log("[Server Action] 'logout' action called.");
    try {
        const cookieStore = await cookies();
        // Check if cookies exist before attempting deletion
        const hasAccessToken = cookieStore.has('access_token');
        const hasRefreshToken = cookieStore.has('refresh_token');

        // Delete cookies using the 'delete' method
        if (hasAccessToken) {
            // For cookies set with path '/', just the name is usually enough
            cookieStore.delete('access_token');
        }
        if (hasRefreshToken) {
            // Important: The 'path' must match the path used when setting the cookie!
            cookieStore.delete({ name: 'refresh_token', path: '/api/auth/token/refresh/' }); // Specify path!
        }

        if (hasAccessToken || hasRefreshToken) {
             console.log("[Server Action] Cleared authentication cookies.");
        } else {
             console.log("[Server Action] No authentication cookies found to clear.");
        }

        // Optional: Call Django's logout endpoint if it performs necessary actions
        // (e.g., token blacklisting). This call might fail if cookies were already invalid/cleared.
        // try {
        //     await callDjangoBackend('/logout/', 'POST', null, 'auth');
        //     console.log("[Server Action] Successfully called Django logout endpoint.");
        // } catch (djangoLogoutError) {
        //     // Log a warning but proceed with local cookie clearing
        //     console.warn("[Server Action] Failed to call Django logout endpoint (maybe OK if tokens were already invalid):", djangoLogoutError);
        // }

        return { success: true, message: "Logged out successfully." };
    } catch(error: any) {
        console.error("[Server Action] Logout process failed:", error);
        return { success: false, message: error.message || "Logout failed due to an unknown error." };
    }
}