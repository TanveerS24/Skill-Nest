import { c as create_ssr_component, e as escape, d as add_attribute } from "../../../chunks/ssr.js";
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let filteredProblems;
  let problems = [];
  let searchQuery = "";
  filteredProblems = problems.filter((problem) => {
    const matchesSearch = problem.title.toLowerCase().includes(searchQuery.toLowerCase()) || problem.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSearch;
  });
  return `${$$result.head += `<!-- HEAD_svelte-9kh34_START -->${$$result.title = `<title>Problems - SkillNest</title>`, ""}<!-- HEAD_svelte-9kh34_END -->`, ""} <div><div class="mb-8" data-svelte-h="svelte-1l32iww"><h1 class="text-4xl font-bold text-gray-900 mb-2">Coding Problems</h1> <p class="text-gray-600">Solve Data Structure &amp; Algorithm problems in Python, Java, C, or C++</p></div>  <div class="bg-white p-4 rounded-lg shadow-sm mb-6"><div class="flex flex-col md:flex-row gap-4 items-center justify-between"><div class="flex gap-2"><button class="${"px-4 py-2 rounded-md font-medium transition " + escape(
    "bg-blue-600 text-white",
    true
  )}">All</button> <button class="${"px-4 py-2 rounded-md font-medium transition " + escape(
    "bg-gray-100 text-gray-700 hover:bg-gray-200",
    true
  )}">Easy</button> <button class="${"px-4 py-2 rounded-md font-medium transition " + escape(
    "bg-gray-100 text-gray-700 hover:bg-gray-200",
    true
  )}">Medium</button> <button class="${"px-4 py-2 rounded-md font-medium transition " + escape(
    "bg-gray-100 text-gray-700 hover:bg-gray-200",
    true
  )}">Hard</button></div> <div class="w-full md:w-auto"><input type="text" placeholder="Search problems..." class="w-full md:w-64 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"${add_attribute("value", searchQuery)}></div></div></div>  ${`<div class="flex justify-center items-center py-12" data-svelte-h="svelte-d851he"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>`} <div class="mt-8 text-center text-sm text-gray-500">Showing ${escape(filteredProblems.length)} of ${escape(problems.length)} problems</div></div>`;
});
export {
  Page as default
};
