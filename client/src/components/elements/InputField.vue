<script>
export default {
    props: {
        placeholder: String
    }
}
</script>

<template>
    <input :placeholder="placeholder" class="InputField-input">
</template>

<style scoped>

.InputField-input {
    @apply w-full block text-left text-small font-semibold dark:bg-white bg-black dark:bg-opacity-10 bg-opacity-10 py-2 px-5 rounded-3xl mr-3 mb-4 select-none h-[36px] outline-none;
}

</style>