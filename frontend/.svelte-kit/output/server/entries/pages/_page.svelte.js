import { c as create_ssr_component, a as subscribe, e as escape } from "../../chunks/ssr.js";
import { a as authStore } from "../../chunks/authStore.js";
import "@sveltejs/kit/internal";
import "../../chunks/exports.js";
import "../../chunks/utils.js";
import "@sveltejs/kit/internal/server";
import "../../chunks/state.svelte.js";
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $authStore, $$unsubscribe_authStore;
  $$unsubscribe_authStore = subscribe(authStore, (value) => $authStore = value);
  let stats = {
    totalProblems: 6,
    totalUsers: 0,
    totalSubmissions: 0
  };
  $$unsubscribe_authStore();
  return `${$$result.head += `<!-- HEAD_svelte-wyh7g7_START -->${$$result.title = `<title>SkillNest - Multi-Language Coding Platform</title>`, ""}<!-- HEAD_svelte-wyh7g7_END -->`, ""} <div class="min-h-[calc(100vh-12rem)]"> <section class="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-20 rounded-lg mb-12"><div class="text-center"><h1 class="text-5xl font-bold mb-4" data-svelte-h="svelte-h6sco5">Welcome to SkillNest</h1> <p class="text-xl mb-8 text-blue-100" data-svelte-h="svelte-yfxcep">Master Data Structures &amp; Algorithms with Real-time Code Execution</p> <div class="flex justify-center gap-4">${$authStore.isAuthenticated ? `<a href="/problems" class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition" data-svelte-h="svelte-mwtaze">Browse Problems</a> <a href="/dashboard" class="bg-blue-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-400 transition" data-svelte-h="svelte-1d5kxwz">My Dashboard</a>` : `<a href="/register" class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition" data-svelte-h="svelte-1ozyopi">Get Started</a> <a href="/problems" class="bg-blue-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-400 transition" data-svelte-h="svelte-dluot9">Browse Problems</a>`}</div></div></section>  <section class="grid md:grid-cols-3 gap-8 mb-12" data-svelte-h="svelte-1xxhk1r"><div class="bg-white p-6 rounded-lg shadow-md"><div class="text-3xl mb-4">🐍</div> <h3 class="text-xl font-bold mb-2">Multi-Language Support</h3> <p class="text-gray-600">Code in Python, Java, C, or C++. All solutions run in isolated Docker containers.</p></div> <div class="bg-white p-6 rounded-lg shadow-md"><div class="text-3xl mb-4">🤖</div> <h3 class="text-xl font-bold mb-2">AI Code Analysis</h3> <p class="text-gray-600">Get instant feedback on time/space complexity and security issues before execution.</p></div> <div class="bg-white p-6 rounded-lg shadow-md"><div class="text-3xl mb-4">🏆</div> <h3 class="text-xl font-bold mb-2">Dynamic Leaderboard</h3> <p class="text-gray-600">Compete with others! Sort by problems solved, complexity score, or submission count.</p></div></section>  <section class="bg-white p-8 rounded-lg shadow-md"><h2 class="text-2xl font-bold text-center mb-6" data-svelte-h="svelte-1rv6eav">Platform Statistics</h2> <div class="grid md:grid-cols-3 gap-6 text-center"><div><div class="text-4xl font-bold text-blue-600">${escape(stats.totalProblems)}</div> <div class="text-gray-600 mt-2" data-svelte-h="svelte-1uegp9r">DSA Problems</div></div> <div><div class="text-4xl font-bold text-green-600">${escape(stats.totalUsers)}+</div> <div class="text-gray-600 mt-2" data-svelte-h="svelte-749ssh">Active Users</div></div> <div><div class="text-4xl font-bold text-purple-600">${escape(stats.totalSubmissions)}+</div> <div class="text-gray-600 mt-2" data-svelte-h="svelte-3ql4b3">Code Submissions</div></div></div></section>  <section class="mt-12 text-center" data-svelte-h="svelte-zx5smi"><h2 class="text-3xl font-bold mb-4">Ready to Start Coding?</h2> <p class="text-gray-600 mb-6">Join thousands of developers improving their problem-solving skills</p> <a href="/problems" class="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition">View All Problems</a></section></div>`;
});
export {
  Page as default
};
