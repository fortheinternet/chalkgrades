<script>
  export default {
    props: {
      routePath: '',
      variant: ''
    },
    methods: {
      navigateToPage() {
        if (this.routePath) {
          this.$router.push(this.routePath)
        }
      }
    },
    computed: {
      buttonClass() {
        return 'Button-btn-' + this.variant
      }
    }
  }
</script>

<template>
  <button @click="navigateToPage" :class="buttonClass" class="Button-btn">
    <slot></slot>
  </button>
</template>

<style scoped>
  .Button-btn {
    @apply block w-full cursor-pointer select-none rounded-xl border-[1px] border-solid border-black border-opacity-5 px-5 py-2 text-left text-base font-semibold sm:w-max dark:border-white dark:border-opacity-5;
  }

  .Button-btn-highlighted {
    @apply bg-black bg-opacity-5 dark:bg-white dark:bg-opacity-5;
  }

  .Button-btn-ghost {
    @apply border-0 border-none;
  }
</style>
