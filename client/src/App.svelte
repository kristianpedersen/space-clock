<script>
  import Button from "./Button.svelte";
  import Clock from "./Clock.svelte";
  export let name;
  let count;
</script>

<style>
  main {
    text-align: center;
    padding: 1em;
    max-width: 240px;
    margin: 0 auto;
  }

  h1 {
    color: #ff3e00;
    text-transform: uppercase;
    font-size: 4em;
    font-weight: 100;
  }

  @media (min-width: 640px) {
    main {
      max-width: none;
    }
  }
</style>

<main>
<h1>Solar system clock</h1>
<Clock />
</main>

<input type="text" bind:value={name} />
