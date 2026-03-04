import { authStore } from '$lib/stores/auth';
import { redirect } from '@sveltejs/kit';

export async function load({ url }) {
    let isAuthenticated = false;
    let user = null;
    
    if (typeof window !== 'undefined') {
        const token = localStorage.getItem('token');
        const storedUser = localStorage.getItem('user');
        
        if (token && storedUser) {
            isAuthenticated = true;
            user = JSON.parse(storedUser);
        }
    }
    
    return {
        isAuthenticated,
        user,
        pathname: url.pathname
    };
}
