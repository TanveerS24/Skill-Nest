import { c as create_ssr_component, b as each, e as escape, a as subscribe, v as validate_component } from "../../../chunks/ssr.js";
import { w as writable } from "../../../chunks/index.js";
import { l as leaderboardApi } from "../../../chunks/client.js";
function getEntryEmail(entry) {
  return entry.email;
}
function getEntryUserId(entry) {
  return entry.user_id;
}
function getEntryProblemsSolved(entry) {
  return entry.problems_solved;
}
function getEntryAvgTimeComplexity(entry) {
  return entry.avg_time_complexity;
}
function getEntryAvgSpaceComplexity(entry) {
  return entry.avg_space_complexity;
}
function getEntryTotalSubmissions(entry) {
  return entry.total_submissions;
}
function getComplexityBadge(score) {
  if (score <= 1.5) return "O(1)";
  if (score <= 2.5) return "O(log n)";
  if (score <= 3.5) return "O(n)";
  if (score <= 4.5) return "O(n log n)";
  return "O(n²)";
}
function getDifficultyColor(score) {
  if (score <= 2) return "text-green-600";
  if (score <= 3.5) return "text-yellow-600";
  return "text-red-600";
}
const LeaderboardTable = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { entries = [] } = $$props;
  let { loading = false } = $$props;
  if ($$props.entries === void 0 && $$bindings.entries && entries !== void 0) $$bindings.entries(entries);
  if ($$props.loading === void 0 && $$bindings.loading && loading !== void 0) $$bindings.loading(loading);
  return `${loading ? `<div class="flex justify-center items-center py-8" data-svelte-h="svelte-19h479d"><div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>` : `${entries.length === 0 ? `<div class="text-center py-8 text-gray-500" data-svelte-h="svelte-1g4wkk8"><p>No entries found</p></div>` : `<div class="overflow-x-auto shadow-md rounded-lg"><table class="min-w-full divide-y divide-gray-200"><thead class="bg-gray-50" data-svelte-h="svelte-6g84q0"><tr><th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rank</th> <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User</th> <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Problems Solved</th> <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Time Complexity</th> <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Avg Space Complexity</th> <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Total Submissions</th></tr></thead> <tbody class="bg-white divide-y divide-gray-200">${each(entries, (entry, index) => {
    return `<tr class="hover:bg-gray-50 transition-colors"><td class="px-6 py-4 whitespace-nowrap"><span class="font-bold text-lg">${escape(index + 1)}</span></td> <td class="px-6 py-4 whitespace-nowrap"><div class="text-sm font-medium text-gray-900">${escape(getEntryEmail(entry))}</div> <div class="text-xs text-gray-500">ID: ${escape(getEntryUserId(entry))}</div></td> <td class="px-6 py-4 whitespace-nowrap"><span class="px-2 py-1 text-sm font-semibold text-blue-800 bg-blue-100 rounded-full">${escape(getEntryProblemsSolved(entry))} </span></td> <td class="px-6 py-4 whitespace-nowrap"><span class="${"text-sm font-mono " + escape(getDifficultyColor(getEntryAvgTimeComplexity(entry)), true)}">${escape(getComplexityBadge(getEntryAvgTimeComplexity(entry)))} </span></td> <td class="px-6 py-4 whitespace-nowrap"><span class="${"text-sm font-mono " + escape(getDifficultyColor(getEntryAvgSpaceComplexity(entry)), true)}">${escape(getComplexityBadge(getEntryAvgSpaceComplexity(entry)))} </span></td> <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">${escape(getEntryTotalSubmissions(entry))}</td> </tr>`;
  })}</tbody></table></div>`}`}`;
});
const initialState = {
  entries: [],
  loading: false,
  error: null,
  sortBy: "solved"
};
function createLeaderboardStore() {
  const { subscribe: subscribe2, set, update } = writable(initialState);
  return {
    subscribe: subscribe2,
    async fetchLeaderboard(sortBy = "solved", problemId, limit = 100) {
      update((state) => ({ ...state, loading: true, error: null, sortBy }));
      try {
        const entries = await leaderboardApi.getLeaderboard(sortBy, problemId, limit);
        update((state) => ({
          ...state,
          entries,
          loading: false
        }));
      } catch (error) {
        update((state) => ({
          ...state,
          loading: false,
          error: error.message
        }));
      }
    },
    clearError() {
      update((state) => ({ ...state, error: null }));
    }
  };
}
const leaderboardStore = createLeaderboardStore();
const Page = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let $leaderboardStore, $$unsubscribe_leaderboardStore;
  $$unsubscribe_leaderboardStore = subscribe(leaderboardStore, (value) => $leaderboardStore = value);
  let sortBy = "solved";
  async function loadLeaderboard() {
    await leaderboardStore.fetchLeaderboard(sortBy);
  }
  {
    {
      loadLeaderboard();
    }
  }
  $$unsubscribe_leaderboardStore();
  return `${$$result.head += `<!-- HEAD_svelte-9muiut_START -->${$$result.title = `<title>Leaderboard - SkillNest</title>`, ""}<!-- HEAD_svelte-9muiut_END -->`, ""} <div><div class="mb-8" data-svelte-h="svelte-a6iurd"><h1 class="text-4xl font-bold text-gray-900 mb-2">Leaderboard</h1> <p class="text-gray-600">Top performers on SkillNest coding platform</p></div>  <div class="bg-white p-4 rounded-lg shadow-sm mb-6"><div class="flex items-center gap-4"><label class="text-sm font-medium text-gray-700" data-svelte-h="svelte-hzdii">Sort By:</label> <div class="flex gap-2"><button class="${"px-4 py-2 rounded-md font-medium transition " + escape(
    "bg-blue-600 text-white",
    true
  )}">Problems Solved</button> <button class="${"px-4 py-2 rounded-md font-medium transition " + escape(
    "bg-gray-100 text-gray-700 hover:bg-gray-200",
    true
  )}">Time Complexity</button> <button class="${"px-4 py-2 rounded-md font-medium transition " + escape(
    "bg-gray-100 text-gray-700 hover:bg-gray-200",
    true
  )}">Space Complexity</button></div></div></div>  ${$leaderboardStore.error ? `<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded"><p class="font-medium" data-svelte-h="svelte-mxvg51">Error loading leaderboard</p> <p class="text-sm">${escape($leaderboardStore.error)}</p> <button class="mt-2 text-sm underline hover:no-underline" data-svelte-h="svelte-avcekj">Try again</button></div>` : `${validate_component(LeaderboardTable, "LeaderboardTable").$$render(
    $$result,
    {
      entries: $leaderboardStore.entries,
      loading: $leaderboardStore.loading
    },
    {},
    {}
  )}`}  <div class="mt-6 bg-blue-50 border border-blue-200 p-4 rounded-lg" data-svelte-h="svelte-xard83"><h3 class="font-semibold text-blue-900 mb-2">How Ranking Works</h3> <ul class="text-sm text-blue-800 space-y-1"><li>• Problems Solved: Ranked by unique problems successfully completed</li> <li>• Time Complexity: Lower average complexity score ranks higher (O(1) = 1, O(log n) = 2, O(n) = 3, O(n log n) = 4, O(n²) = 5)</li> <li>• Space Complexity: Same scoring as time complexity</li></ul></div></div>`;
});
export {
  Page as default
};
