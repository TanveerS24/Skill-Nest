<script lang="ts">
  import { onMount } from 'svelte';
  import type { User } from '$lib/types';

  let user: User | null = null;

  onMount(async () => {
    const response = await fetch('/profile');
    if (response.ok) {
      user = await response.json();
    }
  });
</script>

<main class="p-8">
  <h1 class="text-3xl font-bold mb-6">Profile</h1>

  {#if user}
    <div class="border rounded-lg p-4 shadow">
      <h2 class="text-xl font-semibold">User ID</h2>
      <p class="text-lg">{user.id}</p>

      <h2 class="text-xl font-semibold mt-4">Email</h2>
      <p class="text-lg">{user.email}</p>

      <h2 class="text-xl font-semibold mt-4">Role</h2>
      <p class="text-lg capitalize">{user.role}</p>
    </div>
  {/if}
</main>