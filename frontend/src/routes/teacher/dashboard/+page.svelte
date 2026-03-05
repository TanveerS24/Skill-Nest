<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/authStore';
	import { goto } from '$app/navigation';
	import { adminApi } from '$lib/api/client';
	import LeaderboardTable from '$lib/components/LeaderboardTable.svelte';

	interface Problem {
		problem_id: number;
		title: string;
		attempts: number;
	}

	interface LanguageUsage {
		[key: string]: number;
	}

	interface Stats {
		total_users: number;
		total_submissions: number;
		accepted_submissions: number;
		most_attempted_problems: Problem[];
		top_users: any[];
		top_performers: any[];
		language_usage: LanguageUsage;
		language_stats: any;
	}

	let stats: Stats | null = null;
	let loading = true;
	let error: string | null = null;

	onMount(async () => {
		if (!$authStore.isAuthenticated) {
			goto('/login');
			return;
		}

		if ($authStore.user?.role !== 'admin') {
			goto('/dashboard');
			return;
		}

		await loadDashboard();
	});

	async function loadDashboard() {
		try {
			loading = true;
			error = null;
			stats = await adminApi.getDashboard();
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Admin Dashboard - SkillNest</title>
</svelte:head>

{#if loading}
	<div class="flex justify-center items-center py-12">
		<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
	</div>
{:else if error}
	<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
		<p class="font-medium">Error loading dashboard</p>
		<p class="text-sm">{error}</p>
		<button
			on:click={loadDashboard}
			class="mt-2 text-sm underline hover:no-underline"
		>
			Try again
		</button>
	</div>
{:else if stats}
	<div>
		<div class="mb-8">
			<h1 class="text-4xl font-bold text-gray-900 mb-2">Admin Dashboard</h1>
			<p class="text-gray-600">
				Platform analytics and statistics
			</p>
		</div>

		<!-- Stats Grid -->
		<div class="grid md:grid-cols-4 gap-6 mb-8">
			<div class="bg-white p-6 rounded-lg shadow-md">
				<div class="text-sm font-medium text-gray-600 mb-1">Total Users</div>
				<div class="text-4xl font-bold text-blue-600">{stats.total_users}</div>
			</div>

			<div class="bg-white p-6 rounded-lg shadow-md">
				<div class="text-sm font-medium text-gray-600 mb-1">Total Submissions</div>
				<div class="text-4xl font-bold text-purple-600">{stats.total_submissions}</div>
			</div>

			<div class="bg-white p-6 rounded-lg shadow-md">
				<div class="text-sm font-medium text-gray-600 mb-1">Accepted Submissions</div>
				<div class="text-4xl font-bold text-green-600">{stats.accepted_submissions}</div>
			</div>

			<div class="bg-white p-6 rounded-lg shadow-md">
				<div class="text-sm font-medium text-gray-600 mb-1">Acceptance Rate</div>
				<div class="text-4xl font-bold text-indigo-600">
					{stats.total_submissions > 0 ? Math.round((stats.accepted_submissions / stats.total_submissions) * 100) : 0}%
				</div>
			</div>
		</div>

		<!-- Two Column Layout -->
		<div class="grid md:grid-cols-2 gap-8 mb-8">
			<!-- Most Attempted Problems -->
			<div class="bg-white p-6 rounded-lg shadow-md">
				<h2 class="text-2xl font-bold text-gray-900 mb-4">Most Attempted Problems</h2>
				{#if stats.most_attempted_problems && stats.most_attempted_problems.length > 0}
					<div class="space-y-3">
						{#each stats.most_attempted_problems as problem}
							<div class="flex items-center justify-between p-3 bg-gray-50 rounded">
								<div>
									<a
										href="/problems/{problem.problem_id}"
										class="text-sm font-medium text-blue-600 hover:underline"
									>
										{problem.title}
									</a>
									<p class="text-xs text-gray-500">Problem #{problem.problem_id}</p>
								</div>
								<span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm font-semibold rounded-full">
									{problem.attempts} attempts
								</span>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-gray-500 text-center py-4">No data available</p>
				{/if}
			</div>

			<!-- Language Usage Statistics -->
			<div class="bg-white p-6 rounded-lg shadow-md">
				<h2 class="text-2xl font-bold text-gray-900 mb-4">Language Usage</h2>
				{#if stats.language_usage && Object.keys(stats.language_usage).length > 0}
					<div class="space-y-3">
						{#each Object.entries(stats.language_usage) as [lang, count]}
							<div class="flex items-center justify-between">
								<span class="text-sm font-medium text-gray-700 uppercase">{lang}</span>
								<div class="flex items-center gap-2">
									<div class="w-32 bg-gray-200 rounded-full h-2">
										<div
											class="bg-blue-600 h-2 rounded-full"
											style="width: {(Number(count) / stats.total_submissions) * 100}%"
										></div>
									</div>
									<span class="text-sm font-semibold text-gray-900 w-12 text-right">
										{count}
									</span>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-gray-500 text-center py-4">No data available</p>
				{/if}
			</div>
		</div>

		<!-- Top Users Leaderboard -->
		<div class="bg-white p-6 rounded-lg shadow-md">
			<h2 class="text-2xl font-bold text-gray-900 mb-4">Top 10 Users</h2>
			{#if stats.top_users && stats.top_users.length > 0}
				<LeaderboardTable entries={stats.top_users} loading={false} />
			{:else}
				<p class="text-gray-500 text-center py-4">No leaderboard data available</p>
			{/if}
		</div>
	</div>
{/if}