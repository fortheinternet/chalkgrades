<script>
export default {
  props: {
    routePath: String,
    highlighted: Boolean,
    internal: Boolean
  },
  methods: {
    navigateToPage() {
      this.$router.push(this.routePath);
    },
  },
  computed: {
    buttonClass() {
      return this.highlighted ? 'ChipButton-btn-highlighted' : 'ChipButton-btn-default';
    }
  }
};
</script>

<template>
  <button @click="navigateToPage" v-if="internal" :class="buttonClass"><slot></slot></button>
  <a :href="routePath" v-else :class="buttonClass"><slot></slot></a>
</template>

<style>
.ChipButton-btn-default {
  @apply w-full lg:w-max lg:inline block text-left text-small font-semibold dark:bg-white bg-black dark:bg-opacity-10 bg-opacity-10 py-2 px-5 rounded-full mr-3 mb-4 select-none;
}

.ChipButton-btn-highlighted {
  @apply w-full lg:w-max lg:inline block text-left text-small font-semibold dark:bg-white bg-black dark:text-black text-white py-2 px-5 rounded-full mr-3 mb-4 select-none;
}
</style>
