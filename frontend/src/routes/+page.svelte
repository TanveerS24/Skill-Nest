<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/authStore';
	import { goto } from '$app/navigation';

	let stats = {
		totalProblems: 0,
		totalUsers: 0,
		totalSubmissions: 10
	};

	onMount(async () => {
		// Fetch stats
	});
</script>

<svelte:head>
	<title>SkillNest - Multi-Language Coding Platform</title>
</svelte:head>

<div class="min-h-[calc(100vh-12rem)]">
	<!-- Hero Section -->
	<section class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-20 rounded-lg mb-12">
		<div class="text-center">
			<h1 class="text-5xl font-bold mb-4">Welcome to SkillNest</h1>
			<p class="text-xl mb-8 text-blue-100">
				Master Data Structures & Algorithms with Real-time Code Execution
			</p>
			<div class="flex justify-center gap-4">
				{#if $authStore.isAuthenticated}
					<a
						href="/problems"
						class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
					>
						Browse Problems
					</a>
					<a
						href="/dashboard"
						class="bg-blue-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-400 transition"
					>
						My Dashboard
					</a>
				{:else}
					<a
						href="/register"
						class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
					>
						Get Started
					</a>
					<a
						href="/problems"
						class="bg-blue-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-400 transition"
					>
						Browse Problems
					</a>
				{/if}
			</div>
		</div>
	</section>

	<!-- Features Section -->
	<section class="grid md:grid-cols-3 gap-8 mb-12">
		<div class="bg-white p-6 rounded-lg shadow-md">
			<div class="text-3xl mb-4">🐍</div>
			<h3 class="text-xl font-bold mb-2">Multi-Language Support</h3>
			<p class="text-gray-600">
				Code in Python, Java, C, or C++. All solutions run in isolated Docker containers.
			</p>
		</div>

		<div class="bg-white p-6 rounded-lg shadow-md">
			<div class="text-3xl mb-4">🤖</div>
			<h3 class="text-xl font-bold mb-2">AI Code Analysis</h3>
			<p class="text-gray-600">
				Get instant feedback on time/space complexity and security issues before execution.
			</p>
		</div>

		<div class="bg-white p-6 rounded-lg shadow-md">
			<div class="text-3xl mb-4">🏆</div>
			<h3 class="text-xl font-bold mb-2">Dynamic Leaderboard</h3>
			<p class="text-gray-600">
				Compete with others! Sort by problems solved, complexity score, or submission count.
			</p>
		</div>
	</section>

	<!-- Stats Section -->
	<section class="bg-white p-8 rounded-lg shadow-md">
		<h2 class="text-2xl font-bold text-center mb-6">Platform Statistics</h2>
		<div class="grid md:grid-cols-3 gap-6 text-center">
			<div>
				<div class="text-4xl font-bold text-blue-600">{stats.totalProblems}</div>
				<div class="text-gray-600 mt-2">DSA Problems</div>
			</div>
			<div>
				<div class="text-4xl font-bold text-green-600">{stats.totalUsers}+</div>
				<div class="text-gray-600 mt-2">Active Users</div>
			</div>
			<div>
				<div class="text-4xl font-bold text-purple-600">{stats.totalSubmissions}+</div>
				<div class="text-gray-600 mt-2">Code Submissions</div>
			</div>
		</div>
	</section>

	<!-- CTA Section -->
	<section class="mt-12 text-center">
		<h2 class="text-3xl font-bold mb-4">Ready to Start Coding?</h2>
		<p class="text-gray-600 mb-6">
			Join thousands of developers improving their problem-solving skills
		</p>
		<a
			href="/problems"
			class="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
		>
			View All Problems
		</a>
	</section>
</div>