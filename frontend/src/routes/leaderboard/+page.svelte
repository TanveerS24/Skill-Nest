<script lang="ts">
	import { onMount } from 'svelte';
	import LeaderboardTable from '$lib/components/LeaderboardTable.svelte';
	import { leaderboardStore } from '$lib/stores/leaderboardStore';

	let sortBy = 'solved';

	onMount(() => {
		loadLeaderboard();
	});

	async function loadLeaderboard() {
		await leaderboardStore.fetchLeaderboard(sortBy);
	}

	$: if (sortBy) {
		loadLeaderboard();
	}
</script>

<svelte:head>
	<title>Leaderboard - SkillNest</title>
</svelte:head>

<div>
	<div class="mb-8">
		<h1 class="text-4xl font-bold text-gray-900 mb-2">Leaderboard</h1>
		<p class="text-gray-600">
			Top performers on SkillNest coding platform
		</p>
	</div>

	<!-- Sort Options -->
	<div class="bg-white p-4 rounded-lg shadow-sm mb-6">
		<div class="flex items-center gap-4">
			<label class="text-sm font-medium text-gray-700">Sort By:</label>
			<div class="flex gap-2">
				<button
					on:click={() => sortBy = 'solved'}
					class="px-4 py-2 rounded-md font-medium transition {sortBy === 'solved' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
				>
					Problems Solved
				</button>
				<button
					on:click={() => sortBy = 'time'}
					class="px-4 py-2 rounded-md font-medium transition {sortBy === 'time' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
				>
					Time Complexity
				</button>
				<button
					on:click={() => sortBy = 'space'}
					class="px-4 py-2 rounded-md font-medium transition {sortBy === 'space' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
				>
					Space Complexity
				</button>
			</div>
		</div>
	</div>

	<!-- Leaderboard Table -->
	{#if $leaderboardStore.error}
		<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
			<p class="font-medium">Error loading leaderboard</p>
			<p class="text-sm">{$leaderboardStore.error}</p>
			<button
				on:click={loadLeaderboard}
				class="mt-2 text-sm underline hover:no-underline"
			>
				Try again
			</button>
		</div>
	{:else}
		<LeaderboardTable 
			entries={$leaderboardStore.entries} 
			loading={$leaderboardStore.loading} 
		/>
	{/if}

	<!-- Info Box -->
	<div class="mt-6 bg-blue-50 border border-blue-200 p-4 rounded-lg">
		<h3 class="font-semibold text-blue-900 mb-2">How Ranking Works</h3>
		<ul class="text-sm text-blue-800 space-y-1">
			<li>• Problems Solved: Ranked by unique problems successfully completed</li>
			<li>• Time Complexity: Lower average complexity score ranks higher (O(1) = 1, O(log n) = 2, O(n) = 3, O(n log n) = 4, O(n²) = 5)</li>
			<li>• Space Complexity: Same scoring as time complexity</li>
		</ul>
	</div>
</div>