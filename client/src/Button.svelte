<script>
export let count = 42;

function increment() {
	count++;
}
</script>

<button on:click={increment}>Hei! {count}</button>