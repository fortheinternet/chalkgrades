<script>
  export default {
    props: {
      routePath: '',
      highlighted: false,
      internal: false
    },
    methods: {
      navigateToPage() {
        this.$router.push(this.routePath)
      }
    },
    computed: {
      buttonClass() {
        return this.highlighted ? 'Button-btn-highlighted' : null
      }
    }
  }
</script>

<template>
  <a
    @click="navigateToPage"
    v-if="internal"
    :class="buttonClass"
    class="Button-btn"
  >
    <slot></slot>
  </a>

  <a :href="routePath" v-else :class="buttonClass" class="Button-btn">
    <slot></slot>
  </a>
</template>

<style scoped>
  .Button-btn {
    @apply block w-full cursor-pointer select-none rounded-3xl border-[1px] border-solid border-black border-opacity-5 px-5 py-2 text-left text-base font-semibold sm:w-max dark:border-white dark:border-opacity-5;
  }

  .Button-btn-highlighted {
    @apply border-black border-opacity-5 bg-black bg-opacity-5 dark:border-white dark:border-opacity-5 dark:bg-white dark:bg-opacity-5;
  }
</style>
