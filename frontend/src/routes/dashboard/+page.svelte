<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import Navbar from '$lib/components/Navbar.svelte';
	import LeaderboardTable from '$lib/components/LeaderboardTable.svelte';

	let user = null;
	let submissions = [];
	let leaderboard = [];
	let loading = true;

	authStore.subscribe(state => {
		user = state.user;
	});

	onMount(async () => {
		if (!user) {
			goto('/login');
			return;
		}

		try {
			const [submissionsData, leaderboardData] = await Promise.all([
				api.getMySubmissions(),
				api.getLeaderboard()
			]);

			submissions = submissionsData.slice(0, 5);
			leaderboard = leaderboardData.slice(0, 10);
		} catch (error) {
			console.error('Error loading dashboard:', error);
		} finally {
			loading = false;
		}
	});

	const verdictColors = {
		'Accepted': 'text-green-600',
		'Wrong Answer': 'text-red-600',
		'Runtime Error': 'text-orange-600',
		'Time Limit Exceeded': 'text-yellow-600',
		'Memory Limit Exceeded': 'text-purple-600'
	};
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
	<Navbar />
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<div class="mb-8">
			<h1 class="text-4xl font-bold text-gray-800">Dashboard</h1>
			{#if user}
				<p class="text-gray-600 mt-2">Welcome back, {user.email}!</p>
				<p class="text-lg font-semibold text-indigo-600 mt-1">Score: {user.score} points</p>
			{/if}
		</div>

		{#if loading}
			<div class="text-center py-12">
				<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
			</div>
		{:else}
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
				<!-- Recent Submissions -->
				<div class="bg-white rounded-lg shadow-md p-6">
					<div class="flex justify-between items-center mb-4">
						<h2 class="text-2xl font-bold text-gray-800">Recent Submissions</h2>
						<a href="/problems" class="text-indigo-600 hover:text-indigo-800 font-semibold">
							View All →
						</a>
					</div>

					{#if submissions.length > 0}
						<div class="space-y-3">
							{#each submissions as submission}
								<div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
									<div class="flex justify-between items-start">
										<div>
											<p class="font-semibold text-gray-800">Problem #{submission.problem_id}</p>
											<p class="text-sm text-gray-600 capitalize">{submission.detected_language || 'Unknown'}</p>
										</div>
										<span class={`font-semibold ${verdictColors[submission.verdict] || 'text-gray-600'}`}>
											{submission.verdict}
										</span>
									</div>
									<p class="text-xs text-gray-500 mt-2">
										{new Date(submission.created_at).toLocaleDateString()}
									</p>
								</div>
							{/each}
						</div>
					{:else}
						<p class="text-gray-500 text-center py-8">No submissions yet. Start solving problems!</p>
					{/if}
				</div>

				<!-- Leaderboard Preview -->
				<div>
					<LeaderboardTable users={leaderboard} />
				</div>
			</div>

			<!-- Quick Actions -->
			<div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
				<a
					href="/problems"
					class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition text-center border-2 border-transparent hover:border-indigo-600"
				>
					<div class="text-4xl mb-2">💻</div>
					<h3 class="text-lg font-semibold text-gray-800">Solve Problems</h3>
					<p class="text-sm text-gray-600 mt-2">Practice and improve your skills</p>
				</a>

				<a
					href="/problems"
					class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition text-center border-2 border-transparent hover:border-indigo-600"
				>
					<div class="text-4xl mb-2">📊</div>
					<h3 class="text-lg font-semibold text-gray-800">View Progress</h3>
					<p class="text-sm text-gray-600 mt-2">Track your submission history</p>
				</a>

				<a
					href="/problems"
					class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition text-center border-2 border-transparent hover:border-indigo-600"
				>
					<div class="text-4xl mb-2">🏆</div>
					<h3 class="text-lg font-semibold text-gray-800">Compete</h3>
					<p class="text-sm text-gray-600 mt-2">Climb the leaderboard</p>
				</a>
			</div>
		{/if}
	</div>
</div>
