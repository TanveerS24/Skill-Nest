import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('refresh_token');

  if (token) {
    event.locals.user = await fetchUserFromToken(token);
  }

  return resolve(event);
};

async function fetchUserFromToken(token: string) {
  const response = await fetch('/auth/validate', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` }
  });

  if (response.ok) {
    return await response.json();
  }

  return null;
}