<script>
export default {
  props: {
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
  <div class="flex justify-between w-full">
    <a @click="navigateToPage" v-if="internal" class="AsideButton">
      <slot></slot>
    </a>

    <a :href="routePath" v-else class="AsideButton">
      <slot></slot>
    </a>
  </div>
</template>