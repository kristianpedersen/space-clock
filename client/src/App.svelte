<script>
  import Body from "./Body.svelte";
  const bodyDataRequest = getBodyInformation();
  const t = getTime();
  let ticks = 0;

  function addLeadingZero(n) {
    if (n < 10) {
      return "0" + n;
    }
    return n;
  }

  async function getTime() {
    const response = await fetch("./get-current-time");
    const data = await response.text();
    return data;
  }

  async function getBodyInformation() {
    const response = await fetch("./get-body-info");
    const data = await response.text();
    const divs = document.querySelectorAll("div.body");
    return (
      data
        // Remove starting and closing square brackets
        .slice(1, data.length - 1)
        // Replace single quotes with double quotes
        .replaceAll(`'`, `"`)
        // Create array with individual objects
        .split("},")
        // Add closing curly brace to all except last element
        .map((e, i, a) => (i !== a.length - 1 ? e + "}" : e))
        // Convert each item to object
        .map(JSON.parse)
    );
  }
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
  <h1>Tidsmaskin</h1>

  {#await bodyDataRequest then bodies}
    {#each bodies as body}
      <Body object={body} />
    {/each}
  {/await}

  <p>
    ... og dette er bare småtteri i forhold til de andre galaksene, som er minst
    2,5 millioner lysår unna.
  </p>
</main>
