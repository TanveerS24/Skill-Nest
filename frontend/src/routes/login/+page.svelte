<script lang="ts">
	import { authStore } from '$lib/stores/authStore';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let email = '';
	let password = '';
	let loading = false;

	// Redirect if already authenticated
	onMount(() => {
		if ($authStore.isAuthenticated) {
			goto('/dashboard');
		}
	});

	async function handleLogin() {
		if (loading) return;
		
		loading = true;
		authStore.clearError();
		
		const success = await authStore.login(email, password);
		loading = false;
		
		if (success) {
			goto('/dashboard');
		}
	}
</script>

<svelte:head>
	<title>Login - SkillNest</title>
</svelte:head>

<div class="flex flex-col items-center justify-center min-h-[calc(100vh-12rem)]">
	<div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
		<h1 class="text-3xl font-bold mb-6 text-center text-gray-900">Login to SkillNest</h1>

		{#if $authStore.error}
			<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-4">
				{$authStore.error}
			</div>
		{/if}

		<form on:submit|preventDefault={handleLogin}>
			<div class="mb-4">
				<label for="email" class="block text-sm font-medium text-gray-700 mb-2">Email</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
					placeholder="your@email.com"
					required
				/>
			</div>

			<div class="mb-6">
				<label for="password" class="block text-sm font-medium text-gray-700 mb-2">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
					placeholder="••••••••"
					required
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full bg-blue-600 text-white py-2 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition"
			>
				{loading ? 'Logging in...' : 'Login'}
			</button>
		</form>

		<p class="mt-6 text-center text-sm text-gray-600">
			Don't have an account?
			<a href="/register" class="text-blue-600 hover:text-blue-700 font-medium">
				Register here
			</a>
		</p>

		<div class="mt-6 pt-6 border-t border-gray-200">
			<p class="text-xs text-gray-500 text-center">
				Demo credentials:<br />
				Admin: admin@skillnest.com / admin123<br />
				User: user@test.com / user123
			</p>
		</div>
	</div>
</div>