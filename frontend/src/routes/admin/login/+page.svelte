<script>
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import Navbar from '$lib/components/Navbar.svelte';

	let email = '';
	let password = '';
	let error = '';
	let loading = false;

	async function handleLogin() {
		error = '';
		loading = true;

		try {
			const response = await api.login(email, password);
			
			// Check if user is admin
			if (response.user.role !== 'admin') {
				error = 'Access denied. Admin credentials required.';
				return;
			}

			authStore.login(response.user, response.access_token);
			goto('/admin/dashboard');
		} catch (err) {
			error = err.message || 'Login failed';
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800">
	<Navbar />
	<div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
		<div class="max-w-md w-full">
			<div class="bg-white rounded-lg shadow-2xl p-8">
				<div class="text-center mb-8">
					<div class="text-4xl mb-2">🔐</div>
					<h2 class="text-3xl font-bold text-gray-800">Admin Login</h2>
					<p class="text-gray-600 mt-2">Authorized access only</p>
				</div>

				{#if error}
					<div class="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
						{error}
					</div>
				{/if}

				<form on:submit|preventDefault={handleLogin} class="space-y-6">
					<div>
						<label for="email" class="block text-sm font-medium text-gray-700 mb-2">
							Admin Email
						</label>
						<input
							id="email"
							type="email"
							bind:value={email}
							required
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800"
							placeholder="admin@skillnest.com"
						/>
					</div>

					<div>
						<label for="password" class="block text-sm font-medium text-gray-700 mb-2">
							Password
						</label>
						<input
							id="password"
							type="password"
							bind:value={password}
							required
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800"
							placeholder="••••••••"
						/>
					</div>

					<button
						type="submit"
						disabled={loading}
						class="w-full bg-gray-900 text-white py-3 rounded-md font-semibold hover:bg-gray-800 transition disabled:opacity-50"
					>
						{loading ? 'Authenticating...' : 'Login as Admin'}
					</button>
				</form>

				<div class="mt-6 text-center">
					<a href="/login" class="text-sm text-gray-600 hover:text-gray-800">
						← Back to user login
					</a>
				</div>
			</div>
		</div>
	</div>
</div>
