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
			authStore.login(response.user, response.access_token);
			
			// Redirect based on role
			if (response.user.role === 'admin') {
				goto('/admin/dashboard');
			} else {
				goto('/dashboard');
			}
		} catch (err) {
			error = err.message || 'Login failed';
		} finally {
			loading = false;
		}
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
	<Navbar />
	<div class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
		<div class="max-w-md w-full">
			<div class="bg-white rounded-lg shadow-xl p-8">
				<h2 class="text-3xl font-bold text-center text-gray-800 mb-8">
					Login
				</h2>

				{#if error}
					<div class="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
						{error}
					</div>
				{/if}

				<form on:submit|preventDefault={handleLogin} class="space-y-6">
					<div>
						<label for="email" class="block text-sm font-medium text-gray-700 mb-2">
							Email
						</label>
						<input
							id="email"
							type="email"
							bind:value={email}
							required
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
							placeholder="your@email.com"
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
							class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
							placeholder="••••••••"
						/>
					</div>

					<button
						type="submit"
						disabled={loading}
						class="w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white py-3 rounded-md font-semibold hover:from-indigo-700 hover:to-blue-700 transition disabled:opacity-50"
					>
						{loading ? 'Logging in...' : 'Login'}
					</button>
				</form>

				<div class="mt-6 text-center">
					<p class="text-sm text-gray-600">
						Don't have an account?
						<a href="/register" class="text-indigo-600 hover:text-indigo-800 font-semibold">
							Register
						</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
