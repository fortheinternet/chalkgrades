<script>
export default {
  props: {
    buttonText: String,
    routePath: String,
    internal: Boolean
  },
  methods: {
    navigateToPage() {
      this.$router.push(this.routePath);
    },
  },
};
</script>

<template>
  <button @click="navigateToPage" v-if="internal" class="ChipButton-btn">{{ buttonText }}</button>
  <a :href="routePath" v-else class="ChipButton-btn">{{ buttonText }}</a>
</template>

<style>

.ChipButton-btn {
  @apply w-full lg:w-max lg:inline block text-left text-small dark:bg-white bg-black dark:bg-opacity-5 bg-opacity-5 py-2 px-5 rounded-full mr-3 mb-4 select-none
}

</style>