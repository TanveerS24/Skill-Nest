<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import Navbar from '$lib/components/Navbar.svelte';
	import AdminStatsCard from '$lib/components/AdminStatsCard.svelte';

	let user = null;
	let stats = null;
	let topUsers = [];
	let languageUsage = [];
	let problemAnalytics = [];
	let loading = true;
	let error = '';

	authStore.subscribe(state => {
		user = state.user;
	});

	onMount(async () => {
		if (!user || user.role !== 'admin') {
			goto('/admin/login');
			return;
		}

		try {
			const [statsData, topUsersData, languageData, problemsData] = await Promise.all([
				api.getAdminStats(),
				api.getTopUsers(20),
				api.getLanguageUsage(),
				api.getProblemAnalytics(20)
			]);

			stats = statsData;
			topUsers = topUsersData;
			languageUsage = languageData;
			problemAnalytics = problemsData;
		} catch (err) {
			error = 'Failed to load admin data';
			console.error(err);
		} finally {
			loading = false;
		}
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-gray-100 to-gray-200">
	<Navbar />
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<div class="mb-8">
			<h1 class="text-4xl font-bold text-gray-800">Admin Dashboard</h1>
			<p class="text-gray-600 mt-2">Platform analytics and insights</p>
		</div>

		{#if loading}
			<div class="text-center py-12">
				<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-800"></div>
			</div>
		{:else if error}
			<div class="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
				{error}
			</div>
		{:else}
			<!-- Stats Cards -->
			{#if stats}
				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
					<AdminStatsCard
						title="Total Users"
						value={stats.total_users}
						icon="👥"
						color="blue"
					/>
					<AdminStatsCard
						title="Total Submissions"
						value={stats.total_submissions}
						icon="📝"
						color="purple"
					/>
					<AdminStatsCard
						title="Acceptance Rate"
						value={`${stats.acceptance_rate}%`}
						icon="✅"
						color="green"
					/>
					<AdminStatsCard
						title="Today's Submissions"
						value={stats.submissions_today}
						icon="🔥"
						color="orange"
					/>
				</div>
			{/if}

			<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
				<!-- Top Users -->
				<div class="bg-white rounded-lg shadow-md overflow-hidden">
					<div class="px-6 py-4 bg-gradient-to-r from-blue-600 to-indigo-600">
						<h2 class="text-xl font-bold text-white">Top 20 Users</h2>
					</div>
					<div class="overflow-x-auto max-h-96">
						<table class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50 sticky top-0">
								<tr>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rank</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Score</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								{#each topUsers as user, index}
									<tr class="hover:bg-gray-50">
										<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
											{index + 1}
										</td>
										<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
											{user.email}
										</td>
										<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
											{user.score}
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>

				<!-- Most Attempted Problems -->
				<div class="bg-white rounded-lg shadow-md overflow-hidden">
					<div class="px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600">
						<h2 class="text-xl font-bold text-white">Most Attempted Problems</h2>
					</div>
					<div class="overflow-x-auto max-h-96">
						<table class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50 sticky top-0">
								<tr>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Title</th>
									<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Attempts</th>
								</tr>
							</thead>
							<tbody class="bg-white divide-y divide-gray-200">
								{#each problemAnalytics as problem}
									<tr class="hover:bg-gray-50">
										<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
											{problem.problem_id}
										</td>
										<td class="px-6 py-4 text-sm text-gray-900">
											{problem.problem_title}
										</td>
										<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
											{problem.submission_count}
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				</div>
			</div>

			<!-- Language Usage -->
			{#if languageUsage.length > 0}
				<div class="mt-8 bg-white rounded-lg shadow-md p-6">
					<h2 class="text-2xl font-bold text-gray-800 mb-6">Language Usage</h2>
					<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
						{#each languageUsage as lang}
							<div class="bg-gradient-to-br from-indigo-500 to-purple-500 rounded-lg p-4 text-white">
								<p class="text-sm font-medium uppercase">{lang.language}</p>
								<p class="text-3xl font-bold mt-2">{lang.count}</p>
								<p class="text-xs mt-1">submissions</p>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		{/if}
	</div>
</div>
