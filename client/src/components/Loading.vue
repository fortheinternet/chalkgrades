<template>
  <p class="loading">
    {{ $t('loading') }}
  </p>
</template>

<style scoped>
  .loading {
    @apply w-full select-none rounded-xl border-[1px] border-solid border-black border-opacity-5 bg-black bg-opacity-5 px-5 py-2 text-left text-base font-semibold dark:border-white dark:border-opacity-5 dark:bg-white dark:bg-opacity-5;
  }
</style>
