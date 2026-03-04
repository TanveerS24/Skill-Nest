<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import Navbar from '$lib/components/Navbar.svelte';

	let problems = [];
	let loading = true;
	let user = null;

	authStore.subscribe(state => {
		user = state.user;
	});

	onMount(async () => {
		if (!user) {
			goto('/login');
			return;
		}

		try {
			problems = await api.getProblems();
		} catch (error) {
			console.error('Error loading problems:', error);
		} finally {
			loading = false;
		}
	});

	const difficultyColors = {
		'Easy': 'bg-green-100 text-green-800',
		'Medium': 'bg-yellow-100 text-yellow-800',
		'Hard': 'bg-red-100 text-red-800'
	};

	function navigateToProblem(problemId) {
		goto(`/problems/${problemId}`);
	}
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
	<Navbar />
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		<h1 class="text-4xl font-bold text-gray-800 mb-8">Problems</h1>

		{#if loading}
			<div class="text-center py-12">
				<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
			</div>
		{:else if problems.length > 0}
			<div class="bg-white rounded-lg shadow-md overflow-hidden">
				<table class="min-w-full divide-y divide-gray-200">
					<thead class="bg-gray-50">
						<tr>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								ID
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Title
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Difficulty
							</th>
							<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
								Action
							</th>
						</tr>
					</thead>
					<tbody class="bg-white divide-y divide-gray-200">
						{#each problems as problem}
							<tr class="hover:bg-gray-50 transition cursor-pointer" on:click={() => navigateToProblem(problem.id)}>
								<td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
									{problem.id}
								</td>
								<td class="px-6 py-4 text-sm text-gray-900">
									{problem.title}
								</td>
								<td class="px-6 py-4 whitespace-nowrap">
									<span class={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${difficultyColors[problem.difficulty]}`}>
										{problem.difficulty}
									</span>
								</td>
								<td class="px-6 py-4 whitespace-nowrap text-sm">
									<button
										on:click|stopPropagation={() => navigateToProblem(problem.id)}
										class="text-indigo-600 hover:text-indigo-900 font-semibold"
									>
										Solve →
									</button>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{:else}
			<div class="bg-white rounded-lg shadow-md p-12 text-center">
				<p class="text-gray-500 text-lg">No problems available yet.</p>
			</div>
		{/if}
	</div>
</div>
