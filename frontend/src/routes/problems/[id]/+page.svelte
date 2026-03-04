<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import { authStore } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import Navbar from '$lib/components/Navbar.svelte';
	import CodeEditor from '$lib/components/CodeEditor.svelte';
	import SubmissionResult from '$lib/components/SubmissionResult.svelte';

	let problem = null;
	let code = '';
	let language = 'python';
	let loading = true;
	let submitting = false;
	let submission = null;
	let error = '';
	let user = null;

	authStore.subscribe(state => {
		user = state.user;
	});

	$: problemId = $page.params.id;

	onMount(async () => {
		if (!user) {
			goto('/login');
			return;
		}

		try {
			problem = await api.getProblem(problemId);
			
			// Set default code template
			code = getDefaultCode(language);
		} catch (err) {
			error = 'Failed to load problem';
		} finally {
			loading = false;
		}
	});

	function getDefaultCode(lang) {
		const templates = {
			python: '# Write your solution here\n\ndef solve():\n    pass\n\nif __name__ == "__main__":\n    solve()',
			javascript: '// Write your solution here\n\nfunction solve() {\n    // Your code\n}\n\nsolve();',
			cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your solution here\n    return 0;\n}',
			java: 'public class Solution {\n    public static void main(String[] args) {\n        // Write your solution here\n    }\n}'
		};
		return templates[lang] || '';
	}

	function handleLanguageChange(event) {
		language = event.target.value;
		if (!code || code === getDefaultCode(language)) {
			code = getDefaultCode(language);
		}
	}

	async function handleSubmit() {
		if (!code.trim()) {
			error = 'Please write some code';
			return;
		}

		submitting = true;
		error = '';
		submission = null;

		try {
			const result = await api.submitCode(problemId, code);
			submission = result;
			
			// Update user score if accepted
			if (result.verdict === 'Accepted' && user) {
				const updatedUser = await api.getCurrentUser();
				authStore.login(updatedUser, localStorage.getItem('token'));
			}
		} catch (err) {
			error = err.message || 'Submission failed';
		} finally {
			submitting = false;
		}
	}

	const difficultyColors = {
		'Easy': 'bg-green-100 text-green-800',
		'Medium': 'bg-yellow-100 text-yellow-800',
		'Hard': 'bg-red-100 text-red-800'
	};
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
	<Navbar />
	<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
		{#if loading}
			<div class="text-center py-12">
				<div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
			</div>
		{:else if problem}
			<div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
				<!-- Problem Description -->
				<div class="space-y-6">
					<div class="bg-white rounded-lg shadow-md p-6">
						<div class="flex justify-between items-start mb-4">
							<h1 class="text-3xl font-bold text-gray-800">{problem.title}</h1>
							<span class={`px-3 py-1 rounded-full text-sm font-semibold ${difficultyColors[problem.difficulty]}`}>
								{problem.difficulty}
							</span>
						</div>
						
						<div class="prose max-w-none">
							<p class="text-gray-700 whitespace-pre-wrap">{problem.description}</p>
						</div>

						<div class="mt-6 grid grid-cols-2 gap-4">
							<div class="bg-gray-50 p-4 rounded-lg">
								<p class="text-sm text-gray-600">Time Limit</p>
								<p class="text-lg font-semibold text-gray-800">{problem.time_limit}s</p>
							</div>
							<div class="bg-gray-50 p-4 rounded-lg">
								<p class="text-sm text-gray-600">Memory Limit</p>
								<p class="text-lg font-semibold text-gray-800">{problem.memory_limit}MB</p>
							</div>
						</div>
					</div>

					{#if submission}
						<SubmissionResult {submission} />
					{/if}
				</div>

				<!-- Code Editor -->
				<div class="space-y-4">
					<div class="bg-white rounded-lg shadow-md p-6">
						<div class="flex justify-between items-center mb-4">
							<h2 class="text-xl font-semibold text-gray-800">Code Editor</h2>
							<select
								bind:value={language}
								on:change={handleLanguageChange}
								class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
							>
								<option value="python">Python</option>
								<option value="javascript">JavaScript</option>
								<option value="cpp">C++</option>
								<option value="java">Java</option>
							</select>
						</div>

						<CodeEditor bind:value={code} {language} />

						{#if error}
							<div class="mt-4 bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded">
								{error}
							</div>
						{/if}

						<button
							on:click={handleSubmit}
							disabled={submitting}
							class="mt-4 w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white py-3 rounded-md font-semibold hover:from-indigo-700 hover:to-blue-700 transition disabled:opacity-50"
						>
							{submitting ? 'Submitting...' : 'Submit Solution'}
						</button>
					</div>
				</div>
			</div>
		{:else}
			<div class="bg-white rounded-lg shadow-md p-12 text-center">
				<p class="text-red-600 text-lg">{error || 'Problem not found'}</p>
			</div>
		{/if}
	</div>
</div>
