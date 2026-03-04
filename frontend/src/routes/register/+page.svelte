<script>
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import Navbar from '$lib/components/Navbar.svelte';

	let email = '';
	let password = '';
	let confirmPassword = '';
	let error = '';
	let loading = false;

	async function handleRegister() {
		error = '';

		if (password !== confirmPassword) {
			error = 'Passwords do not match';
			return;
		}

		if (password.length < 6) {
			error = 'Password must be at least 6 characters';
			return;
		}

		loading = true;

		try {
			const response = await api.register(email, password);
			authStore.login(response.user, response.access_token);
			goto('/dashboard');
		} catch (err) {
			error = err.message || 'Registration failed';
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
					Register
				</h2>

				{#if error}
					<div class="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
						{error}
					</div>
				{/if}

				<form on:submit|preventDefault={handleRegister} class="space-y-6">
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

					<div>
						<label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
							Confirm Password
						</label>
						<input
							id="confirmPassword"
							type="password"
							bind:value={confirmPassword}
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
						{loading ? 'Creating account...' : 'Register'}
					</button>
				</form>

				<div class="mt-6 text-center">
					<p class="text-sm text-gray-600">
						Already have an account?
						<a href="/login" class="text-indigo-600 hover:text-indigo-800 font-semibold">
							Login
						</a>
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
