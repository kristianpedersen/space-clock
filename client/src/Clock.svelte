<script>
  let planets = ["Moon", "Mars", "Jupiter"];
</script>

<ul>
  {#each planets as planet}
    <li>{planet}</li>
  {/each}
</ul>
