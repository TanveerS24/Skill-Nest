<script lang="ts">
	import { onMount } from 'svelte';
	import { authStore } from '$lib/stores/authStore';
	import { goto } from '$app/navigation';
	import { submissionsApi } from '$lib/api/client';
	import type { Submission } from '$lib/types';

	let submissions: Submission[] = [];
	let loading = true;
	let stats = {
		totalSubmissions: 0,
		acceptedSubmissions: 0,
		problemsSolved: 0,
		acceptanceRate: 0
	};

	onMount(async () => {
		if (!$authStore.isAuthenticated) {
			goto('/login');
			return;
		}
		
		await loadDashboard();
	});

	async function loadDashboard() {
		try {
			loading = true;
			submissions = await submissionsApi.getSubmissions();
			
			// Calculate stats
			stats.totalSubmissions = submissions.length;
			stats.acceptedSubmissions = submissions.filter(s => s.verdict === 'Accepted').length;
			
			// Count unique problem IDs with accepted verdicts
			const solvedProblems = new Set(
				submissions
					.filter(s => s.verdict === 'Accepted')
					.map(s => s.problem_id)
			);
			stats.problemsSolved = solvedProblems.size;
			
			stats.acceptanceRate = stats.totalSubmissions > 0
				? Math.round((stats.acceptedSubmissions / stats.totalSubmissions) * 100)
				: 0;
		} catch (error) {
			console.error('Error loading dashboard:', error);
		} finally {
			loading = false;
		}
	}

	function getVerdictColor(verdict: string): string {
		switch (verdict) {
			case 'Accepted':
				return 'text-green-600 bg-green-50';
			case 'Wrong Answer':
				return 'text-yellow-600 bg-yellow-50';
			default:
				return 'text-red-600 bg-red-50';
		}
	}

	function formatDate(dateStr: string): string {
		const date = new Date(dateStr);
		return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
	}
</script>

<svelte:head>
	<title>Dashboard - SkillNest</title>
</svelte:head>

{#if loading}
	<div class="flex justify-center items-center py-12">
		<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
	</div>
{:else}
	<div>
		<div class="mb-8">
			<h1 class="text-4xl font-bold text-gray-900 mb-2">My Dashboard</h1>
			<p class="text-gray-600">
				Welcome back, {$authStore.user?.email}
			</p>
		</div>

		<!-- Stats Grid -->
		<div class="grid md:grid-cols-4 gap-6 mb-8">
			<div class="bg-white p-6 rounded-lg shadow-sm">
				<div class="text-sm font-medium text-gray-600 mb-1">Total Submissions</div>
				<div class="text-3xl font-bold text-blue-600">{stats.totalSubmissions}</div>
			</div>

			<div class="bg-white p-6 rounded-lg shadow-sm">
				<div class="text-sm font-medium text-gray-600 mb-1">Accepted</div>
				<div class="text-3xl font-bold text-green-600">{stats.acceptedSubmissions}</div>
			</div>

			<div class="bg-white p-6 rounded-lg shadow-sm">
				<div class="text-sm font-medium text-gray-600 mb-1">Problems Solved</div>
				<div class="text-3xl font-bold text-purple-600">{stats.problemsSolved}</div>
			</div>

			<div class="bg-white p-6 rounded-lg shadow-sm">
				<div class="text-sm font-medium text-gray-600 mb-1">Acceptance Rate</div>
				<div class="text-3xl font-bold text-indigo-600">{stats.acceptanceRate}%</div>
			</div>
		</div>

		<!-- Recent Submissions -->
		<div class="bg-white rounded-lg shadow-sm">
			<div class="p-6 border-b border-gray-200">
				<h2 class="text-2xl font-bold text-gray-900">Recent Submissions</h2>
			</div>

			{#if submissions.length === 0}
				<div class="p-8 text-center text-gray-500">
					<p class="mb-4">No submissions yet</p>
					<a
						href="/problems"
						class="inline-block bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 transition"
					>
						Start Solving Problems
					</a>
				</div>
			{:else}
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Problem</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Language</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Verdict</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Runtime</th>
								<th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
							</tr>
						</thead>
						<tbody class="bg-white divide-y divide-gray-200">
							{#each submissions.slice(0, 20) as submission}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										#{submission.id}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm">
										<a
											href="/problems/{submission.problem_id}"
											class="text-blue-600 hover:underline"
										>
											Problem #{submission.problem_id}
										</a>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{submission.language.toUpperCase()}
									</td>
									<td class="px-6 py-4 whitespace-nowrap">
										<span class="px-2 py-1 text-xs font-semibold rounded {getVerdictColor(submission.verdict)}">
											{submission.verdict}
										</span>
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
										{submission.runtime ? `${submission.runtime.toFixed(2)} ms` : '-'}
									</td>
									<td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
										{formatDate(submission.created_at)}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		</div>
	</div>
{/if}