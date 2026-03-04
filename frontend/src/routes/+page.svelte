<script>
	import Navbar from '$lib/components/Navbar.svelte';
</script>

<div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
	<Navbar />
	<main class="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
		<div class="max-w-md w-full">
			<div class="text-center mb-8">
				<h1 class="text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-blue-600">
					SkillNest
				</h1>
				<p class="mt-4 text-xl text-gray-600">
					Master coding through practice
				</p>
			</div>

			<div class="bg-white rounded-lg shadow-xl p-8">
				<div class="space-y-4">
					<a
						href="/login"
						class="block w-full bg-gradient-to-r from-indigo-600 to-blue-600 text-white py-3 px-4 rounded-md text-center font-semibold hover:from-indigo-700 hover:to-blue-700 transition"
					>
						Login
					</a>
					<a
						href="/register"
						class="block w-full bg-white border-2 border-indigo-600 text-indigo-600 py-3 px-4 rounded-md text-center font-semibold hover:bg-indigo-50 transition"
					>
						Register
					</a>
				</div>

				<div class="mt-8 text-center">
					<a href="/admin/login" class="text-sm text-gray-600 hover:text-gray-800">
						Admin Login
					</a>
				</div>
			</div>

			<div class="mt-8 grid grid-cols-3 gap-4 text-center">
				<div class="bg-white rounded-lg p-4 shadow">
					<p class="text-3xl font-bold text-indigo-600">100+</p>
					<p class="text-sm text-gray-600">Problems</p>
				</div>
				<div class="bg-white rounded-lg p-4 shadow">
					<p class="text-3xl font-bold text-blue-600">4</p>
					<p class="text-sm text-gray-600">Languages</p>
				</div>
				<div class="bg-white rounded-lg p-4 shadow">
					<p class="text-3xl font-bold text-purple-600">AI</p>
					<p class="text-sm text-gray-600">Powered</p>
				</div>
			</div>
		</div>
	</main>
</div>
