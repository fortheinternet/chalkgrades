<template>
  <p class="loading">
    {{ $t('loading') }}
  </p>
</template>

<style scoped>
  .loading {
    @apply select-none rounded-3xl border-[1px] border-solid border-yellow border-opacity-5 bg-yellow bg-opacity-5 px-5 py-2 text-base font-semibold text-yellow;
  }
</style>
