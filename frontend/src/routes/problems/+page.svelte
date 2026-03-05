<script lang="ts">
	import { onMount } from 'svelte';
	import ProblemCard from '$lib/components/ProblemCard.svelte';
	import { problemsApi } from '$lib/api/client';
	import type { Problem } from '$lib/types';

	let problems: Problem[] = [];
	let loading = true;
	let error: string | null = null;
	let filter = 'all';
	let searchQuery = '';

	onMount(async () => {
		await loadProblems();
	});

	async function loadProblems() {
		try {
			loading = true;
			error = null;
			problems = await problemsApi.getProblems();
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}

	$: filteredProblems = problems.filter(problem => {
		const matchesFilter = filter === 'all' || problem.difficulty.toLowerCase() === filter;
		const matchesSearch = problem.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
							  problem.description.toLowerCase().includes(searchQuery.toLowerCase());
		return matchesFilter && matchesSearch;
	});
</script>

<svelte:head>
	<title>Problems - SkillNest</title>
</svelte:head>

<div>
	<div class="mb-8">
		<h1 class="text-4xl font-bold text-gray-900 mb-2">Coding Problems</h1>
		<p class="text-gray-600">
			Solve Data Structure & Algorithm problems in Python, Java, C, or C++
		</p>
	</div>

	<!-- Filters and Search -->
	<div class="bg-white p-4 rounded-lg shadow-sm mb-6">
		<div class="flex flex-col md:flex-row gap-4 items-center justify-between">
			<div class="flex gap-2">
				<button
					on:click={() => filter = 'all'}
					class="px-4 py-2 rounded-md font-medium transition {filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
				>
					All
				</button>
				<button
					on:click={() => filter = 'easy'}
					class="px-4 py-2 rounded-md font-medium transition {filter === 'easy' ? 'bg-green-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
				>
					Easy
				</button>
				<button
					on:click={() => filter = 'medium'}
					class="px-4 py-2 rounded-md font-medium transition {filter === 'medium' ? 'bg-yellow-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
				>
					Medium
				</button>
				<button
					on:click={() => filter = 'hard'}
					class="px-4 py-2 rounded-md font-medium transition {filter === 'hard' ? 'bg-red-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
				>
					Hard
				</button>
			</div>

			<div class="w-full md:w-auto">
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search problems..."
					class="w-full md:w-64 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
				/>
			</div>
		</div>
	</div>

	<!-- Problems Grid -->
	{#if loading}
		<div class="flex justify-center items-center py-12">
			<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
		</div>
	{:else if error}
		<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
			<p class="font-medium">Error loading problems</p>
			<p class="text-sm">{error}</p>
			<button
				on:click={loadProblems}
				class="mt-2 text-sm underline hover:no-underline"
			>
				Try again
			</button>
		</div>
	{:else if filteredProblems.length === 0}
		<div class="text-center py-12 text-gray-500">
			<p class="text-lg">No problems found</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each filteredProblems as problem (problem.id)}
				<ProblemCard {problem} />
			{/each}
		</div>
	{/if}

	<div class="mt-8 text-center text-sm text-gray-500">
		Showing {filteredProblems.length} of {problems.length} problems
	</div>
</div>