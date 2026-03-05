<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/authStore';
	import CodeEditor from '$lib/components/CodeEditor.svelte';
	import { problemsApi, submissionsApi } from '$lib/api/client';
	import { goto } from '$app/navigation';

	let problem: any = null;
	let language = 'python';
	let code = '';
	let result: any = null;
	let loading = false;
	let submitting = false;
	let error: string | null = null;

	const languageTemplates: Record<string, string> = {
		python: '# Write your solution here\n\ndef solution():\n    pass\n\nif __name__ == "__main__":\n    solution()',
		java: 'public class Solution {\n    public static void main(String[] args) {\n        // Write your solution here\n    }\n}',
		c: '#include <stdio.h>\n\nint main() {\n    // Write your solution here\n    return 0;\n}',
		cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    // Write your solution here\n    return 0;\n}'
	};

	onMount(async () => {
		await loadProblem();
	});

	async function loadProblem() {
		try {
			loading = true;
			error = null;
			const id = parseInt($page.params.id);
			problem = await problemsApi.getProblem(id);
			code = languageTemplates[language];
		} catch (err: any) {
			error = err.message;
		} finally {
			loading = false;
		}
	}

	async function submitCode() {
		if (!$authStore.isAuthenticated) {
			alert('Please login to submit code');
			goto('/login');
			return;
		}

		if (!code.trim()) {
			alert('Please write some code before submitting');
			return;
		}

		try {
			submitting = true;
			result = null;
			error = null;
			
			result = await submissionsApi.submitCode(problem.id, language, code);
		} catch (err: any) {
			error = err.message;
		} finally {
			submitting = false;
		}
	}

	function changeLanguage(newLang: string) {
		language = newLang;
		code = languageTemplates[language];
	}

	function getVerdictColor(verdict: string): string {
		switch (verdict) {
			case 'Accepted':
				return 'text-green-600 bg-green-50 border-green-200';
			case 'Wrong Answer':
				return 'text-yellow-600 bg-yellow-50 border-yellow-200';
			case 'Runtime Error':
			case 'Time Limit Exceeded':
			case 'Memory Limit Exceeded':
			case 'Compilation Error':
			case 'Unsafe Code':
				return 'text-red-600 bg-red-50 border-red-200';
			default:
				return 'text-gray-600 bg-gray-50 border-gray-200';
		}
	}
</script>

<svelte:head>
	<title>{problem?.title || 'Problem'} - SkillNest</title>
</svelte:head>

{#if loading}
	<div class="flex justify-center items-center py-12">
		<div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
	</div>
{:else if error && !problem}
	<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
		<p class="font-medium">Error loading problem</p>
		<p class="text-sm">{error}</p>
	</div>
{:else if problem}
	<div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
		<!-- Problem Description -->
		<div class="bg-white p-6 rounded-lg shadow-sm">
			<div class="mb-4 flex items-center justify-between">
				<h1 class="text-3xl font-bold text-gray-900">{problem.title}</h1>
				<span class="px-3 py-1 text-xs font-medium rounded-full {problem.difficulty === 'easy' ? 'bg-green-100 text-green-800' : problem.difficulty === 'medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}">
					{problem.difficulty.toUpperCase()}
				</span>
			</div>

			<div class="mb-4 text-sm text-gray-600">
				<span class="mr-4">⏱️ Time Limit: {problem.time_limit}s</span>
				<span>💾 Memory Limit: {problem.memory_limit}MB</span>
			</div>

			<div class="prose max-w-none mb-6">
				<div class="text-gray-700 whitespace-pre-wrap">{problem.description}</div>
			</div>

			{#if problem.test_cases && problem.test_cases.length > 0}
				<div class="border-t pt-4">
					<h3 class="text-lg font-semibold mb-3">Sample Test Cases</h3>
					{#each problem.test_cases as testCase, index}
						{#if !testCase.is_hidden}
							<div class="mb-4 p-4 bg-gray-50 rounded">
								<p class="text-sm font-medium text-gray-700 mb-1">Test Case {index + 1}</p>
								<div class="mb-2">
									<p class="text-xs text-gray-600">Input:</p>
									<pre class="text-sm bg-white p-2 rounded border">{testCase.input}</pre>
								</div>
								<div>
									<p class="text-xs text-gray-600">Expected Output:</p>
									<pre class="text-sm bg-white p-2 rounded border">{testCase.expected_output}</pre>
								</div>
							</div>
						{/if}
					{/each}
				</div>
			{/if}
		</div>

		<!-- Code Editor & Submission -->
		<div class="bg-white p-6 rounded-lg shadow-sm">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-xl font-bold text-gray-900">Code Editor</h2>
				{#if !$authStore.isAuthenticated}
					<p class="text-sm text-yellow-600">
						<a href="/login" class="underline">Login</a> to submit code
					</p>
				{/if}
			</div>

			<!-- Language Selector -->
			<div class="mb-4">
				<label class="block text-sm font-medium text-gray-700 mb-2">Language</label>
				<div class="flex gap-2">
					{#each ['python', 'java', 'c', 'cpp'] as lang}
						<button
							on:click={() => changeLanguage(lang)}
							class="px-4 py-2 rounded-md font-medium transition {language === lang ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}"
						>
							{lang.toUpperCase()}
						</button>
					{/each}
				</div>
			</div>

			<!-- Code Editor -->
			<div class="mb-4">
				<CodeEditor bind:code {language} height="400px" />
			</div>

			<!-- Submit Button -->
			<button
				on:click={submitCode}
				disabled={submitting || !$authStore.isAuthenticated}
				class="w-full bg-blue-600 text-white py-3 px-4 rounded-md font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition"
			>
				{submitting ? 'Submitting...' : 'Submit Code'}
			</button>

			<!-- Submission Result -->
			{#if result}
				<div class="mt-4 p-4 border rounded {getVerdictColor(result.verdict)}">
					<h3 class="text-lg font-bold mb-2">Submission Result</h3>
					<p class="mb-2"><strong>Verdict:</strong> {result.verdict}</p>
					{#if result.runtime}
						<p class="mb-1"><strong>Runtime:</strong> {result.runtime.toFixed(2)} ms</p>
					{/if}
					{#if result.memory}
						<p class="mb-1"><strong>Memory:</strong> {result.memory.toFixed(2)} MB</p>
					{/if}
					{#if result.time_complexity}
						<p class="mb-1"><strong>Time Complexity:</strong> {result.time_complexity}</p>
					{/if}
					{#if result.space_complexity}
						<p class="mb-1"><strong>Space Complexity:</strong> {result.space_complexity}</p>
					{/if}
				</div>
			{/if}

			{#if error && !result}
				<div class="mt-4 p-4 border rounded bg-red-50 border-red-200 text-red-700">
					<p class="font-medium">Error:</p>
					<p class="text-sm">{error}</p>
				</div>
			{/if}
		</div>
	</div>
{/if}