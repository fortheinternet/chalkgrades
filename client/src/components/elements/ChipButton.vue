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
      return this.highlighted ? 'ChipButton-btn-highlighted' : null
    }
  }
};
</script>

<template>
  <a @click="navigateToPage" v-if="internal" :class="buttonClass" class="ChipButton-btn">
    <slot></slot>
  </a>
  
  <a :href="routePath" v-else :class="buttonClass" class="ChipButton-btn">
    <slot></slot>
  </a>
</template>

<style scoped>
.ChipButton-btn {
  @apply sm:w-max w-full block text-left text-small font-semibold dark:bg-white bg-black dark:bg-opacity-10 bg-opacity-10 py-2 px-5 rounded-3xl mr-3 mb-4 select-none cursor-pointer;
}

.ChipButton-btn-highlighted {
  @apply dark:bg-white bg-black dark:text-black text-white;
}
</style>