<script>
export default {
  props: {
    routePath: String,
    icon: String,
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
    <a @click="navigateToPage" v-if="internal" class="AsideButton-btn"><slot></slot></a>
    <a :href="routePath" v-else class="AsideButton-btn"><slot></slot></a>
  </div>

</template>

<style>

.AsideButton-btn {
  @apply w-full lg:w-max flex justify-start gap-4 items-center text-left text-[14px] p-1 mb-0.5 rounded-full select-none cursor-pointer
}

</style>