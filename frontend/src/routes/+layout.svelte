<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/authStore';
	import { goto } from '$app/navigation';
	import '../app.css';

	onMount(() => {
		// Check auth status on mount
		authStore.checkAuth();
	});

	async function handleLogout() {
		await authStore.logout();
		goto('/');
	}
</script>

<div class="min-h-screen bg-gray-50">
	<!-- Navigation -->
	<nav class="bg-white shadow-sm border-b border-gray-200">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
			<div class="flex justify-between h-16">
				<div class="flex items-center space-x-8">
					<a href="/" class="flex items-center">
						<span class="text-2xl font-bold text-blue-600">SkillNest</span>
					</a>
					<div class="hidden md:flex space-x-4">
						<a
							href="/problems"
							class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition"
						>
							Problems
						</a>
						<a
							href="/leaderboard"
							class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition"
						>
							Leaderboard
						</a>
						{#if $authStore.isAuthenticated}
							<a
								href="/dashboard"
								class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition"
							>
								Dashboard
							</a>
							{#if $authStore.user?.role === 'admin'}
								<a
									href="/teacher/dashboard"
									class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition"
								>
									Admin
								</a>
							{/if}
						{/if}
					</div>
				</div>

				<div class="flex items-center space-x-4">
					{#if $authStore.isAuthenticated}
						<span class="text-sm text-gray-700">
							{$authStore.user?.email}
						</span>
						<button
							on:click={handleLogout}
							class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md text-sm font-medium transition"
						>
							Logout
						</button>
					{:else}
						<a
							href="/login"
							class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition"
						>
							Login
						</a>
						<a
							href="/register"
							class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium transition"
						>
							Register
						</a>
					{/if}
				</div>
			</div>
		</div>
	</nav>

	<!-- Main Content -->
	<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<slot />
	</main>

	<!-- Footer -->
	<footer class="bg-white border-t border-gray-200 mt-12">
		<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
			<p class="text-center text-gray-500 text-sm">
				© 2026 SkillNest. Multi-language Coding Platform with Docker Sandbox Execution.
			</p>
		</div>
	</footer>
</div>