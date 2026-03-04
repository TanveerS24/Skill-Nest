import { redirect } from '@sveltejs/kit';

export async function load({ parent }) {
    const { isAuthenticated, user } = await parent();
    
    // Check if admin
    if (!isAuthenticated || !user || user.role !== 'admin') {
        throw redirect(302, '/login');
    }
    
    return { user };
}
